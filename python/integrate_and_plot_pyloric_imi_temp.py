import matplotlib.pyplot as plt
from matplotlib.pylab import *
import os
from pyloricMeasures import *
from classifyTraces import *
from ancillary_functions import *
from auxFunctions_plot import plot_parameter_change
from sklearn.ensemble import RandomForestClassifier
import time
import joblib
import pickle


def getSolution_IC(pathtoci,pathtop,d_parameters,nsecs, nsecs_sim,temp,delta,trial_n, root_folder,IC_folder):

    with open(root_folder + '/python/classifier.pkl', "rb") as f:
        rfc = pickle.load(f)

    d_string = str(delta)
    n_string = str(trial_n)
    IC_command = IC_folder + '/command_dump'
    os.makedirs(IC_command, exist_ok=True)
    tempdump = IC_command + '/temp_' + str(temp) + '-' + 'd_' + d_string + '-' + 'n_' + n_string + '-IC-' + '.txt'

    initial_cond_path = root_folder + '/initial_conditions_and_parameters/'
    parameters = IC_folder + '/trial_parameters'
    os.makedirs(parameters, exist_ok=True)
    newpathtop= parameters + '/temp_' + str(temp) + '-' + d_string + '-' + n_string + '-IC-' + '.txt'
    savetxt(newpathtop, d_parameters)
    # Explicitly close the file
    with open(newpathtop, 'a') as f:
        f.close()
    pathtojava = root_folder + '/java/model.jar'
    excommand = 'java -cp '+pathtojava+' tempComp.integratePyloricNetwork_temp_imi_realclean_rk4 ' + pathtoci + ' ' + newpathtop
    command = excommand +' ' + str(nsecs)+' '+str(temp) + ' 0.1 '+' > ' + tempdump + ' '

    # print command
    os.system(command)   
    sol = genfromtxt(tempdump)
    os.remove(tempdump)

    # truncate vector
    sol = truncate_solution(sol, nsecs, nsecs_sim)

    # plot conductances
    plot_path = IC_folder + '/conductance_plots'
    os.makedirs(plot_path, exist_ok=True)
    label = d_string + '-' + n_string + '-IC'
    p = [pathtop, newpathtop]
    plot_parameter_change(p, plot_path, label)
    close('all')
        
    trial_n = trial_n + 1
    Ctype = 'IC'
    label = 'delta = ' + str(delta) + ' ' + 'n = ' + str(trial_n)  # create label of delta number and trial number
    plotSolutionAddLabel(sol, nsecs_sim, label, delta, trial_n, Ctype, temp, root_folder, IC_folder)  # plot solution and store plot

    #get classifier results
    features = feature_finder(sol)
    features = np.array(features)
    features = features.reshape(1, -1)

    IC_RESULT = rfc.predict(features)

    return IC_RESULT, features


def getSolution_SC(pathtoci,pathtop,d_parameters,nsecs, nsecs_sim,temp,delta,trial_n, root_folder,SC_folder):

    with open(root_folder + '/python/classifier.pkl', "rb") as f:
        rfc = pickle.load(f)

    d_string = str(delta)
    n_string = str(trial_n)
    SC_command = SC_folder + '/command_dump'
    os.makedirs(SC_command, exist_ok=True)
    tempdump = SC_command + '/temp_' + str(temp) + '-' + 'd_' + d_string + '-' + 'n_' + n_string + '-SC-' + '.txt'

    initial_cond_path = root_folder + '/initial_conditions_and_parameters/'
    parameters = SC_folder + '/trial_parameters'
    os.makedirs(parameters, exist_ok=True)
    newpathtop= parameters +'/temp_' + str(temp) + '-' + d_string + '-' + n_string + '-SC-' + '.txt'
    savetxt(newpathtop, d_parameters)
    # Explicitly close the file
    with open(newpathtop, 'a') as f:
        f.close()
    pathtojava = root_folder + '/java/model.jar'
    excommand = 'java -cp '+pathtojava+' tempComp.integratePyloricNetwork_temp_imi_realclean_rk4 ' + pathtoci + ' ' + newpathtop
    command = excommand +' ' + str(nsecs)+' '+str(temp) + ' 0.1 '+' > ' + tempdump + ' '

    os.system(command)
    sol = genfromtxt(tempdump)
    os.remove(tempdump)

    # truncate vector
    sol = truncate_solution(sol, nsecs, nsecs_sim)

    # plot conductances
    plot_path = SC_folder + '/conductance_plots'
    os.makedirs(plot_path, exist_ok=True)
    label = d_string + '-' + n_string + '-SC'
    p = [pathtop, newpathtop]
    plot_parameter_change(p, plot_path, label)
    close('all')
    
    trial_n = trial_n + 1
    Ctype = 'SC'
    label = 'delta = ' + str(delta) + ' ' + 'n = ' + str(trial_n)  # create label of delta number and trial number
    plotSolutionAddLabel(sol, nsecs_sim, label, delta, trial_n, Ctype, temp, root_folder, SC_folder)  # plot solution and store plot

    #get classifier results
    features = feature_finder(sol)
    features = np.array(features)
    features = features.reshape(1, -1)

    SC_RESULT = rfc.predict(features)

    return SC_RESULT, features


