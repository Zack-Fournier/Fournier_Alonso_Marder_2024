import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import seaborn as sns
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import matplotlib.patches as patches

# set root_folder
root_folder = 'C:/code_package'

# set modelname (choose a model from the model folder, do not include .txt in the name)
# Model 1 in Fig. 6: Model_A (int(250,250), syn(0.45,1.75))
# Model 2 in Fig. 6: edg461_model0 (int(200,175), syn(0.15,1.75))
modelname = 'edg461-model0'


# set conductance search range used (nS)
int_x = 200
int_y = 175
syn_x = 0.15
syn_y = 1.75

##################################################

# set range plots parameters
# number of conductances
n_cond = 34
# number of intervals
n = 100
# set conductance percent scale
z = 500
# find axis factor
f = z/(n-1)
# initialize data vector
n_combinations = (n ** 2)
print(n_combinations)


# index function
def index(i):
    if i in range(0, 9):
        return i
    elif i in range(9, 18):
        return range(40, 49)[i-9]
    elif i in range(18, 27):
        return range(80, 89)[i-18]
    elif i in range(27, 34):
        return range(120, 127)[i-27]
    raise Exception(f"Encountered funny number: {i}")

# provide conductance names
names = ['gNA_PD','gCaT_PD','gCaS_PD','gA_PD','gKCa_PD','gKd_PD','gH_PD','gLeak_PD','gIMI_PD','gNA_LP','gCaT_LP','gCaS_LP','gA_LP','gKCa_LP','gKd_LP','gH_LP','gLeak_LP','gIMI_LP','gNA_PY','gCaT_PY','gCaS_PY','gA_PY','gKCa_PY','gKd_PY','gH_PY','gLeak_PY','gIMI_PY','PDPY_glut','PDPY_chol','PDLP_glut','PDLP_chol','LPPY_glut','PYLP_glut','LPPD_glut']
t_labels = ['PD gNa','PD gCaT','PD gCaS','PD gA','PD gKCa','PD gKd','PD gH','PD gLeak','PD gIMI','LP gNa','LP gCaT','LP gCaS','LP gA','LP gKCa','LP gKd','LP gH','LP gLeak','LP gIMI','PY gNa','PY gCaT','PY gCaS','PY gA','PY gKCa','PY gKd','PY gH','PY gLeak','PY gIMI','PD to PY','PD to PY cholinergic','PD to LP','PD to LP','LP to PY glutamatergic','PY to LP glutamatergic','LP to PD glutamatergic']
ax_labels = ['PD gNa','PD gCaT','PD gCaS','PD gA','PD gKCa','PD gKd','PD gH','PD gLeak','PD gIMI','LP gNa','LP gCaT','LP gCaS','LP gA','LP gKCa','LP gKd','LP gH','LP gLeak','LP gIMI','PY gNa','PY gCaT','PY gCaS','PY gA','PY gKCa','PY gKd','PY gH','PY gLeak','PY gIMI','PD to PY','PD to PY','PD to LP','PD to LP','LP to PY','PY to LP','LP to PD']

# import model for conductance reference
model = np.genfromtxt(root_folder + '/models/'+modelname+'.txt')

# conductance indices used in paper:
# i_s = [0, 9, 18, 30, 29, 29]
# j_s = [5, 14, 23, 28, 32, 33]
i_s = [0, 9, 18, 30, 29, 29]
j_s = [5, 14, 23, 28, 32, 33]

# set font
plt.rcParams['font.family'] = 'Calibri'

# create figures
fig, axs = plt.subplots(2, 3, figsize=(15, 10), dpi=300)

for z in range(len(i_s)):
    # index toggle
    i_index = i_s[z]
    j_index = j_s[z]

    # import range data
    data = pd.read_csv(root_folder + '/range_data/range_data_' + modelname + '_' + str(names[i_index]) + 'v' + str(names[j_index]) + '_g_100v100_.csv', index_col=False)
    data = np.array(data)

    # order is c, classification, i, j, x, y
    matrix = []
    for c in range(n_combinations):

        r = int(data[c,1])
        i = int(data[c,2])
        j = int(data[c,3])
        x = int(data[c,4])
        y = int(data[c,5])

        if i == i_index and j == j_index:

            # enlarge to 0 to z percent scale
            x = x*f
            y = y*f

            row = [x, y, r]
            matrix.append(row)

    dataframe = pd.DataFrame(matrix, columns=['x','y','r'])

    matrix_array = dataframe.pivot_table(index='y', columns='x', values='r', aggfunc='first')
    matrix_array = matrix_array.to_numpy()

    # Mapping dictionary for label replacement
    label_map = {1: 'not pyloric', 2: 'pyloric'}

    # Replace the values in the 'r' column with the mapped labels
    dataframe['r'] = dataframe['r'].replace(label_map)

    white = (1,1,1)
    dark_grey = (0.5, 0.5, 0.5)
    grey = (0.8, 0.8, 0.8)
    blue = (0.196, 0.427, 0.659)
    red = (0.72, 0.125, 0.145)

    if z <= 2:
        color1 = grey
        color2 = blue

    if z > 2:
        color1 = grey
        color2 = red

    # Create a custom colormap with two colors
    custom_cmap = ListedColormap([color1, color2])

    # Plot the matrix using imshow with interpolation='nearest'
    ax = axs[z // 3, z % 3]
    print(i_index, j_index)
    ax.imshow(matrix_array, cmap=custom_cmap, interpolation='nearest', origin='lower')
    ax.set_xticks([])
    ax.set_yticks([])
    # Set labels and title
    ax.set_xlabel(str(ax_labels[i_index])+' [nS]', fontsize=18)
    ax.set_ylabel(str(ax_labels[j_index])+' [nS]', fontsize=18)
    label = str(t_labels[i_index])+' vs. '+str(t_labels[j_index])
    ax.set_title(label, fontsize=20)

    condx = model[index(i_index)]
    condy = model[index(j_index)]

    if z == 3:

        print(condx, condy)

    # Plot an X at point (100, 100)
    if z < 3:
        x = 0
        y = 0
        sizex = 2*n*(condx/int_x)
        sizey = 2*n*(condy/int_y)


    if z > 2:
        x = 0
        y = 0
        sizex = 2*n*(condx/syn_x)
        sizey = 2*n*(condy/syn_y)


    # Create a rectangle patch
    rect = patches.Rectangle((x, y), sizex, sizey, linewidth=4, edgecolor=white, facecolor='none', linestyle='solid')

    # Add the rectangle patch to the plot
    ax.add_patch(rect)

    # Plot an X at point (100, 100)
    if z < 3:
        ax.plot(n*(condx/int_x), n*(condy/int_y), marker='x', color='white', markersize=20, markeredgewidth=6)

    if z > 2:
        ax.plot(n*(condx/syn_x), n*(condy/syn_y), marker='x', color='white', markersize=20, markeredgewidth=6)

# Display and save
plt.tight_layout()
plt.show()

