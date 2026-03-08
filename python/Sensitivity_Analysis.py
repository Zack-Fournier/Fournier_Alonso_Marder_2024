import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from integrate_and_plot_pyloric_imi_temp import *
from ancillary_functions import *
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp
import os
import joblib
import pickle

# set root folder
root_folder = 'C:/code_package'  # for local run

# choose model
pathtop = root_folder + '/models/Model_A.txt'

## set parameters

nsecs = 10  # total length of network integration in seconds

nsecs_sim = 5  # length of trace to analyze at end of time series (last t seconds)

temp = 25  # temperature in celsius

trials = 100  # total number of trials

###############################################################

# create delta variable
d = np.linspace(0, 1, 11)
d = np.round(d, decimals=1)

# create features matrix
# set feature number
feat_n = 11
# initialize vectors
IC_Features = np.zeros([trials*len(d), feat_n])
SC_Features = np.zeros([trials*len(d), feat_n])

pathtoci = root_folder + '/initial_conditions_and_parameters/cis_network_imi.txt'

# create matrices to store classifier results
IC_wholelab_rfc = np.zeros([trials, len(d)])
SC_wholelab_rfc = np.zeros([trials, len(d)])

# initialize results
IC_results = []
SC_results = []

if __name__ == '__main__':
    # get CPU count
    num_processes = mp.cpu_count() - 2

    # Define separate folders for each process
    modelname = os.path.basename(pathtop)
    IC_folder = root_folder + '/SA/' + modelname[:-4] + '/IC_results'
    SC_folder = root_folder + '/SA/' + modelname[:-4] + '/SC_results'

    # Create the folders if they don't exist
    os.makedirs(IC_folder, exist_ok=True)
    os.makedirs(SC_folder, exist_ok=True)

    # initiate processes
    pool = mp.Pool(processes=num_processes)

    # run protocol for each value of delta for IC
    #for i in range(len(d)):
    for delta in d:
    # store current delta value
        for x in range(trials):  # for each trial per value of delta
            trial_n = x  # store current trial number

            d_parameters = genfromtxt(pathtop)

            for i in range(0,9,1):
                d_parameters[i] = d_parameters[i] * (1 - (delta * uniform(-1, 1)))

            for i in range(40,49,1):
                d_parameters[i] = d_parameters[i] * (1 - (delta * uniform(-1, 1)))

            for i in range(80,89,1):
                d_parameters[i] = d_parameters[i] * (1 - (delta * uniform(-1, 1)))


            # print(d_parameters,delta)
            result = pool.apply_async(getSolution_IC, args=(pathtoci, pathtop, d_parameters.copy(), nsecs, nsecs_sim, temp, delta, trial_n, root_folder, IC_folder))
            IC_results.append(result)  # store result


    # run protocol for each value of delta for SC
    for delta in d:
        #store current delta value

        for x in range(trials):  # for each trial per value of delta
            trial_n = x  # store current trial number

            d_parameters = genfromtxt(pathtop)

            for i in range(120,127,1):
                d_parameters[i] = d_parameters[i] * (1 - (delta * uniform(-1, 1)))

            result = pool.apply_async(getSolution_SC, args=(
            pathtoci, pathtop, d_parameters.copy(), nsecs, nsecs_sim, temp, delta, trial_n, root_folder,SC_folder))
            SC_results.append(result)  # store result


    # close and merge processes
    pool.close()
    pool.join()


# get results for all values of delta for process 1
n = 0  # initialize delta index counter
trial_n = 1  # initialize trial number counter

for result in IC_results:  # for each result in the range of results
    Ctype = 'IC'

    IC_result, features = result.get()  # get solution

    IC_wholelab_rfc[int(trial_n - 1), int(d[n] * 10)] = IC_result[0]

    # store features
    IC_Features[trials * n + trial_n - 1, :] = features

    print('classification and storage')
    print(Ctype)
    print(str(d[n]))
    print(str(trial_n))


    if trial_n == trials:  # if the trial number is the last trial...
        trial_n = 1  # reset trial number counter
        n = n + 1  # increase delta index counter
    else:
        trial_n = trial_n + 1  # update the trial number for all other trials

#get results for all values of delta for SC
n = 0  # initialize delta index counter
trial_n = 1  # initialize trial number counter

for result in SC_results:  # for each result in the range of results
    Ctype = 'SC'
    
    # sol = SC_results[j].get()  # get solution
    SC_result, features = result.get()  # get solution

    SC_wholelab_rfc[int(trial_n - 1), int(d[n] * 10)] = SC_result[0]

    # store features
    SC_Features[trials * n + trial_n - 1, :] = features
    
    print('classification and storage')
    print(Ctype)
    print(str(d[n]))
    print(str(trial_n))

    if trial_n == trials:  # if the trial number is the last trial...
        trial_n = 1  # reset trial number counter
        n = n + 1  # increase delta index counter
    else:
        trial_n = trial_n + 1  # update the trial number for all other trials


#export classifications and features as csv

modelname = os.path.basename(pathtop)

IC_wholelab_rfc = pd.DataFrame(IC_wholelab_rfc)
SC_wholelab_rfc = pd.DataFrame(SC_wholelab_rfc)

IC_features = pd.DataFrame(IC_Features)
SC_features = pd.DataFrame(SC_Features)

IC_wholelab_rfc.to_csv(root_folder+'/SA/'+modelname[:-4]+'_IC.csv')
SC_wholelab_rfc.to_csv(root_folder+'/SA/'+modelname[:-4]+'_SC.csv')

IC_features.to_csv(root_folder+'/SA/'+modelname[:-4]+'_IC_features.csv')
SC_features.to_csv(root_folder+'/SA/'+modelname[:-4]+'_SC_features.csv')



