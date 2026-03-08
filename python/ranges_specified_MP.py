import numpy as np
import pandas as pd
import os
from integrate_and_plot_pyloric_imi_temp import *
from pyloricMeasures import *
from ancillary_functions import *
from sklearn.ensemble import RandomForestClassifier
import pickle
from multiprocessing import Pool
import uuid  # For generating unique filenames
import math

# set root folder
root_folder = 'C:/code_package'

# choose model to test
# Model 1 in Fig. 6: Model_A.txt (int(250,250), syn(0.45,1.75))
# Model 2 in Fig. 6: edg461_model0.txt (int(200,175), syn(0.15,1.75))
a = root_folder + '/models/edg461_model0.txt'

# set conductance search range used (nS)
int_x = 200
int_y = 175
syn_x = 0.15
syn_y = 1.75


#####################################################

# conductance indices used in paper:
# i_s = [0, 9, 18, 30, 29, 29]
# j_s = [5, 14, 23, 28, 32, 33]
i_s = [0,9,18,30,29,29]
j_s = [5,14,23,28,32,33]

# number of conductances
n_cond = 34

# number of intervals
n = 100

# import model and set simulation parameters
temp = 25
nsecs = 10
nsecs_sim = 5
pathtojava = root_folder + '/java/celltemp.jar'
pathtoci = root_folder + '/initial_conditions_and_parameters/cis_network_imi.txt'

# import classifier
with open(root_folder + "/python/classifier.pkl", "rb") as f:
    rfc = pickle.load(f)

# index function
def process_data(i, j, x, y, A_original):

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


    A = np.copy(A_original)  # reset conductance values to starting conductance
    # get conductance indices
    i_index = index(i)
    j_index = index(j)
    A[i_index] = xvalues[x]
    A[j_index] = yvalues[y]

    # Generate unique filenames for dumping and retrieving
    unique_id = uuid.uuid4().hex
    modelloc = root_folder + '/range_dump' + '/range_parameters_' + unique_id + '.txt'
    tempdump = root_folder + '/range_parameters' + '/range_dump_' + unique_id + '.txt'

    savetxt(modelloc, A)

    excommand = 'java -cp ' + pathtojava + ' tempComp.integratePyloricNetwork_temp_imi_realclean_rk4 ' + pathtoci + ' ' + modelloc
    command = excommand + ' ' + str(nsecs) + ' ' + str(temp) + ' 0.1 ' + ' > ' + tempdump + ' '
    os.system(command)

    sol = np.genfromtxt(tempdump)
    sol = truncate_solution(sol, nsecs, nsecs_sim)

    features = feature_finder(sol)
    features = np.array(features)
    print(features[0])
    feats = features.reshape(1, -1)
    classification = rfc.predict(feats)
    os.remove(modelloc)
    os.remove(tempdump)

    l = str(i) + '-' + str(j) + '-' + str(x) + '-' + str(y)
    print(l)
    print(classification)
    return [classification[0], i, j, x, y]


names = ['gNa_PD','gCaT_PD','gCaS_PD','gA_PD','gKCa_PD','gKd_PD','gH_PD','gLeak_PD','gIMI_PD','gNa_LP','gCaT_LP','gCaS_LP','gA_LP','gKCa_LP','gKd_LP','gH_LP','gLeak_LP','gIMI_LP','gNa_PY','gCaT_PY','gCaS_PY','gA_PY','gKCa_PY','gKd_PY','gH_PY','gLeak_PY','gIMI_PY','PDPY_glut','PDPY_chol','PDLP_glut','PDLP_chol','LPPY_glut','PYLP_glut','LPPD_glut']


modelname = os.path.basename(a)
modelname = modelname[:-4]
A_original = np.genfromtxt(a)  # model starting parameters

for z in range(len(i_s)):
    # index toggle
    i = i_s[z]
    j = j_s[z]

    # set ranges
    if z < 3:  # intrinsic ranges
        xvalues = np.linspace(0, int_x, n)
        yvalues = np.linspace(0, int_y, n)

    if z > 2:  # synaptic ranges
        xvalues = np.linspace(0, syn_x, n)
        yvalues = np.linspace(0, syn_y, n)

    # set counter for data collection
    c = 0

    # initialize data vector
    n_combinations = (n ** 2)
    print(n_combinations)
    data = np.zeros([n_combinations, 6])  # 6 columns, n rows

    if __name__ == '__main__':
        # extract conductance values
        with Pool() as pool:
            for result in pool.starmap(process_data, [(i, j, x, y, A_original) for x in range(n) for y in range(n)]):

                #print(result)
                data[c, 0] = c
                data[c, 1] = result[0]
                data[c, 2] = result[1]
                data[c, 3] = result[2]
                data[c, 4] = result[3]
                data[c, 5] = result[4]
                c += 1

        print(data)
        data = pd.DataFrame(data)
        data.to_csv(root_folder+'/range_data/range_data_' + modelname + '_' + str(names[i])+'v'+str(names[j])+'_g_100v100_.csv', index=False)
