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
from matplotlib import cm
from matplotlib.colors import ListedColormap

#read in ourput csvs
intervention_old = pd.read_csv('C:/git/vector_bugfix/results/raw/prev/MAP_20200924_test_vector_bug_Int_old.csv')
intervention_new = pd.read_csv('C:/git/vector_bugfix/results/raw/prev/MAP_20200924_test_vector_bug_Int_new.csv')
burnin_old = pd.read_csv('C:/git/vector_bugfix/results/raw/prev/MAP_20200924_test_vector_bug_Burnin_old.csv')
burnin_new = pd.read_csv('C:/git/vector_bugfix/results/raw/prev/MAP_20200924_test_vector_bug_Burnin_new.csv')


#slice last timepoint from burnin
burnin_new = burnin_new[burnin_new.day == 14235]
burnin_old = burnin_old[burnin_old.day == 14235]

#slice just the no IRS version of intervention
intervention_new = intervention_new[intervention_new['IRS_Coverage'] == 0]
intervention_old = intervention_old[intervention_old['IRS_Coverage'] == 0]


#merge tables by site, seed, and larval habitat
old_df = pd.merge(intervention_old, burnin_old, on= ["Site_Name", "Run_Number", "x_Temporary_Larval_Habitat"])
new_df = pd.merge(intervention_new, burnin_new, on= ["Site_Name", "Run_Number", "x_Temporary_Larval_Habitat"])

#filter on impact after 3 years of intervention
old_df = old_df[old_df.day_x == 1095]
# old_df.drop(labels = ['CM_Drug','CM_Coverage','IRS_Coverage','ITN_Start'],axis = 1, inplace=True)
new_df = new_df[new_df.day_x == 1095]
# new_df.drop(labels = ['CM_Drug','CM_Coverage','IRS_Coverage','ITN_Start'],axis = 1, inplace=True)

old_df['old_diff'] = old_df['initial_prev']-old_df['final_prev']
new_df['new_diff'] = new_df['initial_prev']-new_df['final_prev']

#merge old and new and add a difference column
diff_df = pd.merge(old_df[['Site_Name','Run_Number','x_Temporary_Larval_Habitat','ITN_Coverage','old_diff']],
                   new_df[['Site_Name','Run_Number','x_Temporary_Larval_Habitat','ITN_Coverage','new_diff']],
                   on= ["Site_Name", "Run_Number", "x_Temporary_Larval_Habitat","ITN_Coverage"])
fig,axes = plt.subplots(nrows = 3,ncols=4)
archetype_list = [1,10,11,12,2,3,4,5,6,7,8,9]
coverages = np.sort(diff_df.ITN_Coverage.unique())
viridis = cm.get_cmap('viridis',len(coverages))
cmap = ['#440154ff','#433880ff','#31678dff','#21918dff','#3cb875ff']
archetype_counter = 0
for i in np.arange(3):
    for j in np.arange(4):
        for col,cov in enumerate(coverages):
            sub_df = diff_df[(diff_df['Site_Name'] == archetype_list[archetype_counter])
                             &(diff_df['ITN_Coverage'] == cov)]
            axes[i,j].scatter(sub_df['old_diff'],sub_df['new_diff'],alpha = 0.05,color =cmap[col])
            # m,b = np.polyfit(x=sub_df['old_diff'],y=sub_df['new_diff'],1)
            x = np.linspace(np.min(sub_df['old_diff']), np.max(sub_df['old_diff']))

        axes[i,j].plot(x,x,linestyle='dashed',color = 'k')
        axes[i,j].set_title(f'Archetype{archetype_list[archetype_counter]}')
        archetype_counter+=1

fig.text(0.5, 0.012, 'PfPR reduction (pre-bug fix)', ha='center', va='center')
fig.text(0.012, 0.5, 'PfPR reduction (post-bug fix)', ha='center', va='center',rotation='vertical')
plt.tight_layout()
plt.savefig('C:/git/vector_bugfix/diff_by_site_and_coverage.eps')
plt.savefig('C:/git/vector_bugfix/diff_by_site_and_coverage.png')

plt.show()
diff_df['difference'] = pd.Series()