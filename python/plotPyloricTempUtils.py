from pylab import *
from colormap import *
import numpy as np

def plotPyloricNetworkParameters(p):
    fig=figure(figsize=(8,8))
    labels = ('gNa','gCaT','gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gIMI')
    pop=array(p)
    pdim=40
    p1=pop[0:pdim]
    p2=pop[pdim*1:pdim*2]
    p3=pop[pdim*2:pdim*3]
    syns=pop[pdim*3:]
    gs1= p1[0:9]
    gs2= p2[0:9]
    gs3= p3[0:9]
    syngs=syns[0:7]
    pos=[0,1,2,3,5,6,7,8,9]
    for i in range(9):
        ax=subplot(3,5,pos[i]+1)
        # [j.set_linewidth(2) for j in ax.spines.itervalues()]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title(labels[i],y=1.08)
        g1=gs1[i]
        g2=gs2[i]
        g3=gs3[i]
        scatter(1,g1,color='black')
        scatter(2,g2,color='black')
        scatter(3,g3,color='black')
        y_pos=[1,2,3]
        labs=['PD','LP','PY']
        plt.xticks(y_pos, labs,rotation='vertical')
        tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)  
        if(i!=0):plt.gca().set_ylim(bottom=0)
        
        ax=subplot(3,5,4+1)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # [j.set_linewidth(2) for j in ax.spines.itervalues()]
        
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
        
        ax=subplot(3,5,9+1) 
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # [j.set_linewidth(2) for j in ax.spines.itervalues()] 
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

    
    labels_g = ['gNa','gCaT','gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gIMI', 'gGlut','gChol']
    labels_tau = ['tau_m_gNa','tau_h_gNa','tau_m_gCaT','tau_h_gCaT','tau_m_gCaS','tau_h_gCaS', 'tau_m_gA','tau_h_gA', 'tau_m_gKCa', 'tau_m_gKd', 'tau_m_gH','tau_iCa','tau_glut', 'tau_chol']   
    gindexes=[12,15,18,21,24,27,30,33,36,-14,-13]
    tauindexes=[13,14,16,17,19,20,22,23,25,28,31,34, -7,-6]
    for i in range(9):
        ax=subplot2grid((3,5),(2,0),colspan=2,rowspan=1) 
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # [j.set_linewidth(2) for j in ax.spines.itervalues()] 
        #title('g_chol',y=1.08)
        labs=['PD_PY','PD_LP']
        y_pos=1+arange(len(gindexes))   
        title('g_Q10')  
        scatter(1+arange(len(gindexes)),p[gindexes],color='black')   
        plt.xticks(y_pos, labels_g,rotation='vertical')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom') 
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)  
        plt.gca().set_ylim(bottom=0)
        ylim(1,1.5)
        xlim(0.5,len(gindexes)+0.5)
        
        ax=subplot2grid((3,5),(2,2),colspan=3,rowspan=1) 
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        # [j.set_linewidth(2) for j in ax.spines.itervalues()] 
        title('tau_Q10') 
        scatter(1+arange(len(tauindexes)),p[tauindexes],color='black')   
        y_pos=1+arange(len(tauindexes)) 
        plt.xticks(y_pos, labels_tau,rotation='vertical')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom') 
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)  
        plt.gca().set_ylim(bottom=0)
        xlim(0.5,len(tauindexes)+0.5)
        ylim(1,4)  
        tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
        #savefig(pathtostore+'conductances.sameQ10.png',transparent='true', dpi=500)
        return fig


