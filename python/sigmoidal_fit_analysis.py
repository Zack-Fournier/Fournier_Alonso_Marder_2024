import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ast
from scipy.stats import linregress
from scipy.stats import ttest_ind, shapiro, kstest
from matplotlib.ticker import MaxNLocator, FuncFormatter

# set root_folder
root_folder = 'C:/code_package'

####################################

# import curves
IC_curves = pd.read_csv(root_folder + '/analytics/IC_curves.csv')
SC_curves = pd.read_csv(root_folder + '/analytics/SC_curves.csv')

# set trial number
n = 1000

# set d for printing
d = ['0','10','20','30','40','50','60','70','80','90','100']

# set colors
blue = (0.196, 0.427, 0.659)
red = (0.72, 0.125, 0.145)

# choose sample curve
s = 8

# set bin number
bins = 20

# define sigmoid function
def Sigmoid(x,a,b,c):
    #c = 1000.
    #a = -0.1
    #b = 0.5
    y = c * (1. / (1 + np.exp(-(x - b) / a)))
    return y

# define error function
def error(a,b,c,x,y):
    fit = Sigmoid(x,a,b,c)
    error = sum((fit-y)**2)
    return error

# set font
plt.rcParams['font.family'] = 'Calibri'

# Fit and plot IC CURVES
IC_a_values = []
IC_b_values = []
IC_error = []
IC_r = []
count = 0
for index, row in IC_curves.iterrows():

    # extract filename
    filename = row['filename']
    filename = filename[:-4]
    # extract curve
    row['curves'] = row['curves'].replace('. ', ',')
    curves = np.array(ast.literal_eval(row['curves']))
    curves = curves.astype(int)
    curves = curves/n*100
    # set delta
    x = np.linspace(0, 1, 11)
    x = np.round(x, decimals=1)
    # rename data arrays
    x = np.array(x)
    y = np.array(curves)
    # set b and c parameters (c is static for 100% and b is dynamic based on mean (in decimals))
    c = 100
    # find best a b value
    a_vals = np.linspace(-0.5,-0.01,100)
    b_vals = np.linspace(0, 2, 100)
    errors = np.zeros([100, 100])
    A = 0
    B = 0
    for b in b_vals:
        for a in a_vals:
            errors[A, B] = (error(a,b,c,x,y))
            A = A + 1  # advance A index
        B = B + 1  # advance B index
        A = 0  # reset A index
    min_index = np.unravel_index(np.argmin(errors, axis=None), errors.shape)
    a_best = a_vals[min_index[0]]
    b_best = b_vals[min_index[1]]
    IC_a_values.append([filename, a_best])
    IC_b_values.append([filename, b_best])
    IC_error.append(np.sqrt(errors[min_index])/11)
    # fit and plot on the specific subplot for IC curves
    fit_ic = Sigmoid(x, a_best, b_best, c)
    correlation_matrix = np.corrcoef(fit_ic, y)
    correlation_coefficient = correlation_matrix[0, 1]
    IC_r.append(correlation_coefficient**2)

    # sample plot
    if count == s:
        plt.figure(5, dpi=300)
        plt.plot(d, y, label='Intrinsic', zorder=6, color=blue, lw=7)
        plt.scatter(d, y, color=blue, zorder=6, s=150, clip_on=False)
        plt.plot(d, fit_ic, zorder=7, color='black', ls='--', lw=4)
        plt.tick_params(axis='y', labelsize=14)
        plt.tick_params(axis='x', labelsize=14)
        plt.gca().set_xlim([0, 10.2])
        plt.gca().set_ylim([0, 103])
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        desired_ticks = 6
        plt.gca().xaxis.set_major_locator(MaxNLocator(desired_ticks))
        plt.gca().yaxis.set_major_locator(MaxNLocator(desired_ticks))
    # counter
    count = count + 1


