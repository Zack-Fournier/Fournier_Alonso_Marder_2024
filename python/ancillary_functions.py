from pyloricMeasures import *
import os
import matplotlib.pyplot as plt
from scipy import stats


# clear directory
def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            clear_directory(file_path)
            os.rmdir(file_path)


def truncate_solution(sol, nsecs, nsecs_sim):

    # calculate dt
    dt = nsecs / len(sol)
    # time to extract at end of simulation for analysis and plotting
    t_end = nsecs - nsecs_sim
    # calculate cutoff index value for truncation
    c_index = int(t_end / dt)
    # truncate solution
    sol = sol[-c_index:, :]

    return sol


def voltage_distribution(V):

    Vmean = np.mean(V)
    Vstd = np.std(V)
    Vmax = max(V)
    Vmin = min(V)
    Vkurt = stats.kurtosis(V)

    return Vmean, Vstd, Vmax, Vmin, Vkurt


def feature_finder(sol):

    features = np.zeros([11])

    # find duty cycles and frequencies
    dc_and_f = getFreqAndDc(sol)

    # get means
    dc_PD_m = dc_and_f[0][2]
    dc_LP_m = dc_and_f[1][2]
    dc_PY_m = dc_and_f[2][2]
    f_PD_m = dc_and_f[0][0]
    f_LP_m = dc_and_f[1][0]
    f_PY_m = dc_and_f[2][0]

    # get stds
    dc_PD_s = dc_and_f[0][3]
    dc_LP_s = dc_and_f[1][3]
    dc_PY_s = dc_and_f[2][3]
    f_PD_s = dc_and_f[0][1]
    f_LP_s = dc_and_f[1][1]
    f_PY_s = dc_and_f[2][1]

    cell1off_mean, cell2on_mean, cell2off_mean, cell3on_mean, cell3off_mean = getmeanPhases(sol)

    features[0] = dc_PD_m
    features[1] = dc_LP_m
    features[2] = dc_PY_m
    features[3] = dc_PD_s
    features[4] = dc_LP_s
    features[5] = dc_PY_s
    features[6] = cell1off_mean
    features[7] = cell2on_mean
    features[8] = cell2off_mean
    features[9] = cell3on_mean
    features[10] = cell3off_mean

    # make all nan values equal to zero
    features[np.isnan(features)] = 0

    return features
