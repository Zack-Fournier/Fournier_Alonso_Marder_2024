import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import ast
from scipy.stats import linregress
from scipy.stats import ttest_ind, shapiro
from matplotlib.ticker import MaxNLocator
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# set root folder
root_folder = 'C:/code_package'

###############################################

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

# print(IC_curves)
plt.rcParams['font.family'] = 'Calibri'


# get IC avg
IC_vals = []
for index, row in IC_curves.iterrows():

    # extract curve
    row['curves'] = row['curves'].replace('. ', ',')
    curves = np.array(ast.literal_eval(row['curves']))
    curves = curves.astype(int)
    curves = curves / n * 100

    IC_vals.append(curves)

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
IC_stacked = np.stack(IC_vals)
SC_stacked = np.stack(SC_vals)


# # Add 'identity' column to IC_curves and SC_curves DataFrames
IC_curves['identity'] = 'IC'
SC_curves['identity'] = 'SC'

# Combine the data
data = pd.concat([IC_curves, SC_curves])
print(data['identity'])

# Extract curves and stack arrays
curves_vals = []
identity = []
for index, row in data.iterrows():
    # Fix the string representation of the array
    curves_str = row['curves'].replace('. ', ', ')  # Add comma and space between elements
    curves = np.array(ast.literal_eval(curves_str))
    curves = curves.astype(int)
    curves = curves / n * 100
    # curves = np.gradient(curves)
    curves_vals.append(curves)
    identity.append(row['identity'])

# Stack arrays
curves_stacked = np.stack(curves_vals)
identity_stacked = np.stack(identity)
print(curves_stacked[0])


# Perform PCA
pca = PCA(n_components=1)
pca_components = pca.fit_transform(curves_stacked)

ppal_component_vector = pca.components_[0]
print('ppal: ', ppal_component_vector)

######## PCA TEST

# Extract eigenvectors and eigenvalues
eigenvectors = pca.components_
eigenvalues = pca.explained_variance_

# Print eigenvectors and eigenvalues
print("Eigenvectors:")
print(eigenvectors)
print("\nEigenvalues:")
print(eigenvalues)


reconstructed_data = np.dot(pca_components, eigenvectors) + pca.mean_
print(reconstructed_data[0])

print('intrinsic PPAL', pca_components[0, 0])
print('synaptic PPAL', pca_components[100, 0])


t_statistic_pca, p_value_pca = ttest_ind(pca_components[100:199, 0], pca_components[0:99, 0])
statistic_IC_pca, p_value_IC_pca = shapiro(pca_components[0:99, 0])
statistic_SC_pca, p_value_SC_pca = shapiro(pca_components[100:199, 0])

print('PCA', p_value_pca)
print('IC_PCA', p_value_IC_pca)
print('SC_PCA', p_value_SC_pca)

########
bins = 20
plt.figure(6)
PCA1 = pd.DataFrame({'Values': pca_components[100:199, 0].tolist() + pca_components[0:99, 0].tolist(),
                       'Group': ['Synaptic'] * len(pca_components[100:199, 0]) + ['Intrinsic'] * len(pca_components[0:99, 0])})

# Create figure 2
plt.figure(2, dpi=300)

# Create a histogram
sns.histplot(data=PCA1, x='Values', hue='Group', palette=[red, blue], kde=False, bins=bins, alpha=1, legend=False)

# Labeling and styling
plt.xlabel('')
plt.ylabel('')
plt.tick_params(axis='both', labelsize=14)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.tight_layout()
plt.show()
# # Store the explained variance ratios in variables
explained_variance_ratio = pca.explained_variance_ratio_
#
# Print the percentage of variance explained by each component
print("Explained Variance Ratio for Each Component:")
for i, ratio in enumerate(pca.explained_variance_ratio_):
    print(f"Component {i+1}: {ratio:.2%}")

plt.show()