def plotSolution(sol, nsecs, d, n):

      measures = getFreqAndDc(sol)

      t=linspace(0,nsecs,len(sol[:,0]))    
      xmin=t[0]
      xmax=t[-1]
               
      N=len(sol)
      isithres=100
      dt=0.1
      swthres=-50  
      swthres2=-50+10

      fig = figure(figsize=(8,8))
      matplotlib.rcParams.update({'font.size': 13})

      subplot(311)
      
      title('f: ' + str("%0.2f" % measures[0][0]) + ' dc: '+ str("%0.2f" % measures[0][2]))
      plot(t,sol[:,0],color='black')
      plot(t,ones(len(t))*swthres,ls='dashed',color='black')
      plot(t,ones(len(t))*swthres2,ls='dashed',color='red')    
      ylabel('AB-PD [mV]') 
      plt.gca().xaxis.set_major_locator(plt.NullLocator())
      xlim(xmin,xmax)
      ylim(-70,30)
      subplot(312)
      
      title('f: ' + str("%0.2f" % measures[1][0]) + ' dc: '+ str("%0.2f" % measures[1][2]))
      plot(t,sol[:,1],color='black')
      plot(t,ones(len(t))*swthres,ls='dashed',color='black')
      plot(t,ones(len(t))*swthres2,ls='dashed',color='red')        
      ylabel('LP [mV]') 
      plt.gca().xaxis.set_major_locator(plt.NullLocator())
      xlim(xmin,xmax)
      ylim(-70,30)
      subplot(313)
      
      title('f: ' + str("%0.2f" %measures[2][0]) + ' dc: '+ str("%0.2f" % measures[2][2]))
      plot(t,sol[:,2],color='black')
      plot(t,ones(len(t))*swthres,ls='dashed',color='black')
      plot(t,ones(len(t))*swthres2,ls='dashed',color='red')        
      ylabel('PY [mV]') 
      xlabel('time [secs]') 
      ylim(-70,30)
      xlim(xmin,xmax)

      return fig



def plotSolution_feattest(sol, nsecs, features):


    V1 = sol[:, 0]
    V2 = sol[:, 1]
    V3 = sol[:, 2]

    # get spike times
    st1 = spikefinder(V1)
    st2 = spikefinder(V2)
    st3 = spikefinder(V3)

    st1 = np.array(st1)
    st2 = np.array(st2)
    st3 = np.array(st3)

    t = linspace(0, nsecs, len(sol[:, 0]))
    xmin = t[0]
    xmax = t[-1]

    N = len(sol)
    isithres = 100
    dt = 0.1
    swthres = -50
    swthres2 = -50 + 10

    fig = figure(figsize=(8, 8))
    matplotlib.rcParams.update({'font.size': 13})

    subplot(311)

    title('PDoff: ' + str("%0.2f" % features[12]) + ' dc: ' + str("%0.2f" % features[0]))
    plot(t, sol[:, 0], color='black')
    plt.scatter(st1, [20] * len(st1), color='red', label='Spike Times')
    ylabel('AB-PD [mV]')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    xlim(xmin, xmax)
    ylim(-70, 30)
    subplot(312)

    title('LPon: ' + str("%0.2f" % features[13]) + ' LPoff: ' + str("%0.2f" % features[14]) + ' dc: ' + str("%0.2f" % features[1]))
    plot(t, sol[:, 1], color='black')
    plot(st2, [20] * len(st2), color='red', marker='o', label='Spike Times')
    ylabel('LP [mV]')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    xlim(xmin, xmax)
    ylim(-70, 30)
    subplot(313)

    title('PYon: ' + str("%0.2f" % features[15]) + ' PYoff: ' + str("%0.2f" % features[16]) + ' dc: ' + str("%0.2f" % features[2]))
    plot(t, sol[:, 2], color='black')
    plot(st3, [20] * len(st3), color='red', marker='o', label='Spike Times')
    ylabel('PY [mV]')
    xlabel('time [secs]')
    ylim(-70, 30)
    xlim(xmin, xmax)

    return fig

