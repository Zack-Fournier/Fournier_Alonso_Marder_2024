import os
import matplotlib.pyplot as plt
import numpy as np
from ancillary_functions import truncate_solution
from integrate_and_plot_pyloric_imi_temp import plotSolution_overlaid_perturbed
from integratePyloricSQ10s_currentscapes_RK4_mp import getDownwardCrossings

root_folder = 'C:/code_package'

pathtoci = root_folder + '/initial_conditions_and_parameters/cis_network_imi.txt'
pathtop = root_folder + '/initial_conditions_and_parameters/p-97JM4D.score.19507.072066900437.txt'


############################

# # perturbed overlaid with normal pyloric trace
# normal trace
pyloric_n = root_folder + '/models/ssc-0.1-model6.txt'
# perturbed traces
pyloric_p_SC = root_folder + '/initial_conditions_and_parameters/sample_trace_SC_perturbed.txt'
pyloric_p_IC = root_folder + '/initial_conditions_and_parameters/sample_trace_IC_perturbed.txt'
pyloric_P = [pyloric_p_IC, pyloric_p_SC]

# colors
blue = (0.196, 0.427, 0.659)
red = (0.72, 0.125, 0.145)

for pyloric_p in pyloric_P:

    if pyloric_p == pyloric_p_IC:
        color = blue

    if pyloric_p == pyloric_p_SC:
        color = red

    # plot traces
    delta = 0
    trial_n = 0
    nsecs = 10
    nsecs_sim = 7
    temp = 15
    d_string = str(delta)
    n_string = str(trial_n)
    tempdump = root_folder + '/initial_conditions_and_parameters/dump/' + 'dump' + '.txt'

    pathtojava = root_folder + '/java/model.jar'
    excommand = 'java -cp ' + pathtojava + ' tempComp.integratePyloricNetwork_temp_imi_realclean_rk4 ' + pathtoci + ' ' + pyloric_n
    command = excommand + ' ' + str(nsecs) + ' ' + str(temp) + ' 0.1 ' + ' > ' + tempdump + ' '

    os.system(command)
    soln = np.genfromtxt(tempdump)

    soln = truncate_solution(soln, nsecs, nsecs_sim)

    delta = 1
    trial_n = 0
    nsecs = 20
    nsecs_sim = 10
    temp = 15
    d_string = str(delta)
    n_string = str(trial_n)
    tempdump = root_folder + '/initial_conditions_and_parameters/dump/' + 'dump' + '.txt'

    pathtojava = root_folder + '/java/model.jar'
    excommand = 'java -cp ' + pathtojava + ' tempComp.integratePyloricNetwork_temp_imi_realclean_rk4 ' + pathtoci + ' ' + pyloric_p
    command = excommand + ' ' + str(nsecs) + ' ' + str(temp) + ' 0.1 ' + ' > ' + tempdump + ' '

    os.system(command)
    solp = np.genfromtxt(tempdump)

    solp = truncate_solution(solp, nsecs, nsecs_sim)

    # get period for normal
    nPD = soln[:, 0]
    dc = getDownwardCrossings(min(nPD) + 3, nPD)
    print(dc)
    xmin = dc[1] - 100
    xmax = dc[5] - 100
    soln = soln[xmin:xmax, :]

    # get start of perturbed
    pPD = solp[:, 0]
    dc = getDownwardCrossings(min(pPD) + 3, pPD)
    print(dc)
    pstart = dc[1] - 100
    pend = (xmax-xmin) + pstart
    solp = solp[pstart:pend, :]


    label = 'Unperturbed Pyloric Rhythm'
    # secs = nsecs - nsecs_sim
    secs = xmax - xmin
    print(secs)
    plotSolution_overlaid_perturbed(soln, solp, secs, label, color)

    plt.show()


    p = [pyloric_p, pyloric_n]

    pathtostore = 'null'
    label = 'All Models'
    y_limits = [110, 2, 1, 10, 12, 110, 7, 0.1, None, 0.1, 1.2, 0.5]
    plt.show()


    ###################
    # set font
    plt.rcParams['font.family'] = 'Calibri'
    colors = [color, 'black']
    s = 150
    # synaptic
    if color == red:
        plt.figure(figsize=(8, 4), dpi=500)
        for j in range(len(p)):
            pdim = 40
            parameters = np.genfromtxt(p[j])
            pop = np.array(parameters)  # turn the parameters list into an array
            p1 = pop[0:pdim]  # get AB/PD parameters
            p2 = pop[pdim * 1:pdim * 2]  # get LP parameters
            p3 = pop[pdim * 2:pdim * 3]  # get PY parameters
            syns = pop[pdim * 3:]  # get synapse parameters
            gs1 = p1[0:9]  # get AB/PD conductances
            gs2 = p2[0:9]  # get LP conductances
            gs3 = p3[0:9]  # get PY conductances
            syngs = syns[0:7]  # get synapse conductances
            # synssss
            plt.scatter(1, syngs[0], color=colors[j], marker='o', s=s)
            plt.scatter(2, syngs[2], color=colors[j], marker='o', s=s)
            plt.scatter(3, syngs[4], color=colors[j], marker='o', s=s)
            plt.scatter(4, syngs[5], color=colors[j], marker='o', s=s)
            plt.scatter(5, syngs[6], color=colors[j], marker='o', s=s)
            plt.scatter(6, syngs[1], color=colors[j], marker='o', s=s)
            plt.scatter(7, syngs[3], color=colors[j], marker='o', s=s)
            plt.scatter(7, syngs[3], color=colors[j], marker='o', s=s)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            labs = ['PD to PY', 'PD to LP', 'LP to PY', 'PY to LP', 'LP to PD', 'PD to LP', 'PD to PY']
            y_pos = [1, 2, 3, 4, 5, 6, 7]
            plt.gca().set_xticks(y_pos)
            plt.gca().set_xticklabels(labs, rotation='vertical')
            plt.gca().xaxis.set_tick_params(labelsize=16)
            plt.gca().yaxis.set_tick_params(labelsize=16)

    # intrinsic
    if color == blue:
        fig, axes = plt.subplots(1, 2, figsize=(8, 4), dpi=500)
        for j in range(len(p)):
            pdim = 40
            parameters = np.genfromtxt(p[j])
            pop = np.array(parameters)  # turn the parameters list into an array
            p1 = pop[0:pdim]  # get AB/PD parameters
            p2 = pop[pdim * 1:pdim * 2]  # get LP parameters
            p3 = pop[pdim * 2:pdim * 3]  # get PY parameters
            syns = pop[pdim * 3:]  # get synapse parameters
            gs1 = p1[0:9]  # get AB/PD conductances
            gs2 = p2[0:9]  # get LP conductances
            gs3 = p3[0:9]  # get PY conductances
            syngs = syns[0:7]  # get synapse conductances
            # intrinsicssss
            ax = axes[0]
            ax.scatter(1, gs1[0], color=colors[j], marker='o', s=s)
            ax.scatter(2, gs2[0], color=colors[j], marker='o', s=s)
            ax.scatter(3, gs3[0], color=colors[j], marker='o', s=s)

            ax.set_ylim(0, 105)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            y_pos = [1, 2, 3]
            labs = ['PD', 'LP', 'PY']
            ax.set_xticks(y_pos)
            ax.set_xticklabels(labs, rotation='vertical')
            ax.xaxis.set_tick_params(labelsize=18)
            ax.yaxis.set_tick_params(labelsize=18)

            ax = axes[1]
            ax.scatter(1, gs1[5], color=colors[j], marker='o', s=s)
            ax.scatter(2, gs2[5], color=colors[j], marker='o', s=s)
            ax.scatter(3, gs3[5], color=colors[j], marker='o', s=s)

            ax.set_ylim(0, 105)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            y_pos = [1, 2, 3]
            labs = ['PD', 'LP', 'PY']
            ax.set_xticks(y_pos)
            ax.set_xticklabels(labs, rotation='vertical')
            ax.xaxis.set_tick_params(labelsize=18)
            ax.yaxis.set_tick_params(labelsize=18)

    plt.tight_layout()
    plt.show()


