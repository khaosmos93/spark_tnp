
# allowed choices
def get_allowed_resonances():
    
    resonances = [
        'Z',
        'JPsi'
    ]
    return resonances


def get_allowed_eras(resonance):

    eras = {
        'Z': [
            # ultra legacy
            'Run2016_UL_HIPM',
            'Run2016_UL',
            'Run2017_UL',
            'Run2018_UL',
            # rereco
            'Run2016',
            'Run2017',
            'Run2018',
            # dR studies
            'Run2018_dR0p1',
            'Run2018_dR0p2',
            'Run2018_dR0p3',
            'Run2018_dR0p4'
        ],
        'JPsi': [
            # heavy ion
            'Run2016_HI_pPb_8TeV',
            # rereco
            'Run2016',
            'Run2017',
            'Run2018'
        ],
    }
    return eras.get(resonance, [])


def get_allowed_sub_eras(resonance, era):
    
    subEras = {
        'Z': {
            # ultra legacy
            'Run2016_UL_HIPM': ['Run2016'] + [
                f'Run2016{b}' for b in 'BCDEF']+['DY_madgraph'],
            'Run2016_UL': ['Run2016'] + [
                f'Run2016{b}' for b in 'FGH']+['DY_madgraph'],
            'Run2017_UL': ['Run2017'] + [
                f'Run2017{b}' for b in 'BCDEF']+['DY_madgraph'],
            'Run2018_UL': ['Run2018'] + [
                f'Run2018{b}' for b in 'ABCD']+['DY_madgraph', 'DY_powheg'],
            # rereco
            'Run2016': ['Run2016'] + [
               f'Run2016{b}' for b in 'BCDEFGH']+['DY_madgraph'],
            'Run2017': ['Run2017'] + [
               f'Run2017{b}' for b in 'BCDEF']+['DY_madgraph'],
            'Run2018': ['Run2018'] + [
               f'Run2018{b}' for b in 'ABCD']+['DY_madgraph'],
            # dR studies
            'Run2018_dR0p1': ['Run2018'] + [
               f'Run2018{b}' for b in 'ABCD']+['DY_madgraph'],
            'Run2018_dR0p2': ['Run2018'] + [
               f'Run2018{b}' for b in 'ABCD']+['DY_madgraph'],
            'Run2018_dR0p3': ['Run2018'] + [
               f'Run2018{b}' for b in 'ABCD']+['DY_madgraph'],
            'Run2018_dR0p4': ['Run2018'] + [
               f'Run2018{b}' for b in 'ABCD']+['DY_madgraph'],
        },
        'JPsi': {
            # ultra legacy
            'Run2017_UL': ['Run2017'] + [
                f'Run2017{b}' for b in 'BCDEF']+['JPsi_pythia8'],
            # heavy ion
            'Run2016_HI_pPb_8TeV': ['Run2016'],
            # rereco
            'Run2016': ['Run2016'] + [
               f'Run2016{b}' for b in 'BCDEFGH']+['JPsi_pythia8'],
            'Run2017': ['Run2017'] + [
               f'Run2017{b}' for b in 'BCDEF']+['JPsi_pythia8'],
            'Run2018': ['Run2018'] + [
               f'Run2018{b}' for b in 'ABCD']+['JPsi_pythia8'],
        },
    }
    return subEras.get(resonance, {}).get(era, [])


def get_data_mc_sub_eras(resonance, era):
    eraMap = {
        'Z': {
            # ultra legacy
            'Run2016_UL_HIPM': ['Run2016', 'DY_madgraph'],
            'Run2016_UL': ['Run2016', 'DY_madgraph'],
            'Run2017_UL': ['Run2017', 'DY_madgraph'],
            # TODO: decide how to handle alternate generators
            'Run2018_UL': ['Run2018', 'DY_madgraph'],
            # rereco
            'Run2016': ['Run2016', 'DY_madgraph'],
            'Run2017': ['Run2017', 'DY_madgraph'],
            'Run2018': ['Run2018', 'DY_madgraph'],
            # dR studies
            'Run2018_dR0p1': ['Run2018', 'DY_madgraph'],
            'Run2018_dR0p2': ['Run2018', 'DY_madgraph'],
            'Run2018_dR0p3': ['Run2018', 'DY_madgraph'],
            'Run2018_dR0p4': ['Run2018', 'DY_madgraph'],
        },
        'JPsi': {
            # ultra legacy
            'Run2017_UL': ['Run2017', 'JPsi_pythia8'],
            # heavy ion
            'Run2016_HI_pPb_8TeV': ['Run2016', None],
            # Rereco (Charmonium)
            'Run2016': ['Run2016', 'JPsi_pythia8'],
            'Run2017': ['Run2017', 'JPsi_pythia8'],
            'Run2018': ['Run2018', 'JPsi_pythia8'],
        },
    }
    return eraMap.get(resonance, {}).get(era, [None, None])