def featplot(sol, nsecs, features):
    import matplotlib.pyplot as plt
    import numpy as np

    V1 = sol[:, 0]
    V2 = sol[:, 1]
    V3 = sol[:, 2]

    # get spike times
    st1 = spikefinder(V1)
    st2 = spikefinder(V2)
    st3 = spikefinder(V3)

    st1 = np.array(st1)
    st2 = np.array(st2)
    st3 = np.array(st3)

    # get isis and find unique interburst cutoff per trace
    isis1 = []
    for i in range(len(st1) - 1):  # get all isis and find modes
        time = st1[i + 1] - st1[i]
        time = round(time, -1)
        isis1.append(time)

    # PD inter burst cutoff value
    hist, bins = np.histogram(isis1[len(isis1)//2:], bins=2)
    indices = np.argsort(hist)[-2:]
    peak1, peak2 = bins[indices]
    val1 = (0.5 * (peak1 - peak2)) + peak2

    isis2 = []
    for i in range(len(st2) - 1):  # get all isis and find modes
        time = st2[i + 1] - st2[i]
        time = round(time, -1)
        isis2.append(time)

    # LP inter burst cutoff value
    hist, bins = np.histogram(isis2[len(isis2)//2:], bins=2)
    indices = np.argsort(hist)[-2:]
    peak1, peak2 = bins[indices]
    val2 = (0.5 * (peak1 - peak2)) + peak2

    isis3 = []
    for i in range(len(st3) - 1):  # get all isis and find modes
        time = st3[i + 1] - st3[i]
        time = round(time, -1)
        isis3.append(time)

    # PY inter burst cutoff value
    hist, bins = np.histogram(isis3[len(isis3)//2:], bins=2)
    indices = np.argsort(hist)[-2:]
    peak1, peak2 = bins[indices]
    val3 = (0.5 * (peak1 - peak2)) + peak2

    if val1 > 3000 or val1 < 1000:
        val1 = 1000
    if val2 > 3000 or val2 < 1000:
        val2 = 1000
    if val3 > 3000 or val3 < 1000:
        val3 = 1000

    bs1 = array(st1[::-1][argwhere(diff(st1[::-1]) < -val1)])[::-1]
    be1 = array(st1[argwhere(diff(st1[::1]) > val1)])
    bs2 = array(st2[::-1][argwhere(diff(st2[::-1]) < -val2)])[::-1]
    be2 = array(st2[argwhere(diff(st2[::1]) > val2)])
    bs3 = array(st3[::-1][argwhere(diff(st3[::-1]) < -val3)])[::-1]
    be3 = array(st3[argwhere(diff(st3[::1]) > val3)])

    bs1 = np.array(bs1)
    be1 = np.array(be1)
    bs2 = np.array(bs2)
    be2 = np.array(be2)
    bs3 = np.array(bs3)
    be3 = np.array(be3)

    # make sure tonic spiking has no bursts
    if np.std(isis1) < 150:
        bs1 = st1
        be1 = st1
    if np.std(isis2) < 150:
        bs2 = st2
        be2 = st2
    if np.std(isis3) < 150:
        bs3 = st3
        be3 = st3

    # Create a time series (replace this with your actual time series data)
    t = linspace(0, nsecs, len(sol[:, 0]))

    # find spike voltages
    sv1 = []
    for index in st1:
        index = int(index)
        sv1.append(V1[index])
    sv2 = []
    for index in st2:
        index = int(index)
        sv2.append(V2[index])
    sv3 = []
    for index in st3:
        index = int(index)
        sv3.append(V3[index])
    # find burst time voltages
    bvs1 = []
    for index in bs1:
        index = int(index)
        bvs1.append(V1[index])
    bve1 = []
    for index in be1:
        index = int(index)
        bve1.append(V1[index])
    bvs2 = []
    for index in bs2:
        index = int(index)
        bvs2.append(V2[index])
    bve2 = []
    for index in be2:
        index = int(index)
        bve2.append(V2[index])
    bvs3 = []
    for index in bs3:
        index = int(index)
        bvs3.append(V3[index])
    bve3 = []
    for index in be3:
        index = int(index)
        bve3.append(V3[index])


    # Plot the time series
    fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)

    axs[0].plot(t, sol[:, 0], color='black')
    axs[0].scatter(st1 * 0.0001, sv1, color='red', label='Spike Times')
    axs[0].scatter(bs1 * 0.0001, bvs1, color='black', label='Burst Start')
    axs[0].scatter(be1 * 0.0001, bve1, color='blue', label='Burst End')
    axs[0].set_ylabel('AB-PD [mV]')
    axs[0].set_ylim(-65,30)
    axs[0].set_title('PDoff: ' + str("%0.2f" % features[6]) + ' dc: ' + str("%0.2f" % features[0]))

    axs[1].plot(t, sol[:, 1], color='black')
    axs[1].scatter(st2 * 0.0001, sv2, color='red', marker='o', label='Spike Times')
    axs[1].scatter(bs2 * 0.0001, bvs2, color='black', label='Burst Start')
    axs[1].scatter(be2 * 0.0001, bve2, color='blue', label='Burst End')
    axs[1].set_ylabel('LP [mV]')
    axs[1].set_ylim(-65, 30)
    axs[1].set_title('LPon: ' + str("%0.2f" % features[7]) + ' LPoff: ' + str("%0.2f" % features[8]) + ' dc: ' + str("%0.2f" % features[1]))

    axs[2].plot(t, sol[:, 2], color='black')
    axs[2].scatter(st3 * 0.0001, sv3, color='red', marker='o', label='Spike Times')
    axs[2].scatter(bs3 * 0.0001, bvs3, color='black', label='Burst Start')
    axs[2].scatter(be3 * 0.0001, bve3, color='blue', label='Burst End')
    axs[2].set_ylabel('PY [mV]')
    axs[2].set_xlabel('time [secs]')
    axs[2].set_ylim(-65, 30)
    axs[2].set_title('PYon: ' + str("%0.2f" % features[9]) + ' PYoff: ' + str("%0.2f" % features[10]) + ' dc: ' + str("%0.2f" % features[2]))

    plt.tight_layout()

    return fig

def plotSolutionAddLabel(sol, nsecs, label, delta, trial_n, Ctype, temp, root_folder,p_folder):
    
    # plotSolutionAddLabel(sol, nsecs, label, d, n, trial_n, Ctype, temp, root_folder):

      measures = getFreqAndDc(sol)
      # print(measures)

      t=linspace(0,nsecs,len(sol[:,0]))    
      xmin=t[0]
      xmax=t[-1]
               
      N=len(sol)
      isithres=100
      dt=0.1
      swthres=-50  
      swthres2=-50+10

      fig = figure(figsize=(8,8))
      suptitle(label)
      matplotlib.rcParams.update({'font.size': 13})

      subplot(311)
      
      title('f: ' + str("%0.2f" % measures[0][0]) + ' dc: '+ str("%0.2f" % measures[0][2]))
      plot(t,sol[:,0],color='black')
      plot(t,ones(len(t))*swthres,ls='dashed',color='black')
      plot(t,ones(len(t))*swthres2,ls='dashed',color='red')    
      ylabel('AB-PD [mV]') 
      plt.gca().xaxis.set_major_locator(plt.NullLocator())
      xlim(xmin,xmax)
      ylim(-70,30)
      subplot(312)
      
      title('f: ' + str("%0.2f" % measures[1][0]) + ' dc: '+ str("%0.2f" % measures[1][2]))
      plot(t,sol[:,1],color='black')
      plot(t,ones(len(t))*swthres,ls='dashed',color='black')
      plot(t,ones(len(t))*swthres2,ls='dashed',color='red')        
      ylabel('LP [mV]') 
      plt.gca().xaxis.set_major_locator(plt.NullLocator())
      xlim(xmin,xmax)
      ylim(-70,30)
      subplot(313)
      
      title('f: ' + str("%0.2f" %measures[2][0]) + ' dc: '+ str("%0.2f" % measures[2][2]))
      plot(t,sol[:,2],color='black')
      plot(t,ones(len(t))*swthres,ls='dashed',color='black')
      plot(t,ones(len(t))*swthres2,ls='dashed',color='red')        
      ylabel('PY [mV]') 
      xlabel('time [secs]') 
      ylim(-70,30)
      xlim(xmin,xmax)

      plot_path = p_folder + '/plots'
      os.makedirs(plot_path, exist_ok=True)
      filename = plot_path + '/temp_' + str(temp) + '-' + 'd_' + str(delta) + '-' + 'n_' + str(trial_n) + ' - ' + Ctype + '.png'
      plt.savefig(filename, dpi=50)
      print('temp_' + str(temp) + '-' + 'd_' + str(delta) + '-' + 'n_' + str(trial_n) + ' - ' + Ctype)
      
      return fig
      # close('all'))



def basicplotsolution(sol, nsecs, label, modelcode, plot_dest):
    # plotSolutionAddLabel(sol, nsecs, label, d, n, trial_n, Ctype, temp, root_folder):

    measures = getFreqAndDc(sol)

    t = linspace(0, nsecs, len(sol[:, 0]))
    xmin = t[0]
    xmax = t[-1]

    N = len(sol)
    isithres = 100
    dt = 0.1
    swthres = -50
    swthres2 = -50 + 10

    fig = figure(figsize=(8, 8))
    suptitle(label)
    matplotlib.rcParams.update({'font.size': 13})

    subplot(311)

    title('f: ' + str("%0.2f" % measures[0][0]) + ' dc: ' + str("%0.2f" % measures[0][2]))
    plot(t, sol[:, 0], color='black')
    plot(t, ones(len(t)) * swthres, ls='dashed', color='black')
    plot(t, ones(len(t)) * swthres2, ls='dashed', color='red')
    ylabel('AB-PD [mV]')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    xlim(xmin, xmax)
    ylim(-70, 30)
    subplot(312)

    title('f: ' + str("%0.2f" % measures[1][0]) + ' dc: ' + str("%0.2f" % measures[1][2]))
    plot(t, sol[:, 1], color='black')
    plot(t, ones(len(t)) * swthres, ls='dashed', color='black')
    plot(t, ones(len(t)) * swthres2, ls='dashed', color='red')
    ylabel('LP [mV]')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    xlim(xmin, xmax)
    ylim(-70, 30)
    subplot(313)

    title('f: ' + str("%0.2f" % measures[2][0]) + ' dc: ' + str("%0.2f" % measures[2][2]))
    plot(t, sol[:, 2], color='black')
    plot(t, ones(len(t)) * swthres, ls='dashed', color='black')
    plot(t, ones(len(t)) * swthres2, ls='dashed', color='red')
    ylabel('PY [mV]')
    xlabel('time [secs]')
    ylim(-70, 30)
    xlim(xmin, xmax)

    filename = plot_dest + modelcode + '-'+ label + '_plot' + '.png'
    plt.savefig(filename)

    return fig


def plotSolution_overlaid_perturbed(soln, solp, nsecs, label, color):
    blue = (0.196, 0.427, 0.659)
    red = (0.72, 0.125, 0.145)

    t = linspace(0, nsecs, len(soln[:, 0]))
    xmin = t[0]
    xmax = t[-1]

    N = len(soln)
    isithres = 100
    dt = 0.1
    swthres = -50
    swthres2 = -50 + 10

    fig = figure(figsize=(8, 8), dpi=300)
    # suptitle(label, fontsize=20)
    matplotlib.rcParams.update({'font.size': 13})

    subplot(311)

    # title('AB/PD', x=1)
    plot(t, solp[:, 0], color=color)
    plot(t, soln[:, 0], color='black')
    plot(t, ones(len(t)) * swthres, ls='dashed', color='black')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    xlim(xmin, xmax)
    ylim(-70, 30)
    ax = plt.gca()

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    y_ticks = [-50,0]
    plt.yticks(y_ticks)

    subplot(312)

    # title('LP', x=1)
    plot(t, solp[:, 1], color=color)
    plot(t, soln[:, 1], color='black')
    plot(t, ones(len(t)) * swthres, ls='dashed', color='black')

    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    xlim(xmin, xmax)
    ylim(-70, 30)
    ax = plt.gca()

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    y_ticks = [-50,0]
    plt.yticks(y_ticks)

    subplot(313)

    # title('PY', x=1)
    plot(t, solp[:, 2], color=color)
    plot(t, soln[:, 2], color='black')
    plot(t, ones(len(t)) * swthres, ls='dashed', color='black')

    ylim(-70, 30)
    xlim(xmin, xmax)

    ax = plt.gca()
    plt.gca().xaxis.set_major_locator(plt.NullLocator())

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    y_ticks = [-50,0]
    plt.yticks(y_ticks)

    tight_layout()
    return fig