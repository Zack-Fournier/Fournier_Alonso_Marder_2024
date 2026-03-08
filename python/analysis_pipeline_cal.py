import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
from scipy.integrate import trapz
from matplotlib.ticker import MaxNLocator

# set root folder
root_folder = 'C:/code_package'

# set whether data has been collected from all models (yes=1, no=0)
# this will create plot from figure 4
alldata = 0

#######################################

# get all data folders
# Specify the directory path
directory_path = root_folder + '/DATA'

# set known data parameters
d = ['0','10','20','30','40','50','60','70','80','90','100']
# trial number
n = 1000

# colors
blue = (0.196, 0.427, 0.659)
red = (0.72, 0.125, 0.145)

# initialize
names = []
IC_curves = []
SC_curves = []

# get paths to all folders
folders = [folder for folder in glob.glob(os.path.join(directory_path, '*')) if os.path.isdir(folder)]

# folders to plot
plot_folders = ['Model_A', 'edg461_model0', 'edg461_model64', 'gjd842_model11', 'wcz837_model48', 'gjd842_model16', 'qla777_model76', 'qla777_model4', 'dof948_model5', 'wcz837_model53']

for idx, folder in enumerate(folders):

    # get IC results
    IC_result_path = folder + '/IC_results/data/IC.csv'
    IC_result = pd.read_csv(IC_result_path)
    # get SC results
    SC_result_path = folder + '/SC_results/data/SC.csv'
    SC_result = pd.read_csv(SC_result_path)
    # clear unwanted columns
    # clear unnamed columns
    IC_result = IC_result.loc[:, ~IC_result.columns.str.contains('^Unnamed')]
    SC_result = SC_result.loc[:, ~SC_result.columns.str.contains('^Unnamed')]

    # compress classifications
    IC = np.zeros([len(d)])
    SC = np.zeros([len(d)])

    for i in range(len(d)):
        IC[i] = (IC_result.iloc[:, i] == 2).sum()
        SC[i] = (SC_result.iloc[:, i] == 2).sum()

    # compress and save model name
    folder_name = os.path.basename(folder)
    IC_curve = [folder_name, IC]
    SC_curve = [folder_name, SC]
    IC_curves.append(IC_curve)
    SC_curves.append(SC_curve)

    # produce figure
#################
if alldata == 1:
    # initialize figure
    fig, axs = plt.subplots(5, 2, figsize=(15, 20), dpi=300)

    for idx, folder in enumerate(plot_folders):

        folder = directory_path + '/' + folder + '.txt'

        # get IC results
        IC_result_path = folder + '/IC_results/data/IC.csv'
        IC_result = pd.read_csv(IC_result_path)
        # get SC results
        SC_result_path = folder + '/SC_results/data/SC.csv'
        SC_result = pd.read_csv(SC_result_path)
        # clear unwanted columns
        # clear unnamed columns
        IC_result = IC_result.loc[:, ~IC_result.columns.str.contains('^Unnamed')]
        SC_result = SC_result.loc[:, ~SC_result.columns.str.contains('^Unnamed')]

        # compress classifications
        IC = np.zeros([len(d)])
        SC = np.zeros([len(d)])

        for i in range(len(d)):
            IC[i] = (IC_result.iloc[:, i] == 2).sum()
            SC[i] = (SC_result.iloc[:, i] == 2).sum()

        # Produce subplot for the folder of a sample model
        ax = axs[idx // 2, idx % 2]  # Get subplot location

        ax.plot(d, 100 * SC / n, label='Synaptic', color=red, lw=7)
        ax.scatter(d, 100 * SC / n, color=red, zorder=5, s=150, clip_on=False)

        # Plot lines with shaded regions
        ax.plot(d, 100 * IC / n, label='Intrinsic', color=blue, lw=7)
        ax.scatter(d, 100 * IC / n, color=blue, zorder=5, s=150, clip_on=False)

        # remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # set desired number of ticks
        desired_ticks = 6
        ax.xaxis.set_major_locator(MaxNLocator(desired_ticks))
        ax.yaxis.set_major_locator(MaxNLocator(desired_ticks))

        # set ticks
        if idx == 8 or idx == 9:
            #ax.set_xlabel(delta, fontsize=20)
            ax.tick_params(axis='x', labelsize=24)
        else:
            ax.set_xticks([])

        if idx == 0 or idx == 2 or idx == 4 or idx == 6 or idx == 8:
            # ax.set_ylabel('% Pyloric', fontsize=16)
            ax.tick_params(axis='y', labelsize=24)
        else:
            ax.set_yticks([])

        ax.set_xlim([0, 10.2])
        ax.set_ylim([0, 103])
        # ax.legend(loc='upper right')
        # Set border thickness for all sides of the subplot
        for spine in ax.spines.values():
            spine.set_linewidth(2)  # Set border thickness to 2 points
###############

    # Adjust layout
    plt.tight_layout()
    fig.subplots_adjust(wspace=0.07)
    # # Show the plot
    plt.show()
    #
