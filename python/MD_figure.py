import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import glob
import matplotlib.ticker as ticker
import matplotlib.patches as patches
from scipy.stats import kstest, shapiro
from matplotlib.ticker import MaxNLocator

# set root_folder
root_folder = 'C:/code_package'

# import model features
features = pd.read_csv(root_folder + '/analytics/MD_features.csv')


files = ['dof948-model5', 'edg461-model64', 'qla777-model76', 'wcz837-model53', 'gjd842-model16', 'edg461-model0', 'wcz837-model48', 'qla777-model4', 'gjd842-model11', 'Model_A', 'dof948-model0', 'dof948-model11', 'dof948-model17', 'dof948-model26', 'dof948-model45', 'dof948-model36', 'dof948-model47', 'dof948-model49', 'dof948-model30', 'edg461-model2', 'edg461-model59', 'edg461-model16', 'edg461-model17', 'edg461-model20', 'edg461-model25', 'edg461-model28', 'edg461-model32', 'edg461-model38', 'edg461-model40', 'edg461-model45', 'edg461-model47', 'edg461-model50', 'edg461-model53', 'edg461-model55', 'edg461-model58', 'edg461-model60', 'edg461-model61', 'gjd842-model0', 'gjd842-model3', 'gjd842-model5', 'gjd842-model7', 'gjd842-model8', 'gjd842-model10', 'gjd842-model12', 'gjd842-model31', 'gjd842-model37', 'gjd842-model41', 'gjd842-model53', 'gjd842-model57', 'gjd842-model68', 'gjd842-model69', 'gjd842-model72', 'gjd842-model77', 'gjd842-model78', 'gjd842-model80', 'qla777-model0', 'qla777-model1', 'qla777-model2', 'qla777-model3', 'qla777-model7', 'qla777-model12', 'qla777-model13', 'qla777-model16', 'qla777-model25', 'qla777-model29', 'qla777-model32', 'qla777-model34', 'qla777-model35', 'qla777-model37', 'qla777-model38', 'qla777-model39', 'qla777-model75', 'qla777-model77', 'ssc-0.1-model1', 'ssc-0.1-model3', 'ssc-0.1-model6', 'ssc-0.1-model10', 'ssc-0.1-model11', 'ssc-0.1-model16', 'ssc-0.1-model26', 'ssc-0.1-model30', 'ssc-0.1-model38', 'wcz837-model0', 'wcz837-model2', 'wcz837-model6', 'wcz837-model10', 'wcz837-model12', 'wcz837-model16', 'wcz837-model21', 'wcz837-model24', 'wcz837-model28', 'wcz837-model29', 'wcz837-model32', 'wcz837-model35', 'wcz837-model40', 'wcz837-model46', 'wcz837-model52', 'wcz837-model61', 'wcz837-model62', 'wcz837-model64']

# c_files = glob.glob(c+'*')
c_params=[]
for fname in files:
    fname = root_folder + '/models/' + fname + '.txt'
    c_params.append(np.genfromtxt(fname))
allparams = []
allparams.append(c_params)
all_params = [item for sublist in allparams for item in sublist]
conductances = pd.DataFrame(all_params)

# get PD gA, PDPY_glut
gA_PD = [sublist[3] for sublist in all_params]
PDPY_glut = [sublist[120] for sublist in all_params]

# conductances TSNE
gtsne = TSNE(n_components=2, perplexity=20, random_state=42)
g_tsne = gtsne.fit_transform(conductances)

# features TSNE
ftsne = TSNE(n_components=2, perplexity=20, random_state=42)
features = features.drop(columns=['filenames'])
f_tsne = ftsne.fit_transform(features)

# create figure
plt.rcParams['font.family'] = 'Calibri'
fig, axs = plt.subplots(2, 3, figsize=(12, 8), dpi=300)
fig.subplots_adjust(hspace=0.3, wspace=0.4)
grey = 'grey'
red = (0.72, 0.125, 0.145)
green = (0.357, 0.64, 0)
pink = (0.9, 0.19, 0.54)
dark_pink = (0.71, 0.098, 0.388)
orange = (0.961, 0.463, 0)
dark_orange = (0.769, 0.275, 0.004)
light_blue = (0.545, 0.671, 0.945)
blue = (0, 0.451, 0.902)
dark_blue = (0.0196, 0.31, 0.726)
#shading colors
shaded_green = (0.357, 0.64, 0, 0.5)
shaded_grey = (0.5, 0.5, 0.5, 0.5)
shaded_orange = (0.961, 0.463, 0, 0.5)
shaded_blue = (0, 0.451, 0.902, 0.5)
# set gA PD histogram
axs[0, 0].hist(gA_PD, bins=10, color=orange, edgecolor='black')
formatter = ticker.StrMethodFormatter('{x:.0f}')
axs[0, 0].xaxis.set_major_formatter(formatter)
axs[0, 0].set_ylim([0,23])
# set PDPY histogram
axs[0, 1].hist(PDPY_glut, bins=10, color=orange, edgecolor='black')
x = PDPY_glut
formatter1 = ticker.FuncFormatter(lambda x, _: '{:.1f}'.format(x) if 0 < x < 1 else '{:.0f}'.format(x))
axs[0, 1].xaxis.set_major_formatter(formatter1)
axs[0, 1].set_ylim([0,23])
# set LP DC histogram
axs[1, 0].hist(features['LPdc_m'], bins=10, color=blue, edgecolor='black')
axs[1, 0].set_ylim([0,23])
# set LP ON/OFF histogram
axs[1, 1].hist(features['LPon'], bins=10, color=blue, edgecolor='black')
axs[1, 1].set_ylim([0,23])
# axs[1, 1].hist(features['LPoff'], bins=10, color='black', edgecolor=grey)
# plot conductance TSNE
axs[0, 2].scatter(g_tsne[:, 0], g_tsne[:, 1], marker='o', edgecolor='black', color=orange)
desired_ticks = 3
axs[0, 2].yaxis.set_major_locator(MaxNLocator(desired_ticks))
# plot feature TSNE
axs[1, 2].scatter(f_tsne[:, 1], f_tsne[:, 0], marker='o', edgecolor='black', color=blue)
desired_ticks = 3
axs[1, 2].yaxis.set_major_locator(MaxNLocator(desired_ticks))


for i in range(2):
    for j in range(3):

        ax = axs[i, j]
        ax.tick_params(axis='x', labelsize=16)
        ax.tick_params(axis='y', labelsize=16)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
plt.show()