# Fit and plot SC CURVES
SC_a_values = []
SC_b_values = []
SC_error = []
SC_r = []
count = 0
for index, row in SC_curves.iterrows():

    # extract filename
    filename = row['filename']
    filename = filename[:-4]
    # extract curve
    row['curves'] = row['curves'].replace('. ', ',')
    curves = np.array(ast.literal_eval(row['curves']))
    curves = curves.astype(int)
    curves = curves/n*100
    # set delta
    x = np.linspace(0, 1, 11)
    x = np.round(x, decimals=1)
    # rename data arrays
    x = np.array(x)
    y = np.array(curves)
    # set b and c parameters (c is static for 100% and b is dynamic based on mean (in decimals))
    c = 100
    # find best a b value
    a_vals = np.linspace(-0.5,-0.01,100)
    b_vals = np.linspace(0, 2, 100)
    errors = np.zeros([100, 100])
    A = 0
    B = 0
    for b in b_vals:
        for a in a_vals:
            errors[A, B] = (error(a, b, c, x, y))
            A = A + 1  # advance A index
        B = B + 1  # advance B index
        A = 0  # reset A index

    min_index = np.unravel_index(np.argmin(errors, axis=None), errors.shape)
    a_best = a_vals[min_index[0]]
    b_best = b_vals[min_index[1]]
    SC_a_values.append([filename, a_best])
    SC_b_values.append([filename, b_best])
    SC_error.append(np.sqrt(errors[min_index])/11)
    # fit and plot on the specific subplot for SC curves
    fit_sc = Sigmoid(x, a_best, b_best, c)
    correlation_matrix = np.corrcoef(fit_sc, y)
    correlation_coefficient = correlation_matrix[0, 1]
    SC_r.append(correlation_coefficient**2)

    # sample plot
    if count == s:
        plt.figure(5, dpi=300)
        plt.plot(d, y, label='Synaptic', zorder=5, color=red, lw=7)
        plt.scatter(d, y, color=red, zorder=5, s=150, clip_on=False)
        plt.plot(d, fit_sc, zorder=7, color='black', ls='--', lw=4)
        plt.tick_params(axis='y', labelsize=14)
        plt.tick_params(axis='x', labelsize=14)
        plt.gca().set_xlim([0, 10.2])
        plt.gca().set_ylim([0, 103])
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        desired_ticks = 6
        plt.gca().xaxis.set_major_locator(MaxNLocator(desired_ticks))
        plt.gca().yaxis.set_major_locator(MaxNLocator(desired_ticks))
        plt.tight_layout()

    # counter
    count = count + 1


# create dataframes
IC_a_values = pd.DataFrame(IC_a_values, columns=['filename','a'])
IC_b_values = pd.DataFrame(IC_b_values, columns=['filename','b'])
SC_a_values = pd.DataFrame(SC_a_values, columns=['filename','a'])
SC_b_values = pd.DataFrame(SC_b_values, columns=['filename','b'])
IC_error = pd.DataFrame(IC_error, columns=['error'])
SC_error = pd.DataFrame(SC_error, columns=['error'])
IC_rsq = pd.DataFrame(IC_r, columns=['rsq'])
SC_rsq = pd.DataFrame(SC_r, columns=['rsq'])

# t-tests of midpoint and width parameters
statistic_IC_a, p_value_IC_a = shapiro(IC_a_values['a'])
statistic_SC_a, p_value_SC_a = shapiro(SC_a_values['a'])
statistic_IC_b, p_value_IC_b = shapiro(IC_b_values['b'])
statistic_SC_b, p_value_SC_b = shapiro(SC_b_values['b'])
t_statistic_a, p_value_a = ttest_ind(IC_a_values['a'], SC_a_values['a'])
t_statistic_b, p_value_b = ttest_ind(IC_b_values['b'], SC_b_values['b'])
t_statistic_error, p_value_error = ttest_ind(IC_error['error'], SC_error['error'])
print('P value of Width Parameter = '+str(p_value_a))
print('P value of Midpoint Parameter = '+str(p_value_b))
print('P value of error = '+str(p_value_error))
print('S_IC_a', p_value_IC_a)
print('S_SC_a', p_value_SC_a)
print('S_IC_b', p_value_IC_b)
print('S_SC_b', p_value_SC_b)


print('IC width mean', np.mean(IC_a_values['a']))
print('SC width mean', np.mean(SC_a_values['a']))

# width parameter
data_a = pd.DataFrame({'Values': SC_a_values['a'].tolist() + IC_a_values['a'].tolist(),
                     'Group': ['Synaptic'] * len(SC_a_values['a']) + ['Intrinsic'] * len(IC_a_values['a'])})

