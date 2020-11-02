#!/usr/bin/env python
from __future__ import print_function
import os
import sys
from TagAndProbeFitter import TagAndProbeFitter
import ROOT
ROOT.gROOT.SetBatch()
# kInfo = 1001, kWarning = 2001, ...
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")
ROOT.gROOT.LoadMacro('RooCMSShape.cc+')


def hist_fitter(outFName, inFName, binName, templateFName, plotDir,
                version='Nominal', histType='data', shiftType='Nominal'):



    tnpNomFitSig = [
        "meanP1[91,84,98]",  "widthP1[2.495]", "sigmaP1[2.5,1,6]",
        "meanP2[91,81,101]", "widthP2[2.495]", "sigmaP2[5,1,10]",
        "Voigtian::sigPass1(x, meanP1, widthP1, sigmaP1)",
        "Voigtian::sigPass2(x, meanP2, widthP2, sigmaP2)",
        "SUM::sigPass(fP[0.8, 0, 1]*sigPass1, sigPass2)",

        "meanF1[91,84,98]",  "widthF1[2.495]", "sigmaF1[0.9, 0.5, 3.0]",
        "meanF2[91,81,101]", "widthF2[2.495]", "sigmaF2[4.0, 3.0, 10.0]",
        "Voigtian::sigFail1(x, meanF1, widthF1, sigmaF1)",
        "Voigtian::sigFail2(x, meanF2, widthF2, sigmaF2)",
        "SUM::sigFail(fF[0.8, 0, 1]*sigFail1, sigFail2)",
    ]
    tnpNomFitBkg = [
        "alphaP[-0.1,-1,0.1]",
        "alphaF[-0.1,-1,0.1]",
        "Exponential::bkgPass(x, alphaP)",
        "Exponential::bkgFail(x, alphaF)",
    ]

    tnpWorkspace = []
    doTemplate = False
    if version == 'Nominal':
        tnpWorkspace.extend(tnpNomFitSig)
        tnpWorkspace.extend(tnpNomFitBkg)
    # Trigger: No Sig/Bkg shape variation for now
    # if version == 'NominalOld':
    #     tnpWorkspace.extend(tnpNomFitOldSig)
    #     tnpWorkspace.extend(tnpNomFitOldBkg)
    #     doTemplate = False
    # if version == 'AltSigOld':
    #     tnpWorkspace.extend(tnpAltSigFitOld)
    #     tnpWorkspace.extend(tnpNomFitOldBkg)
    #     doTemplate = False
    # elif version == 'AltSig':
    #     tnpWorkspace.extend(tnpAltSigFit)
    #     tnpWorkspace.extend(tnpNomFitBkg)
    # elif version == 'AltBkg':
    #     tnpWorkspace.extend(tnpNomFitSig)
    #     tnpWorkspace.extend(tnpAltBkgFit)

    def rebin(hP, hF):
        # if shiftType == 'massBinUp':
        #     pass  # no rebin, bin widths are 0.25 GeV
        # elif shiftType == 'massBinDown':
        #     hP = hP.Rebin(4)  # 1.0 GeV bins
        #     hF = hF.Rebin(4)  # 1.0 GeV bins
        # else:
        #     hP = hP.Rebin(2)  # 0.5 GeV bins
        #     hF = hF.Rebin(2)  # 0.5 GeV bins
        # Trigger: Default bin width is 1.5 GeV
        if shiftType == 'massBinUp':
            hP = hP.Rebin(4)  # 1.0 GeV bins
            hF = hF.Rebin(4)  # 1.0 GeV bins
        elif shiftType == 'massBinDown':
            hP = hP.Rebin(8)  # 2.0 GeV bins
            hF = hF.Rebin(8)  # 2.0 GeV bins
        else:
            hP = hP.Rebin(6)  # 1.5 GeV bins
            hF = hF.Rebin(6)  # 1.5 GeV bins
        return hP, hF

    # init fitter
    infile = ROOT.TFile(inFName, "read")
    hP = infile.Get(f'{binName}_Pass')
    hF = infile.Get(f'{binName}_Fail')
    hP, hF = rebin(hP, hF)
    fitter = TagAndProbeFitter(binName)
    fitter.set_histograms(hP, hF)
    infile.Close()

    # mass range systematic
    if shiftType == 'massRangeUp':
        fitter.set_fit_range(75, 135)
    elif shiftType == 'massRangeDown':
        fitter.set_fit_range(65, 125)
    else:
        fitter.set_fit_range(70, 130)

    # setup
    os.makedirs(os.path.dirname(outFName), exist_ok=True)

    # generated Z LineShape
    # for high pT change the failing spectra to any probe to get statistics
    fileTruth = ROOT.TFile(templateFName, 'read')
    if version == 'AltSig':
        # TODO: truth file for ZmmGenLevel instead of reco in case of AltSig
        histZLineShapeP = fileTruth.Get(f'{binName}_Pass_Gen')
        histZLineShapeF = fileTruth.Get(f'{binName}_Fail_Gen')
    else:
        histZLineShapeP = fileTruth.Get(f'{binName}_Pass')
        histZLineShapeF = fileTruth.Get(f'{binName}_Fail')
    histZLineShapeP, histZLineShapeF = rebin(histZLineShapeP, histZLineShapeF)
    fitter.set_gen_shapes(histZLineShapeP, histZLineShapeF)

    fileTruth.Close()

    # set workspace
    fitter.set_workspace(tnpWorkspace, doTemplate)
    fitter.fit(outFName, histType == 'mc', doTemplate)


# TODO other fits and argparse
if __name__ == "__main__":
    argv = sys.argv[1:]
    hist_fitter(*argv)
    sys.exit(0)
