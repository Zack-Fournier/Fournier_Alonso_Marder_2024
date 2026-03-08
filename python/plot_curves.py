import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import trapz
from matplotlib.ticker import MaxNLocator

# set known data parameters

# set root folder
root_folder = 'C:/code_package'

# set modelname
# modelname = 'Model_A'
modelname = 'Model_A'

# trial number: MAKE SURE TO INPUT THE EXACT NUMBER OF TRIALS YOU RAN
n = 100

########################################

# delta
d = ['0','10','20','30','40','50','60','70','80','90','100']

rfc_wholelab_accuracy = 95
#
rfc_wholelab_error = 100 - rfc_wholelab_accuracy


# import classifications
IC_wholelab_rfc = pd.read_csv(root_folder+'/SA/'+modelname+'_IC.csv')
SC_wholelab_rfc = pd.read_csv(root_folder+'/SA/'+modelname+'_SC.csv')

# clear unnamed columns
IC_wholelab_rfc = IC_wholelab_rfc.loc[:, ~IC_wholelab_rfc.columns.str.contains('^Unnamed')]
SC_wholelab_rfc = SC_wholelab_rfc.loc[:, ~SC_wholelab_rfc.columns.str.contains('^Unnamed')]

# compress classifications
IC_wholelab_classes_rfc = np.zeros([len(d)])
SC_wholelab_classes_rfc = np.zeros([len(d)])

for i in range(len(d)):

    IC_wholelab_classes_rfc[i] = (IC_wholelab_rfc.iloc[:, i] == 2).sum()
    SC_wholelab_classes_rfc[i] = (SC_wholelab_rfc.iloc[:, i] == 2).sum()

# plotting attributes
darker_pink = (1.0, 0.4, 0.6)
delta = "\u03B4"
set = "\u2208"

plt.figure(1)
blue = (0.196, 0.427, 0.659)
red = (0.72, 0.125, 0.145)
plt.plot(d, 100*IC_wholelab_classes_rfc/n, label=('$\ Intrinsic$'), color=blue, lw=7, zorder=2)
plt.plot(d, 100*SC_wholelab_classes_rfc/n, label=('$\ Synaptic$'), color=red, lw=7, zorder=1)
plt.title(modelname, fontsize=16, y=1.05, x=0.5)
plt.xlabel(delta, fontsize=16)
plt.ylabel('% Pyloric', fontsize=16)
# remove spines
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# set desired number of ticks
desired_ticks = 6
plt.gca().xaxis.set_major_locator(MaxNLocator(desired_ticks))
plt.gca().yaxis.set_major_locator(MaxNLocator(desired_ticks))
plt.gca().set_xlim([0, 10.2])
plt.gca().set_ylim([0, 106])
plt.tick_params(axis='y', labelsize=14)
plt.tick_params(axis='x', labelsize=14)
plt.legend(loc='lower left', fontsize=16)

# Get the current axes
ax = plt.gca()

plt.tight_layout()
plt.show()
plt.close()

# Calculate the difference between the two lines
difference = (IC_wholelab_classes_rfc - SC_wholelab_classes_rfc)/n
# Calculate the integral using the trapezoidal rule
area_under_curve = trapz(difference, dx=(1 / (len(d) - 1)))

# Print the result
print("Integral between the two lines:", area_under_curve)