#colors = matplotlib.cm.nipy_spectral(np.linspace(0, 1, len(chosenps)))
def plotConductancesModelsColors(pop):
    fig=figure(figsize=(8,8))
    labels = ('gNa','gCaT','gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL','tau_iCa')
    pop=array(pop)
    p1=pop[:,0:37]
    p2=pop[:,37*1:37*2]
    p3=pop[:,37*2:37*3]
    syns=pop[:,37*3:]
    gs1= p1[:,0:8]
    gs2= p2[:,0:8]
    gs3= p3[:,0:8]
    syngs=syns[:,0:7]
    pos=[0,1,2,3,5,6,7,8]
    cs=arange(0,len(pop))
    cmmap='brg'
    for i in range(8):
        ax=subplot(3,5,pos[i]+1)
        # [j.set_linewidth(2) for j in ax.spines.itervalues()]
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        title(labels[i],y=1.08)
        g1=gs1[:,i]
        g2=gs2[:,i]
        g3=gs3[:,i]
    
        scatter(ones(len(g1)),g1,c=cs,cmap=cmmap,linewidth='1',s=40)
        scatter(2*ones(len(g2)),g2,c=cs,cmap=cmmap,linewidth='1',s=40)
        scatter(3*ones(len(g3)),g3,c=cs,cmap=cmmap,linewidth='1',s=40)
        y_pos=[1,2,3]
        labs=['PD','LP','PY']
        plt.xticks(y_pos, labs,rotation='vertical')
        tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        ax.xaxis.set_tick_params(width=2)
        ax.yaxis.set_tick_params(width=2)  
        if(i!=0):plt.gca().set_ylim(bottom=0)
    
    ax=subplot(3,5,4+1)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # [j.set_linewidth(2) for j in ax.spines.itervalues()]
    
    title('g_glut',y=1.08)
    labs=['PD_PY','PD_LP', 'LP_PY','PY_LP','LP_PD']
    y_pos=[1,2,3,4,5]
    plt.xticks(y_pos, labs,rotation='vertical')
    scatter(ones(len(syngs[:,0])),syngs[:,0],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(2*ones(len(syngs[:,2])),syngs[:,2],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(3*ones(len(syngs[:,4])),syngs[:,4],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(4*ones(len(syngs[:,5])),syngs[:,5],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(5*ones(len(syngs[:,6])),syngs[:,6],c=cs,cmap=cmmap,linewidth='1',s=40)
    xlim(0.,5.5) 
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    plt.gca().set_ylim(bottom=0)    
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
        
    ax=subplot(3,5,9+1) 
    # [j.set_linewidth(2) for j in ax.spines.itervalues()]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    title('g_chol',y=1.08)
    labs=['PD_PY','PD_LP']
    y_pos=[1,2]     
    plt.xticks(y_pos, labs,rotation='vertical')
    scatter(1*ones(len(syngs[:,1])),syngs[:,1],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(2*ones(len(syngs[:,3])),syngs[:,3],c=cs,cmap=cmmap,linewidth='1',s=40)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom') 
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    
    plt.gca().set_ylim(bottom=0)
    xlim(0.5,2.5)
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
    
    labels_g = ['gNa','gCaT','gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gGlut','gChol']
    labels_tau = ['tau_m_gNa','tau_h_gNa','tau_m_gCaT','tau_h_gCaT','tau_m_gCaS','tau_h_gCaS', 'tau_m_gA','tau_h_gA', 'tau_m_gKCa', 'tau_m_gKd', 'tau_m_gH','tau_iCa','tau_glut', 'tau_chol']   
    gindexes=[12,15,18,21,24,27,30,33,-14,-13]
    tauindexes=[13,14,16,17,19,20,22,23,25,28,31,34, -7,-6]
    
    gq10 = pop[:, gindexes]
    tauq10 = pop[:, tauindexes]
    #for i in range(8):      
    ax=subplot2grid((3,5),(2,0),colspan=2,rowspan=1) 
    # [j.set_linewidth(2) for j in ax.spines.itervalues()]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  

    scatter(1*ones(len(gq10[:,0])),gq10[:,0],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(2*ones(len(gq10[:,1])),gq10[:,1],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(3*ones(len(gq10[:,2])),gq10[:,2],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(4*ones(len(gq10[:,3])),gq10[:,3],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(5*ones(len(gq10[:,4])),gq10[:,4],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(6*ones(len(gq10[:,5])),gq10[:,5],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(7*ones(len(gq10[:,6])),gq10[:,6],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(8*ones(len(gq10[:,7])),gq10[:,7],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(9*ones(len(gq10[:,8])),gq10[:,8],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(10*ones(len(gq10[:,9])),gq10[:,9],c=cs,cmap=cmmap,linewidth='1',s=40)
    y_pos=1+arange(len(labels_g)) 
    plt.xticks(y_pos, labels_g,rotation='vertical')
    plt.gca().set_ylim(bottom=0)
    ylim(1,1.7)
    xlim(0.5,len(gindexes)+0.5)
    
    ax=subplot2grid((3,5),(2,2),colspan=3,rowspan=1) 
    
    [j.set_linewidth(2) for j in ax.spines.itervalues()]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  

    scatter(1*ones(len(tauq10[:,0])),tauq10[:,0],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(2*ones(len(tauq10[:,1])),tauq10[:,1],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(3*ones(len(tauq10[:,2])),tauq10[:,2],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(4*ones(len(tauq10[:,3])),tauq10[:,3],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(5*ones(len(tauq10[:,4])),tauq10[:,4],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(6*ones(len(tauq10[:,5])),tauq10[:,5],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(7*ones(len(tauq10[:,6])),tauq10[:,6],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(8*ones(len(tauq10[:,7])),tauq10[:,7],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(9*ones(len(tauq10[:,8])),tauq10[:,8],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(10*ones(len(tauq10[:,9])),tauq10[:,9],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(11*ones(len(tauq10[:,10])),tauq10[:,10],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(12*ones(len(tauq10[:,11])),tauq10[:,11],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(13*ones(len(tauq10[:,12])),tauq10[:,12],c=cs,cmap=cmmap,linewidth='1',s=40)
    scatter(14*ones(len(tauq10[:,13])),tauq10[:,13],c=cs,cmap=cmmap,linewidth='1',s=40)
    
    #scatter(15*ones(len(tauq10[:,14])),tauq10[:,6],c=cs,cmap=cmmap,linewidth='1',s=40)
    #scatter(8*ones(len(tauq10[:,7])),tauq10[:,7],c=cs,cmap=cmmap,linewidth='1',s=40)
    
    y_pos=1+arange(len(labels_tau)) 
    plt.xticks(y_pos, labels_tau,rotation='vertical')
    xlim(0.5,len(tauindexes)+0.5)
    ylim(1,4.2)  
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
    return fig
    
    
    
def plotConductancesModelsColorsShapes(pop):
    m = ["v", "s","D" ] 
    fig=figure(figsize=(8,8))
    labels = ('gNa','gCaT','gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL','tau_iCa')
    pop=array(pop)
    p1=pop[:,0:37]
    p2=pop[:,37*1:37*2]
    p3=pop[:,37*2:37*3]
    syns=pop[:,37*3:]
    gs1= p1[:,0:8]
    gs2= p2[:,0:8]
    gs3= p3[:,0:8]
    syngs=syns[:,0:7]
    pos=[0,1,2,3,5,6,7,8]
    cs=arange(0,len(pop))
    cmmap='brg'
    
    for cellnum in arange(3):
        for i in range(8):
            ax=subplot(3,5,pos[i]+1)
            # [j.set_linewidth(2) for j in ax.spines.itervalues()]
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            title(labels[i],y=1.08)
            g1=gs1[cellnum,i]
            g2=gs2[cellnum,i]
            g3=gs3[cellnum,i]
        
            scatter(1,g1,c=cs,marker=m[cellnum],linewidth='1',s=40)
            scatter(2,g2,c=cs,markers=m[cellnum],linewidth='1',s=40)
            scatter(3,g3,c=cs,markers=m[cellnum],linewidth='1',s=40)
            y_pos=[1,2,3]
            labs=['PD','LP','PY']
            plt.xticks(y_pos, labs,rotation='vertical')
            tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
            ax.yaxis.set_ticks_position('left')
            ax.xaxis.set_ticks_position('bottom')
            ax.xaxis.set_tick_params(width=2)
            ax.yaxis.set_tick_params(width=2)  
            if(i!=0):plt.gca().set_ylim(bottom=0)
    
    ax=subplot(3,5,4+1)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # [j.set_linewidth(2) for j in ax.spines.itervalues()]
    
    title('g_glut',y=1.08)
    labs=['PD_PY','PD_LP', 'LP_PY','PY_LP','LP_PD']
    y_pos=[1,2,3,4,5]
    plt.xticks(y_pos, labs,rotation='vertical')
    for cellnum in arange(3):
        scatter(ones(len(syngs[cellnum,0])),syngs[cellnum,0],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(2*ones(len(syngs[cellnum,2])),syngs[cellnum,2],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(3*ones(len(syngs[cellnum,4])),syngs[cellnum,4],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(4*ones(len(syngs[cellnum,5])),syngs[cellnum,5],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(5*ones(len(syngs[cellnum,6])),syngs[cellnum,6],c=cs,marker=m[cellnum],linewidth='1',s=40)
    xlim(0.,5.5) 
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    plt.gca().set_ylim(bottom=0)    
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
        
    ax=subplot(3,5,9+1) 
    # [j.set_linewidth(2) for j in ax.spines.itervalues()]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    title('g_chol',y=1.08)
    labs=['PD_PY','PD_LP']
    y_pos=[1,2]     
    plt.xticks(y_pos, labs,rotation='vertical')
    for cellnum in arange(3):
        scatter(1*ones(len(syngs[cellnum,1])),syngs[cellnum,1],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(2*ones(len(syngs[cellnum,3])),syngs[cellnum,3],c=cs,marker=m[cellnum],linewidth='1',s=40)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom') 
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    
    plt.gca().set_ylim(bottom=0)
    xlim(0.5,2.5)
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
    
    labels_g = ['gNa','gCaT','gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gGlut','gChol']
    labels_tau = ['tau_m_gNa','tau_h_gNa','tau_m_gCaT','tau_h_gCaT','tau_m_gCaS','tau_h_gCaS', 'tau_m_gA','tau_h_gA', 'tau_m_gKCa', 'tau_m_gKd', 'tau_m_gH','tau_iCa','tau_glut', 'tau_chol']   
    gindexes=[12,15,18,21,24,27,30,33,-14,-13]
    tauindexes=[13,14,16,17,19,20,22,23,25,28,31,34, -7,-6]
    
    gq10 = pop[:, gindexes]
    tauq10 = pop[:, tauindexes]
    #for i in range(8):      
    ax=subplot2grid((3,5),(2,0),colspan=2,rowspan=1) 
    # [j.set_linewidth(2) for j in ax.spines.itervalues()]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    for cellnum in arange(3):
        scatter(1*ones(len(gq10[:,0])),gq10[cellnum,0],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(2*ones(len(gq10[:,1])),gq10[cellnum,1],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(3*ones(len(gq10[:,2])),gq10[cellnum,2],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(4*ones(len(gq10[:,3])),gq10[cellnum,3],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(5*ones(len(gq10[:,4])),gq10[cellnum,4],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(6*ones(len(gq10[:,5])),gq10[cellnum,5],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(7*ones(len(gq10[:,6])),gq10[cellnum,6],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(8*ones(len(gq10[:,7])),gq10[cellnum,7],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(9*ones(len(gq10[:,8])),gq10[cellnum,8],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(10*ones(len(gq10[:,9])),gq10[cellnum,9],c=cs,marker=m[cellnum],linewidth='1',s=40)
    y_pos=1+arange(len(labels_g)) 
    plt.xticks(y_pos, labels_g,rotation='vertical')
    plt.gca().set_ylim(bottom=0)
    ylim(1,1.7)
    xlim(0.5,len(gindexes)+0.5)
    
    ax=subplot2grid((3,5),(2,2),colspan=3,rowspan=1) 
    
    # [j.set_linewidth(2) for j in ax.spines.itervalues()]
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(width=2)
    ax.yaxis.set_tick_params(width=2)  
    for cellnum in arange(3):
        scatter(1*ones(len(tauq10[:,0])),tauq10[cellnum,0],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(2*ones(len(tauq10[:,1])),tauq10[cellnum,1],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(3*ones(len(tauq10[:,2])),tauq10[cellnum,2],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(4*ones(len(tauq10[:,3])),tauq10[cellnum,3],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(5*ones(len(tauq10[:,4])),tauq10[cellnum,4],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(6*ones(len(tauq10[:,5])),tauq10[cellnum,5],c=cs,cmarker=m[cellnum],linewidth='1',s=40)
        scatter(7*ones(len(tauq10[:,6])),tauq10[cellnum,6],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(8*ones(len(tauq10[:,7])),tauq10[cellnum,7],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(9*ones(len(tauq10[:,8])),tauq10[cellnum,8],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(10*ones(len(tauq10[:,9])),tauq10[cellnum,9],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(11*ones(len(tauq10[:,10])),tauq10[cellnum,10],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(12*ones(len(tauq10[:,11])),tauq10[cellnum,11],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(13*ones(len(tauq10[:,12])),tauq10[cellnum,12],c=cs,marker=m[cellnum],linewidth='1',s=40)
        scatter(14*ones(len(tauq10[:,13])),tauq10[cellnum,13],c=cs,marker=m[cellnum],linewidth='1',s=40)
    
    #scatter(15*ones(len(tauq10[:,14])),tauq10[:,6],c=cs,cmap=cmmap,linewidth='1',s=40)
    #scatter(8*ones(len(tauq10[:,7])),tauq10[:,7],c=cs,cmap=cmmap,linewidth='1',s=40)
    
    y_pos=1+arange(len(labels_tau)) 
    plt.xticks(y_pos, labels_tau,rotation='vertical')
    xlim(0.5,len(tauindexes)+0.5)
    ylim(1,4.2)  
    tight_layout(pad=0.4, w_pad=2, h_pad=1.5)
    return fig    
def plotCurrentScape(trace, currents):      
    fig = figure(figsize=(4,4))
        
    c0=array(currents)
    cpos= c0.copy()
    cpos[c0<0]=0    
    cneg=c0.copy()
    cneg[c0>0]=0
    
    normapos = sum(abs(array(cpos)),axis=0)
    normaneg = sum(abs(array(cneg)),axis=0)
    npPD=normapos
    nnPD=normaneg
    cnorm=c0.copy()
    cnorm[c0>0]=(abs(c0)/normapos)[c0>0]
    cnorm[c0<0]=-(abs(c0)/normaneg)[c0<0]
    
    resy=1000
    impos=zeros((resy,shape(cnorm)[-1])) 
    imneg=zeros((resy,shape(cnorm)[-1]))     
    times=arange(0,shape(cnorm)[-1])
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]>0):
                percent = int(curr[t]*(resy))   
                impos[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]<0):
                percent = int(abs(curr[t])*(resy))   
                imneg[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    im0= vstack((impos,imneg))   

    
    clf()
    swthres=-50        
    ax=subplot2grid((7,1),(0,0),rowspan=2)
    t=arange(0,len(trace))
    plot(t, trace, color='black',lw=1.)
    plot(t,ones(len(t))*swthres,ls='dashed',color='black',lw=0.75)
    vlines(1,-50,-20,lw=1)
    ylim(-75,30)
    xlim(0,len(trace))
    axis('off')         
    
    elcolormap='Set1'
    #xmin=10000*8
    #xmax=10000*10
    #ax=subplot2grid((24,1),(7,0),rowspan=1)
    ax=subplot2grid((7,1),(2,0),rowspan=1)
    fill_between(arange(len((npPD))),(npPD),color='black')
    plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    yscale('log')
    ylim(0.01,1500)
    xlim(0,xmax-xmin)
    axis('off') 
    
    ax=subplot2grid((7,1),(3,0),rowspan=3)
    #for axxis in ['top','bottom','left','right']:ax.spines[axxis].set_linewidth(2)
    imshow(im0[::1,::1],interpolation='nearest',aspect='auto',cmap=elcolormap)
    ylim(2*resy,0)
    plot(resy*ones(len(npPD)),color='black',lw=2)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    xlim(0,xmax-xmin)
    clim(0,8)
    axis('off') 
    #subplot(413)
    ax=subplot2grid((7,1),(6,0),rowspan=1)
    fill_between(arange(len((nnPD))),(nnPD),color='black')
    plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    yscale('log')
    ylim(1500,0.01)
    xlim(0,xmax-xmin)
    axis('off') 
    subplots_adjust(wspace=0, hspace=0)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    #savefig(pathtostore+'sol.'+hashname+'.s.'+str(score)+'.currents.png',dpi=500) 
    #savefig(pathtostore+'sol.CaT.'+str(percents[n])+'.xmin.'+str(xmin)+'.xmax.'+str(xmax)+'.traces.currentscape.png',dpi=500)
    return fig  


def plotCurrentScapePyloricNetwork(currs, xmin, xmax):

    # change currs to currents
    currents = currs

    # breakdown currents matrix
    tracess = currents[0:3, :]
    curr1 = currents[3:13, :]
    curr2 = currents[13:23, :]
    curr3 = currents[23:33, :]
    syn_currs = currents[33:40, :]

    # check synaptic currents


    # truncate matrices and rename
    traces = tracess[:, xmin:xmax]
    curr1=curr1[:,xmin:xmax]
    curr2=curr2[:,xmin:xmax]
    curr3=curr3[:,xmin:xmax]
    syn_currs=syn_currs[:, xmin:xmax]

    #COMPUTE CURRENTSCAPES. THIS IS DIRTY, THREE COPIES OF THE SAME CHUNK OF CODE - OCT2018
    resy=1000
    
    c0=curr1
    c0=array(c0)
    cpos= c0.copy()
    cpos[c0<0]=0    
    cneg=c0.copy()
    cneg[c0>0]=0    
    normapos = sum(abs(array(cpos)),axis=0)
    normaneg = sum(abs(array(cneg)),axis=0)
    npPD=normapos
    nnPD=normaneg
    cnorm=c0.copy()
    cnorm[c0>0]=(abs(c0)/normapos)[c0>0]
    cnorm[c0<0]=-(abs(c0)/normaneg)[c0<0]
    impos=zeros((resy,shape(cnorm)[-1])) 
    imneg=zeros((resy,shape(cnorm)[-1])) 
    times=arange(0,shape(cnorm)[-1])
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]>0):
                percent = int(curr[t]*(resy))   
                impos[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]<0):
                percent = int(abs(curr[t])*(resy))   
                imneg[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    im0= vstack((impos,imneg))
    
    #SECOND COPY    
    c0=curr2
    c0=array(c0)
    cpos= c0.copy()
    cpos[c0<0]=0    
    cneg=c0.copy()
    cneg[c0>0]=0
    
    normapos = sum(abs(array(cpos)),axis=0)
    normaneg = sum(abs(array(cneg)),axis=0)
    npLP=normapos
    nnLP=normaneg
    
    cnorm=c0.copy()
    cnorm[c0>0]=(abs(c0)/normapos)[c0>0]
    cnorm[c0<0]=-(abs(c0)/normaneg)[c0<0]
    impos=zeros((resy,shape(cnorm)[-1])) 
    imneg=zeros((resy,shape(cnorm)[-1])) 
    
    times=arange(0,shape(cnorm)[-1])
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]>0):
                percent = int(curr[t]*(resy))   
                impos[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]<0):
                percent = int(abs(curr[t])*(resy))   
                imneg[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    
    im1= vstack((impos,imneg))   

    #THIRD COPY       
    c0=curr3
    c0=array(c0)
    cpos= c0.copy()
    cpos[c0<0]=0
    
    cneg=c0.copy()
    cneg[c0>0]=0
    
    normapos = sum(abs(array(cpos)),axis=0)
    normaneg = sum(abs(array(cneg)),axis=0)
    npPY=normapos
    nnPY=normaneg
    
    cnorm=c0.copy()
    cnorm[c0>0]=(abs(c0)/normapos)[c0>0]
    cnorm[c0<0]=-(abs(c0)/normaneg)[c0<0]
    
    impos=zeros((resy,shape(cnorm)[-1])) 
    imneg=zeros((resy,shape(cnorm)[-1])) 
    
    times=arange(0,shape(cnorm)[-1])
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]>0):
                percent = int(curr[t]*(resy))   
                impos[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    for t in times:
        lastpercent=0
        for numcurr, curr in enumerate(cnorm):
            if(curr[t]<0):
                percent = int(abs(curr[t])*(resy))   
                imneg[lastpercent:lastpercent+percent,t]=numcurr
                lastpercent=lastpercent+percent        
    im2= vstack((impos,imneg))
    print('done computing images, plotting')
        
    
    #PLOTTING STARTS HERE
    AB = traces[0]
    LP = traces[1]
    PY = traces[2]
    
    close('all')
    traces=[AB,LP,PY]
    ims=[im0,im1,im2]
    unitlabels=['AB', 'LP', 'PY']

    npPD=np.log2(npPD)
    nnPD=np.log2(nnPD)
    npLP=np.log2(npLP)
    nnLP=np.log2(nnLP)
    npPY=np.log2(npPY)
    nnPY=np.log2(nnPY)

    norms=[[npPD,nnPD],[npLP,nnLP],[npPY,nnPY]]

    print('ref:', max(npPD))
    # elcolormap='Set1'
    #elcolormap = 'tab10'
    elcolormap = customcmap()
    
    fignetwork = figure(figsize=(4,8))
    #TRACES
    subplot2grid((24,1),(0,0),rowspan=6)
    plot(AB,color='black',lw=1)
    plot(-50*ones(len(AB)),color='black', ls='dashed', lw=0.5)
    vlines(0,-50,-20,color='black',lw=2)
     
    plot(LP-90,color='black',lw=1)
    plot(-50*ones(len(AB))-90,color='black', ls='dashed', lw=0.5)
    plot(PY-(2*90),color='black',lw=1) 
    plot(-50*ones(len(AB))-(2*90),color='black', ls='dashed', lw=0.5)
    xlim(0,len(AB))
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    ylim(-180-70,30)
    axis('off') 
    
    #PD            
    ax=subplot2grid((24,1),(7,0),rowspan=1)
    fill_between(arange(len((npPD))),(npPD),color='black')
    # plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(8)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(32)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(128)*ones(len(nnPD)),color='black', ls=':',lw=1)

    # yscale('log')
    ylim(0.01, 7.2)  # CHANGING YLIM FROM 1500 TO 100
    xlim(0,len(AB))
    axis('off') 
    ax=subplot2grid((24,1),(8,0),rowspan=3)
    #for axxis in ['top','bottom','left','right']:ax.spines[axxis].set_linewidth(2)
    imshow(im0[::1,::1],interpolation='nearest',aspect='auto',cmap=elcolormap)
    ylim(2*resy,0)
    plot(resy*ones(len(npPD)),color='black',lw=2)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    xlim(0,len(AB))
    clim(0,9)
    axis('off') 
    #subplot(413)
    ax=subplot2grid((24,1),(11,0),rowspan=1)
    fill_between(arange(len((nnPD))),(nnPD),color='black')
    # plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(8)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(32)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(128)*ones(len(nnPD)),color='black', ls=':',lw=1)
    # yscale('log')
    ylim(7.2,0.01)  # changed
    xlim(0,len(AB))
    axis('off') 
            
    ax=subplot2grid((24,1),(13,0),rowspan=1)
    fill_between(arange(len((npPD))),(npLP),color='black')
    # plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(8)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(32)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(128)*ones(len(nnPD)),color='black', ls=':',lw=1)
    # yscale('log')
    ylim(0.01, 7.2)  # CHANGING YLIM FROM 1500 T0 500
    xlim(0,len(AB))
    axis('off') 
    ax=subplot2grid((24,1),(14,0),rowspan=3)
    #for axxis in ['top','bottom','left','right']:ax.spines[axxis].set_linewidth(2)
    imshow(im1[::1,::1],interpolation='nearest',aspect='auto',cmap=elcolormap)
    ylim(2*resy,0)
    plot(resy*ones(len(npPD)),color='black',lw=2)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    xlim(0,len(AB))
    clim(0,9)
    axis('off') 
    #subplot(413)
    ax=subplot2grid((24,1),(17,0),rowspan=1)
    fill_between(arange(len((nnPD))),(nnLP),color='black')
    # plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(8)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(32)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(128)*ones(len(nnPD)),color='black', ls=':',lw=1)
    # yscale('log')
    ylim(7.2,0.01)  # changed
    xlim(0,len(AB))
    axis('off') 
        
    ax=subplot2grid((24,1),(19,0),rowspan=1)
    fill_between(arange(len((npPD))),(npPY),color='black')
    # plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(8)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(32)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(128)*ones(len(nnPD)),color='black', ls=':',lw=1)
    # yscale('log')
    ylim(0.01,7.2)
    xlim(0,len(AB))
    axis('off') 
    ax=subplot2grid((24,1),(20,0),rowspan=3)
    #for axxis in ['top','bottom','left','right']:ax.spines[axxis].set_linewidth(2)
    imshow(im2[::1,::1],interpolation='nearest',aspect='auto',cmap=elcolormap)
    ylim(2*resy,0)
    plot(resy*ones(len(npPD)),color='black',lw=2)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    xlim(0,len(AB))
    clim(0,9)
    axis('off') 
    #subplot(413)
    ax=subplot2grid((24,1),(23,0),rowspan=1)
    fill_between(arange(len((nnPD))),(nnPY),color='black')
    # plot(5.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(50.*ones(len(nnPD)),color='black', ls=':',lw=1)
    # plot(500.*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(8)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(32)*ones(len(nnPD)),color='black', ls=':',lw=1)
    plot(np.log2(128)*ones(len(nnPD)),color='black', ls=':',lw=1)
    #yscale('log')
    ylim(7.2,0.01)
    xlim(0,len(AB))
    axis('off')          
    #subplots_adjust(wspace=0, hspace=0, w)
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    return fignetwork
    