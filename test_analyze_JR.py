import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import matplotlib as mpl
from simtools.Analysis.AnalyzeManager import AnalyzeManager
from simtools.Analysis.BaseAnalyzers import BaseAnalyzer
from simtools.SetupParser import SetupParser
from scipy import interpolate
import os

class test_Analyzer(BaseAnalyzer):
    def __init__(self, output_fname):
        super(test_Analyzer, self).__init__()
        self.filenames = ['output/MalariaSummaryReport_10.json']
        self.output_fname = output_fname

    def select_simulation_data(self, data, simulation):
        simdata = pd.DataFrame(
            {'timeinterval': [data[self.filenames[0]]['Metadata']['PfPR by Age Bin'][0][0]],
             'agebins': [data[self.filenames[0]]['Metadata']['PfPR by Age Bin'][0][1]],
             'incdata': [
                 data[self.filenames[0]]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][0][0]],
             'severedata': [
                 data[self.filenames[0]]['DataByTimeAndAgeBins']['Annual Clinical Incidence by Age Bin'][0][1]],
             'popdata': [data[self.filenames[0]]['DataByTimeAndAgeBins']['PfPR by Age Bin'][0][0]],
             'timedata': [data[self.filenames[0]]['DataByTime']['PfPR by Age Bin'][0][0]],
             }

        )

        for tag in self.tags:
            simdata[tag] = [simulation.tags[tag]]

        return simdata


# json_fname = "/Users/bertozzivill/Desktop/MalariaSummaryReport_10.json"
# with open(json_fname) as f:
#     report = json.loads(f.read())


timeinterval = report["Metadata"]["Reporting_Interval"]
agebins = report["Metadata"]["Age Bins"]
incdata = report["DataByTimeAndAgeBins"]["Annual Clinical Incidence by Age Bin"]
severedata =  report["DataByTimeAndAgeBins"]["Annual Severe Incidence by Age Bin"]
popdata =  report["DataByTimeAndAgeBins"]["Average Population by Age Bin"]
timedata = report["DataByTime"]["Time Of Report"]

max_years = int(max(timedata)/timeinterval)
incidence = [np.average(incdata[x], weights=popdata[x]) for x in range(0, max_years)]
severe_incidence = [severedata[x][0] for x in range(0, max_years)]


