import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ast
from scipy.stats import linregress
from scipy.stats import ttest_ind, shapiro
from matplotlib.ticker import MaxNLocator

# set root_folder
root_folder = 'C:/code_package'


# import curves
IC_curves = pd.read_csv(root_folder + '/analytics/IC_curves.csv')
SC_curves = pd.read_csv(root_folder + '/analytics/SC_curves.csv')

# set trial number
n = 1000

# get IC avg
IC_vals = []
for index, row in IC_curves.iterrows():

    # extract curve
    row['curves'] = row['curves'].replace('. ', ',')
    curves = np.array(ast.literal_eval(row['curves']))
    curves = curves.astype(int)
    curves = curves / n * 100

    IC_vals.append(curves)

# stack arrays
IC_stacked = np.stack(IC_vals)

# calculate mean IC curve
IC_avg = np.mean(IC_stacked, axis=0)
IC_SE = np.std(IC_stacked, axis=0)/10

# SC svg
SC_vals = []
for index, row in SC_curves.iterrows():

    # extract curve
    row['curves'] = row['curves'].replace('. ', ',')
    curves = np.array(ast.literal_eval(row['curves']))
    curves = curves.astype(int)
    curves = curves / n * 100

    SC_vals.append(curves)

# stack arrays
SC_stacked = np.stack(SC_vals)

# calculate mean IC curve
SC_avg = np.mean(SC_stacked, axis=0)
SC_SE = np.std(SC_stacked, axis=0)/10

print(SC_avg)

# plot figure
d = ['0','10','20','30','40','50','60','70','80','90','100']
print(d)
n = 1000
rfc_wholelab_accuracy = 97
rfc_wholelab_error = 100 - rfc_wholelab_accuracy
blue = (0.196, 0.427, 0.659)
red = (0.72, 0.125, 0.145)
delta = "\u03B4"
set = "\u2208"
plt.rcParams['font.family'] = 'Calibri'
plt.figure(1, dpi=300)
plt.plot(d, SC_avg, label='Synaptic', color=red, lw=7)
plt.scatter(d, SC_avg, color=red, zorder=5, s=150, clip_on=False)

# Plot lines with shaded regions
plt.plot(d, IC_avg, label='Intrinsic', color=blue, lw=7)
plt.scatter(d, IC_avg, color=blue, zorder=5, s=150, clip_on=False)

# remove spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# set desired number of ticks
desired_ticks = 6
plt.gca().xaxis.set_major_locator(MaxNLocator(desired_ticks))
plt.gca().yaxis.set_major_locator(MaxNLocator(desired_ticks))

plt.gca().set_xlim([0, 10.2])
plt.gca().set_ylim([0, 103])

plt.tick_params(axis='y', labelsize=14)
plt.tick_params(axis='x', labelsize=14)

plt.tight_layout()
plt.show()


####################### CALCULATE AREAS

IC_areas = []
for index, row in IC_curves.iterrows():
    row['curves'] = row['curves'].replace('. ', ',')
    curves = np.array(ast.literal_eval(row['curves']))
    IC = curves.astype(int)
    # Calculate the integral of the intrinsic curve
    IC_trap_width = 1 / (len(100*IC/n) - 1)  # assumes spacing is uniform
    IC_area = np.trapz(100*IC/n, dx=IC_trap_width)
    IC_areas.append(IC_area)
IC_curves['area'] = IC_areas

# Calculate the integral of the synaptic curve
SC_areas = []
for index, row in SC_curves.iterrows():
    row['curves'] = row['curves'].replace('. ', ',')
    curves = np.array(ast.literal_eval(row['curves']))
    SC = curves.astype(int)
    # Calculate the integral of the synaptic curve
    SC_trap_width = 1 / (len(100*SC/n) - 1)  # assumes spacing is uniform
    SC_area = np.trapz(100*SC/n, dx=SC_trap_width)
    SC_areas.append(SC_area)
SC_curves['area'] = SC_areas

t_statistic_area, p_value_area = ttest_ind(IC_areas, SC_areas)
statistic_IC_area, p_value_IC_area = shapiro(IC_areas)
statistic_SC_area, p_value_SC_area = shapiro(SC_areas)

print('area', p_value_area)
print('IC_area', p_value_IC_area)
print('SC_area', p_value_SC_area)

##################################

data = pd.DataFrame({'Values': SC_curves['area'].tolist() + IC_curves['area'].tolist(),
                       'Group': ['Synaptic'] * len(SC_curves['area']) + ['Intrinsic'] * len(IC_curves['area'])})

# Create figure 2
plt.figure(2, dpi=300)

# Create a histogram
sns.histplot(data=data, x='Values', hue='Group', palette=[red, blue], kde=False, bins=20, alpha=1, legend=False)

# set desired number of ticks
desired_ticks = 6
plt.gca().xaxis.set_major_locator(MaxNLocator(desired_ticks))
plt.gca().yaxis.set_major_locator(MaxNLocator(desired_ticks))

# Labeling and styling
plt.xlabel('')
plt.ylabel('')
plt.ylim(0,30.5)
plt.tick_params(axis='both', labelsize=14)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.show()