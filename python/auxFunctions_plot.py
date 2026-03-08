from pylab import *
import glob

def plotParameters(p,pathtostore):
    fig=figure(figsize=(8,8))  # set figure size
    labels = ('gNa','gCaT','gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL','gIMI') # create label names for conductances
    pop=array(p) # turn the parameters list into an array
    pdim=40      # this is the number of parameters per compartment
    p1=pop[0:pdim]  # get AB/PD parameters
    p2=pop[pdim*1:pdim*2] # get LP parameters
    p3=pop[pdim*2:pdim*3] # get PY parameters
    syns=pop[pdim*3:]   # get synapse parameters
    gs1= p1[0:9]  # get AB/PD conductances
    gs2= p2[0:9]  # get LP conductances
    gs3= p3[0:9]  # get PY conductances
    syngs=syns[0:7] # get synapse conductances

    pos=arange(10)
    for i in range(9):
        ax=subplot(4,3,pos[i]+1)
        #[j.set_linewidth(2) for j in ax.spines.itervalues()]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title(labels[i],y=1.08)
        g1=gs1[i]  # plot each AB/PD conductance
        g2=gs2[i]  # plot each LP conductance
        g3=gs3[i]  # plot each PY conductance

        scatter(1,g1,color='black')
        scatter(2,g2,color='black')
        scatter(3,g3,color='black')
        y_pos=[1,2,3]
        labs=['PD','LP','PY'] # create x labels
        plt.xticks(y_pos, labs,rotation='vertical')
        tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)  
        if(i!=0):plt.gca().set_ylim(bottom=0)

    ax=subplot(4,3,9+2)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #[j.set_linewidth(2) for j in ax.spines.itervalues()]
    
    title('g_glut',y=1.08)
    labs=['PD_PY','PD_LP', 'LP_PY','PY_LP','LP_PD']
    y_pos=[1,2,3,4,5]
    plt.xticks(y_pos, labs,rotation='vertical')
    scatter(1,syngs[0],color='black') 
    scatter(2,syngs[2],color='black')
    scatter(3,syngs[4],color='black')   
    scatter(4,syngs[5],color='black')   
    scatter(5,syngs[6],color='black') 
    xlim(0.,5.5) 
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    plt.gca().set_ylim(bottom=0)    
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)


    ax=subplot(4,3,9+3) 
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    #[j.set_linewidth(2) for j in ax.spines.itervalues()] 
    title('g_chol',y=1.08)
    labs=['PD_PY','PD_LP']
    y_pos=[1,2]     
    plt.xticks(y_pos, labs,rotation='vertical')
    scatter(1,syngs[1],color='black')   
    scatter(2,syngs[3],color='black') 
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom') 
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    plt.gca().set_ylim(bottom=0)
    xlim(0.5,2.5)
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)

    savefig(pathtostore+'conductances.png',transparent=False, dpi=500)

#############

import numpy as np
import matplotlib.pyplot as plt
import os

def plot_multiple_Parameters(p, pathtostore, label, y_axis_limits=None):

    fig, axes = plt.subplots(4, 3, figsize=(8, 8))  # set figure size
    labels = ('gNa', 'gCaT', 'gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gIMI')  # create label names for conductances
    pdim = 40  # this is the number of parameters per compartment

    axes[3,2].remove()

    # Initialize y-axis limits if not provided
    if y_axis_limits is None:
        y_axis_limits = [None] * 30  # Default to None for automatic scaling

    legend_labels = []
    # create for loop to update figure for all parameter sets
    for j in range(len(p)):
        # set colors and shapes
        colors = ['black', 'red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'grey', 'olive', 'cyan']
        markers = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']
        name = os.path.basename(p[j])
        name = name[:-4]
        legend_labels.append(name)

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

        pos = np.arange(10)
        for i in range(9):
            ax = axes[i // 3, i % 3]
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            title = labels[i]
            ax.set_title(title, y=1.08)
            g1 = gs1[i]  # plot each AB/PD conductance
            g2 = gs2[i]  # plot each LP conductance
            g3 = gs3[i]  # plot each PY conductance

            ax.scatter(1, g1, color=colors[j], marker=markers[j])
            ax.scatter(2, g2, color=colors[j], marker=markers[j])
            ax.scatter(3, g3, color=colors[j], marker=markers[j])
            y_pos = [1, 2, 3]
            labs = ['PD', 'LP', 'PY']  # create x labels
            ax.set_xticks(y_pos)
            ax.set_xticklabels(labs, rotation='vertical')
            plt.tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.xaxis.set_tick_params(width=2)
            ax.yaxis.set_tick_params(width=2)

            # Set y-axis limit if provided
            if y_axis_limits[i] is not None:
                ax.set_ylim(bottom=0, top=y_axis_limits[i])

        ax9_2 = axes[2, 2]
        ax9_2.set_ylim(bottom=0, top=y_axis_limits[9])


        ax = axes[3, 0]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title = 'g_glut'
        ax.set_title(title, y=1.08)
        labs = ['PD_PY', 'PD_LP', 'LP_PY', 'PY_LP', 'LP_PD']
        y_pos = [1, 2, 3, 4, 5]
        ax.set_xticks(y_pos)
        ax.set_xticklabels(labs, rotation='vertical')
        ax.scatter(1, syngs[0], color=colors[j], marker=markers[j])
        ax.scatter(2, syngs[2], color=colors[j], marker=markers[j])
        ax.scatter(3, syngs[4], color=colors[j], marker=markers[j])
        ax.scatter(4, syngs[5], color=colors[j], marker=markers[j])
        ax.scatter(5, syngs[6], color=colors[j], marker=markers[j])
        ax.set_xlim(0., 5.5)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        ax.set_ylim(bottom=0, top=y_axis_limits[10])

        ax = axes[3, 1]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title = 'g_chol'
        ax.set_title(title, y=1.08)
        labs = ['PD_PY', 'PD_LP']
        y_pos = [1, 2]
        ax.set_xticks(y_pos)
        ax.set_xticklabels(labs, rotation='vertical')
        ax.scatter(1, syngs[1], color=colors[j], marker=markers[j])
        ax.scatter(2, syngs[3], color=colors[j], marker=markers[j])
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        ax.set_ylim(bottom=0, top=y_axis_limits[11])
        ax.set_xlim(0.5, 2.5)

    # Add a legend in place of the removed subplot
    legend_handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label)
                      for color, label in zip(colors, legend_labels)]
    fig.legend(handles=legend_handles, title='Legend', loc='lower right', fontsize='small', bbox_to_anchor=(0.92, 0.01))

    plt.tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
    return fig