# # Create figure
plt.figure(1, dpi=300)

# # Create a histogram
# sns.histplot(data=data_a, x='Values', hue='Group', palette=[red, blue], kde=False, bins=bins, alpha=1, legend=False)
#
# # Labeling and styling
# plt.xlabel('')
# plt.ylabel('')
# plt.ylim(0,30.5)
# plt.tick_params(axis='both', labelsize=14)
# plt.gca().spines['top'].set_visible(False)
# plt.gca().spines['right'].set_visible(False)
# desired_ticks = 4
# plt.gca().xaxis.set_major_locator(MaxNLocator(desired_ticks))
# plt.gca().yaxis.set_major_locator(MaxNLocator(7))
# plt.tight_layout()

##################

# Separate the data based on 'Group'
synaptic_data = data_a[data_a['Group'] == 'Synaptic']['Values']
intrinsic_data = data_a[data_a['Group'] == 'Intrinsic']['Values']

# Determine common bin edges for both distributions
combined_values = pd.concat([synaptic_data, intrinsic_data])
bin_edges = np.histogram_bin_edges(combined_values, bins=bins)

# Create subplots with the Intrinsic plot on top
fig, (ax2, ax1) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))

# Plot the Intrinsic data (blue) on the top plot
sns.histplot(intrinsic_data, bins=bin_edges, color=blue, kde=False, alpha=1, ax=ax2, legend=False, linewidth=2)
ax2.set_ylim(0, 30.5)  # Adjust for the y-values
ax2.set_ylabel('')

# Plot the Synaptic data (red) on the bottom plot
sns.histplot(synaptic_data, bins=bin_edges, color=red, kde=False, alpha=1, ax=ax1, legend=False, linewidth=2)
ax1.set_ylim(0, 30.5)  # Adjust for the y-values
ax1.set_ylabel('')

# Shared x-axis labeling and styling
ax1.set_xlabel('')
ax1.tick_params(axis='both', labelsize=22)
ax2.tick_params(axis='both', labelsize=22)

# Adjust the x-axis to show the same ticks on both plots
ax1.xaxis.set_major_locator(MaxNLocator(4))
ax1.yaxis.set_major_locator(MaxNLocator(3))
ax2.yaxis.set_major_locator(MaxNLocator(3))

# Remove top and right spines
for ax in [ax1, ax2]:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
##################

# Adjust layout
plt.tight_layout()

# Show plot
plt.show()
##################


# midpoint parameter
data_b = pd.DataFrame({'Values': SC_b_values['b'].tolist() + IC_b_values['b'].tolist(),
                       'Group': ['Synaptic'] * len(SC_b_values['b']) + ['Intrinsic'] * len(IC_b_values['b'])})

# Create figure 2
plt.figure(2, dpi=300)

# Create a histogram
sns.histplot(data=data_b, x='Values', hue='Group', palette=[red, blue], kde=False, bins=bins, alpha=1, legend=False)

# Labeling and styling
plt.xlabel('')
plt.ylabel('')
plt.tick_params(axis='both', labelsize=14)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()


####### ERROR DISTRIBUTION
data_error = pd.DataFrame({'Values': SC_error['error'].tolist() + IC_error['error'].tolist(),
                       'Group': ['Synaptic'] * len(SC_error['error']) + ['Intrinsic'] * len(IC_error['error'])})

print('IC error mean', np.mean(IC_error['error']))
print('SC error mean', np.mean(SC_error['error']))

# Create error figure
plt.figure(10, dpi=300)

# Create a histogram
sns.histplot(data=data_error, x='Values', hue='Group', palette=[red, blue], kde=False, bins=bins, alpha=1, legend=False)

# Labeling and styling
plt.xlabel('Fit error', fontsize=18)
plt.ylabel('Count', fontsize=18)

plt.tick_params(axis='both', labelsize=14)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)


plt.tight_layout()
plt.show()

folder = 'C:/Python/Sensitivity_Analysis/network_code_for_zack'
IC_a_values.to_csv(folder+'/IC_a_values.csv')
IC_b_values.to_csv(folder+'/IC_b_values.csv')
SC_a_values.to_csv(folder+'/SC_a_values.csv')
SC_b_values.to_csv(folder+'/SC_b_values.csv')

