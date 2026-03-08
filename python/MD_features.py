import numpy as np
import uuid
import os
import pandas as pd
from integrate_and_plot_pyloric_imi_temp import *
from pyloricMeasures import *
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import glob
import matplotlib.ticker as ticker
import matplotlib.patches as patches

# set root_folder
root_folder = 'C:/code_package'

###########
files = ['dof948-model5', 'edg461-model64', 'qla777-model76', 'wcz837-model53', 'gjd842-model16', 'edg461-model0', 'wcz837-model48', 'qla777-model4', 'gjd842-model11', 'Model_A', 'dof948-model0', 'dof948-model11', 'dof948-model17', 'dof948-model26', 'dof948-model45', 'dof948-model36', 'dof948-model47', 'dof948-model49', 'dof948-model30', 'edg461-model2', 'edg461-model59', 'edg461-model16', 'edg461-model17', 'edg461-model20', 'edg461-model25', 'edg461-model28', 'edg461-model32', 'edg461-model38', 'edg461-model40', 'edg461-model45', 'edg461-model47', 'edg461-model50', 'edg461-model53', 'edg461-model55', 'edg461-model58', 'edg461-model60', 'edg461-model61', 'gjd842-model0', 'gjd842-model3', 'gjd842-model5', 'gjd842-model7', 'gjd842-model8', 'gjd842-model10', 'gjd842-model12', 'gjd842-model31', 'gjd842-model37', 'gjd842-model41', 'gjd842-model53', 'gjd842-model57', 'gjd842-model68', 'gjd842-model69', 'gjd842-model72', 'gjd842-model77', 'gjd842-model78', 'gjd842-model80', 'qla777-model0', 'qla777-model1', 'qla777-model2', 'qla777-model3', 'qla777-model7', 'qla777-model12', 'qla777-model13', 'qla777-model16', 'qla777-model25', 'qla777-model29', 'qla777-model32', 'qla777-model34', 'qla777-model35', 'qla777-model37', 'qla777-model38', 'qla777-model39', 'qla777-model75', 'qla777-model77', 'ssc-0.1-model1', 'ssc-0.1-model3', 'ssc-0.1-model6', 'ssc-0.1-model10', 'ssc-0.1-model11', 'ssc-0.1-model16', 'ssc-0.1-model26', 'ssc-0.1-model30', 'ssc-0.1-model38', 'wcz837-model0', 'wcz837-model2', 'wcz837-model6', 'wcz837-model10', 'wcz837-model12', 'wcz837-model16', 'wcz837-model21', 'wcz837-model24', 'wcz837-model28', 'wcz837-model29', 'wcz837-model32', 'wcz837-model35', 'wcz837-model40', 'wcz837-model46', 'wcz837-model52', 'wcz837-model61', 'wcz837-model62', 'wcz837-model64']


# import classifier
with open(root_folder + "/python/rfc_wholelab_rfeat.pkl", "rb") as f:
    rfc = pickle.load(f)

all_features = []
for fname in files:
    modelloc = root_folder + '/models/' + fname + '.txt'

    print(fname)

    temp = 25
    nsecs = 10
    nsecs_sim = 5
    pathtojava = root_folder + '/java/model.jar'
    pathtoci = root_folder + '/initial_conditions_and_parameters/cis_network_imi.txt'


    # Generate filename
    tempdump = root_folder + '/model_solutions/' + fname + '_solution.txt'


    excommand = 'java -cp ' + pathtojava + ' tempComp.integratePyloricNetwork_temp_imi_realclean_rk4 ' + pathtoci + ' ' + modelloc
    command = excommand + ' ' + str(nsecs) + ' ' + str(temp) + ' 0.1 ' + ' > ' + tempdump + ' '
    os.system(command)

    sol = np.genfromtxt(tempdump)
    sol = truncate_solution(sol, nsecs, nsecs_sim)

    feats = feature_finder(sol)
    feats = list(feats)
    feats.insert(0, fname)
    feats = np.array(feats)
    all_features.append(feats)
    print(feats)

labels = ['filenames', 'PDdc_m', 'LPdc_m', 'PYdc_m', 'PDdc_s', 'LPdc_s', 'PYdc_s', 'PDoff', 'LPon', 'LPoff', 'PYon', 'PYoff']

All_features = pd.DataFrame(all_features, columns=labels)
All_features.to_csv(root_folder + '/analytics/MD_features.csv', index=False)