#############


def plot_Parameters_paper(p, pathtostore, label, y_axis_limits=None):

    # set font
    plt.rcParams['font.family'] = 'Calibri'

    fig, axes = plt.subplots(4, 3, figsize=(8, 8), dpi=300)  # set figure size
    labels = ('gNa', 'gCaT', 'gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gIMI')  # create label names for conductances
    pdim = 40  # this is the number of parameters per compartment

    axes[3,2].remove()

    # Initialize y-axis limits if not provided
    if y_axis_limits is None:
        y_axis_limits = [None] * 30  # Default to None for automatic scaling

    legend_labels = []
    # create for loop to update figure for all parameter sets
    for j in range(len(p)):
        # set colors and shapes
        RED = (0.72, 0.125, 0.145)
        colors = [RED,'black']
        markers = ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']
        name = os.path.basename(p[j])
        name = name[:-4]

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

        pos = np.arange(10)
        for i in range(9):
            ax = axes[i // 3, i % 3]
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            title = labels[i]
            ax.set_title(title, y=1.08, fontsize=18)
            g1 = gs1[i]  # plot each AB/PD conductance
            g2 = gs2[i]  # plot each LP conductance
            g3 = gs3[i]  # plot each PY conductance

            ax.scatter(1, g1, color=colors[j], marker=markers[j])
            ax.scatter(2, g2, color=colors[j], marker=markers[j])
            ax.scatter(3, g3, color=colors[j], marker=markers[j])
            y_pos = [1, 2, 3]
            labs = ['PD', 'LP', 'PY']  # create x labels
            ax.set_xticks(y_pos)
            ax.set_xticklabels(labs, rotation='vertical', fontsize=16)
            y_ticks = ax.get_yticks()
            y_ticklabels = [f'{tick:g}' for tick in y_ticks]  # Formatting to remove trailing zero
            ax.set_yticklabels(y_ticklabels)
            ax.yaxis.set_tick_params(labelsize=14)  # Set
            plt.tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.xaxis.set_tick_params(width=2)
            ax.yaxis.set_tick_params(width=2)

            # Set y-axis limit if provided
            if y_axis_limits[i] is not None:
                ax.set_ylim(bottom=0, top=y_axis_limits[i])

        ax9_2 = axes[2, 2]
        ax9_2.set_ylim(bottom=0, top=y_axis_limits[9])

        ax = axes[3, 0]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title = 'Glutamatergic'
        ax.set_title(title, y=1.08, fontsize=18)
        labs = ['PD to PY', 'PD to LP', 'LP to PY', 'PY to LP', 'LP to PD']
        y_pos = [1, 2, 3, 4, 5]
        ax.set_xticks(y_pos)
        ax.set_xticklabels(labs, rotation='vertical', fontsize=16)
        ax.scatter(1, syngs[0], color=colors[j], marker=markers[j])
        ax.scatter(2, syngs[2], color=colors[j], marker=markers[j])
        ax.scatter(3, syngs[4], color=colors[j], marker=markers[j])
        ax.scatter(4, syngs[5], color=colors[j], marker=markers[j])
        ax.scatter(5, syngs[6], color=colors[j], marker=markers[j])
        ax.set_xlim(0., 5.5)
        y_ticks = ax.get_yticks()
        y_ticklabels = [f'{tick:g}' for tick in y_ticks]  # Formatting to remove trailing zero
        ax.set_yticklabels(y_ticklabels)
        ax.yaxis.set_tick_params(labelsize=14)  # Set
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        ax.set_ylim(bottom=0, top=y_axis_limits[10])

        ax = axes[3, 1]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title = 'Cholinergic'
        ax.set_title(title, y=1.08, fontsize=18)
        labs = ['PD to PY', 'PD to LP']
        y_pos = [1, 2]
        ax.set_xticks(y_pos)
        ax.set_xticklabels(labs, rotation='vertical', fontsize=16)
        ax.scatter(1, syngs[1], color=colors[j], marker=markers[j])
        ax.scatter(2, syngs[3], color=colors[j], marker=markers[j])
        y_ticks = ax.get_yticks()
        y_ticklabels = [f'{tick:g}' for tick in y_ticks]  # Formatting to remove trailing zero
        ax.set_yticklabels(y_ticklabels)
        ax.yaxis.set_tick_params(labelsize=14)  # Set
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        ax.set_ylim(bottom=0, top=y_axis_limits[11])
        ax.set_xlim(0.5, 2.5)

    plt.tight_layout(pad=0.4, w_pad=2, h_pad=1.5)

    return fig

#################

def plot_parameter_change(p, pathtostore, label):

    fig = figure(figsize=(8, 8))  # set figure size
    labels = ('gNa', 'gCaT', 'gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gIMI')  # create label names for conductances
    pdim = 40  # this is the number of parameters per compartment

    # create for loop to update figure for all parameter sets
    for j in range(len(p)):

        # set colors and shapes
        colors = ['black', 'red']
        # markers = ['o', 's', '^', 'v', '<', '>', 'D', 'X', 'P', '*', 'H']
        markers = ['o', '*']

        parameters = genfromtxt(p[j])
        pop = array(parameters)  # turn the parameters list into an array
        p1 = pop[0:pdim]  # get AB/PD parameters
        p2 = pop[pdim * 1:pdim * 2]  # get LP parameters
        p3 = pop[pdim * 2:pdim * 3]  # get PY parameters
        syns = pop[pdim * 3:]  # get synapse parameters
        gs1 = p1[0:9]  # get AB/PD conductances
        gs2 = p2[0:9]  # get LP conductances
        gs3 = p3[0:9]  # get PY conductances
        syngs = syns[0:7]  # get synapse conductances

        pos = arange(10)
        for i in range(9):
            ax = subplot(4, 3, pos[i] + 1)
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            title(labels[i], y=1.08)
            g1 = gs1[i]  # plot each AB/PD conductance
            g2 = gs2[i]  # plot each LP conductance
            g3 = gs3[i]  # plot each PY conductance

            scatter(1, g1, color=colors[j], marker=markers[j])
            scatter(2, g2, color=colors[j], marker=markers[j])
            scatter(3, g3, color=colors[j], marker=markers[j])
            y_pos = [1, 2, 3]
            labs = ['PD', 'LP', 'PY']  # create x labels
            plt.xticks(y_pos, labs, rotation='vertical')
            tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.xaxis.set_tick_params(width=2)
            ax.yaxis.set_tick_params(width=2)
            if (i != 0): plt.gca().set_ylim(bottom=0)

        ax = subplot(4, 3, 9 + 2)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        title('g_glut', y=1.08)
        labs = ['PD_PY', 'PD_LP', 'LP_PY', 'PY_LP', 'LP_PD']
        y_pos = [1, 2, 3, 4, 5]
        plt.xticks(y_pos, labs, rotation='vertical')
        scatter(1, syngs[0], color=colors[j], marker=markers[j])
        scatter(2, syngs[2], color=colors[j], marker=markers[j])
        scatter(3, syngs[4], color=colors[j], marker=markers[j])
        scatter(4, syngs[5], color=colors[j], marker=markers[j])
        scatter(5, syngs[6], color=colors[j], marker=markers[j])
        xlim(0., 5.5)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        plt.gca().set_ylim(bottom=0)
        tight_layout(pad=0.4, w_pad=2, h_pad=1.5)

        ax = subplot(4, 3, 9 + 3)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title('g_chol', y=1.08)
        labs = ['PD_PY', 'PD_LP']
        y_pos = [1, 2]
        plt.xticks(y_pos, labs, rotation='vertical')
        scatter(1, syngs[1], color=colors[j], marker=markers[j])
        scatter(2, syngs[3], color=colors[j], marker=markers[j])
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)
        plt.gca().set_ylim(bottom=0)
        xlim(0.5, 2.5)
        tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
        savefig(pathtostore + '/conductances - ' + label + '.png', transparent=False, dpi=50)
