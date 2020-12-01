import os
import glob
import getpass
from pyspark.sql import SparkSession

from registry import registry
from dataset_allowed_definitions import get_allowed_sub_eras


def run_convert(spark, particle, probe, resonance, era, subEra, customDir=''):
    '''
    Converts a directory of root files into parquet
    '''
    
    # fnames = registry.root(particle, probe, resonance, era, subEra)
    # fnames = ['root://eosuser' + f for f in fnames]
    
    baseDir = os.path.join(
        '/hdfs/analytix.cern.ch/user',
        getpass.getuser(), customDir, 'root',
        particle, resonance, era, subEra
        )
    
    print(f'Path to convert from: {baseDir}')

    fnames = glob.glob(os.path.join(baseDir, f'{baseDir}/*.root'))
    fnames = [f.replace('/hdfs/analytix.cern.ch',
                        'hdfs://analytix') for f in fnames]
    
    outDir = os.path.join('parquet', customDir, particle, resonance, era, subEra)     
    outname = os.path.join(outDir, 'tnp.parquet')
    
    # treename = 'tpTree/fitter_tree'
    treename = 'muon/Events'

    print(f'Number of files to process: {len(fnames)}')
    if len(fnames) == 0:
        print('Error! No ROOT files found to convert with desired options.')
        print('Also make sure converter step is run from the edge nodes. Lxplus currently does not mount hdfs as a fuse-style filestystem (i.e. /hdfs/...')
        print('Exiting...')
        return
    print(f'First file: {fnames[0]}')

    # process batchsize files at a time
    batchsize = 500
    new = True
    while fnames:
        current = fnames[:batchsize]
        fnames = fnames[batchsize:]

        rootfiles = spark.read.format("root")\
                         .option('tree', treename)\
                         .load(current)
        # temporary fix for duplicate column names in L3 filter
        rootfiles = rootfiles.drop('probe_hltL3fLMu7p5TrackL3Filtered7p5')\
                             .drop('tag_hltL3fLMu7p5TrackL3Filtered7p5')
        
        # merge rootfiles. chosen to make files of 8-32 MB (input)
        # become at most 1 GB (parquet recommendation)
        # https://parquet.apache.org/documentation/latest/
        # .coalesce(int(len(current)/32)) \
        # but it is too slow for now, maybe try again later
        if new:
            rootfiles.write.parquet(outname)
            new = False
        else:
            rootfiles.write.mode('append')\
                     .parquet(outname)


def run_all(particle, probe, resonance, era, subEra=None, customDir=''):

    if subEra is not None:
        subEras = [subEra]
    else:
        subEras = get_allowed_sub_eras(resonance, era)

    local_jars = ','.join([
        './laurelin-1.0.0.jar',
        './log4j-api-2.13.0.jar',
        './log4j-core-2.13.0.jar',
    ])
    
    spark = SparkSession\
        .builder\
        .appName("TnP")\
        .config("spark.jars", local_jars)\
        .config("spark.driver.extraClassPath", local_jars)\
        .config("spark.executor.extraClassPath", local_jars)\
        .config("spark.dynamicAllocation.maxExecutors", "100")\
        .config("spark.driver.memory", "6g")\
        .config("spark.executor.memory", "4g")\
        .config("spark.executor.cores", "2")\
        .getOrCreate()

    print('\n\n------------------ DEBUG ----------------')
    sc = spark.sparkContext
    print(sc.getConf().toDebugString())
    print('---------------- END DEBUG ----------------\n\n')

    for subEra in subEras:
        print('\nConverting:', particle, probe, resonance, era, subEra)
        run_convert(spark, particle, probe, resonance, era, subEra, customDir)

    spark.stop()
