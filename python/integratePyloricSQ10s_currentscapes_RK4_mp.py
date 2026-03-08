# -*- coding: utf-8 -*-
from pylab import * 
import os
import string
import glob 
import time
from getCurrents import *
from plotCurrentsTraces_rk4 import * 
from plotPyloricTempUtils import * 
import multiprocessing
from multiprocessing import Pool

def getDownwardCrossings(thres,V):
    times=[]
    for i in arange(0,len(V)-1):
        if(V[i]>thres and V[i+1]<=thres):
            times.append(i)
    return array(times)

def job(pathtoci,pathtostore,pathtojava,pathtop,nsecs,temp,dt,transient):
    # The job creates the command line run by os.system. See other script for more comments
    fname = pathtostore + str(temp)+'.dump'
    excommand = 'java -cp  ' +pathtojava+' standaloneCodePyloricTempComp.integratePyloricNetwork_slow_full_temp_sameq10s_rk4_fullout_droptransient ' + pathtoci + ' ' + pathtop
    command = excommand +' ' + str(nsecs)+' '+str(temp) + ' '+str(dt)+  ' '+ str(transient)+ ' > ' + fname 
    # uncomment if you want to see the actual command line. 
    # print(command)
    os.system(command)
    sol = genfromtxt(fname)
    os.system('rm '+ fname)
    # return temp to sort the solutions. 
    return [sol,temp]
    
# IMPORTANT: you need to make sure python can find the different files. 
# pathtoci should be a string with the location of the initial conditions file included in the package
# pathtojava should be a string with the location of compiled java temp.jar (see README.txt for instructions to compile)
# pathtomodels should be a string with the location of the folder that contains the model parameters. 
# Model parameters files start with p- and contain a six letter identifier plus a score value.  

os.getcwd()
pathtoci=os.getcwd()+'/parameters_and_ci/cis_network.txt'    
pathtojava = os.getcwd()+'/temp.jar'
pathtomodels=os.getcwd()+'/parameters_and_ci/'

print(pathtomodels)

pathtosaveresults=os.getcwd()+'/simulations-currentscapes/'

# modelparameters is a list of paths to parameter files
modelparameters = glob.glob(pathtomodels+'p-*.txt') 

# or we can do it for a particular model as follows
# modelparameters = glob.glob(pathtomodels+'p-WWZ3CN*.txt') #figure 8
# modelparameters = glob.glob(pathtomodels+'p-FGFKQS*.txt') #figure 9
modelparameters = glob.glob(pathtomodels+'p-71G6LA*.txt') #figure 10


# in this example we simulate and plot the first 3 models in the list. 
# alternatively, one can construct a list modelparameters with paths to specific models 

for pathtop in modelparameters:
    
    modelname=pathtop.split('/')[-1].split('.')[0].split('-')[-1]
    pathtostore = pathtosaveresults+ pathtop.split('/')[-1]+'/'
    if not os.path.exists(pathtostore):os.makedirs(pathtostore)
    

    f= plotPyloricNetworkParameters(genfromtxt(pathtop))
    f.savefig(pathtostore + modelname+'.parameters.png', dpi=300,transparent=True) 
    
    cpcommand = 'cp ' + pathtojava  + ' ' + pathtostore
    os.system(cpcommand)
    cpcommand = 'cp ' + pathtoci + ' ' + pathtostore
    os.system(cpcommand)
    cpcommand = 'cp ' + pathtop + ' ' + pathtostore
    os.system(cpcommand)    
    cpcommand = 'cp ' + pathtop + ' ' + pathtostore + 'p-'+modelname+'.txt'
    os.system(cpcommand)        
    # os.chdir(pathtostore)
    

    # list of temperatures
    temps=[10,15,20,25]    

    # parameters of the simulation
    dt=0.05
    nsecs= 3
    transient=10

    #USE MULTIPROCESSING TO GENERATE THE SOLUTIONS IN PARALLEL (LEAVE 2 CORES FREE)
    sols=[]
    num_cores = multiprocessing.cpu_count()-2
    def log_result(result):
        sols.append(result)
    po = Pool(num_cores) 
    for temp in temps:        
        po.apply_async(job, args=(pathtoci,pathtostore,pathtojava,pathtop, nsecs, temp, dt,transient,), callback = log_result) 
    po.close()
    po.join()
    
    # sort the solutions by temperature
    nsols = array(sols)[:,0]
    sortmetemps = array(sols)[:,1]
    sols=nsols[argsort(sortmetemps)]       


    p = genfromtxt(pathtop)

    traces=[]
    currs=[]
    for i,sol in enumerate(sols):  
        print(shape(sol))
        c1 = sol[:,0:13]
        c2 = sol[:,13:13+13]
        c3 = sol[:,13+13:13+13+13]
        q10= p[12:35]
        p1=p[0:37]
        p2=p[37:37*2]
        p3=p[37*2:37*3]
        p2[12:35]=q10
        p3[12:35]=q10
        curr1= model(c1,p1,temps[i])
        curr2= model(c2,p2,temps[i])
        curr3= model(c3,p3,temps[i])
        syn_currs = getSynCurrents(sol,p,temps[i])
        tracess=[sol[:,0],sol[:,13*1],sol[:,13*2]]

        # We add the synaptic currents that go in each cell 
        curr1.append(syn_currs[-1])
        curr2.append(syn_currs[2]+syn_currs[3]+syn_currs[5])
        curr3.append(syn_currs[0]+syn_currs[1]+syn_currs[4])
        currs.append([tracess, array(curr1),array(curr2),array(curr3),array(syn_currs) ]) 
    
    #UNCOMMENT IF YOU WANT TO SAVE THE CURRENTS' TIME SERIES
    # np.save(pathtostore+pathtop.split('/')[-1]+'.currents.syn.temp.npy', *[temps,traces, currs])
    
    #PLOT CURRENTS' TRACES
    newpathtostore=pathtostore+'currents-traces/'
    if not os.path.exists(newpathtostore):os.makedirs(newpathtostore)
    
    # here we plot the currents' traces using an auxiliary module 
    figs  = plotCurrentTracesEachNeuron(currs, temps)
    figsall = plotCurrentTraces(currs, temps)
    
    for n,fig in enumerate(figsall):
        xmin=0
        xmax=nsecs
        fig.savefig(newpathtostore+modelname+'.current.traces.temp.'+str(temps[n])+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.WORK-RANGE.ALL.png', dpi=300) 
    for n,fig in enumerate(figs):
        xmin=0
        xmax=nsecs
        fig[0].savefig(newpathtostore+modelname+'.current.traces.temp.'+str(temps[n])+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.WORK-RANGE.PD.png', dpi=300) 
        fig[1].savefig(newpathtostore+modelname+'.current.traces.temp.'+str(temps[n])+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.WORK-RANGE.LP.png', dpi=300) 
        fig[2].savefig(newpathtostore+modelname+'.current.traces.temp.'+str(temps[n])+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.WORK-RANGE.PY.png', dpi=300) 
    
    
    # plot currentscapes
    newpathtostore=pathtostore+'/currentscapes/'
    if not os.path.exists(newpathtostore):os.makedirs(newpathtostore)
    
    close('all')
    for n,casetemp in enumerate(currs): 
        #sol = casetemp[-1]
        close('all')
        traces=casetemp[0]
        if(len(traces)>0):
            curr1=array(casetemp[1])
            curr2=array(casetemp[2])
            curr3=array(casetemp[3])
            temp= temps[n]
                
            PD=traces[0]

            # we want to plot a number of periods. We use downward crossings to obtain a list of timestamps spaced by one period.
            # The waverform is complex so this works sometimes and sometimes it doesn't so we plot many cycles.
            dc = getDownwardCrossings(min(PD)+3, PD)
            print(dc)
            xmin=0
            xmax=len(PD)
            print(xmin, xmax)
            
            #This plots currentscapes for the entire nsec simulation. It can be very resource intensive. 
            #ALL NOT ALIGNED
            #fignetwork = plotCurrentScapePyloricNetwork(casetemp, xmin,xmax) 
            #fignetwork.savefig(newpathtostore+hashname+'.currentscape.temp.'+str(temp)+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.dur.'+str(dt*(xmax-xmin))+'.ALL.NETWORK.png', dpi=300) 
            #
            
            #This plots one second of simulation
            #ONE SECOND ALIGNED
            if(len(dc)>1):
                print('first min PD ' , dc[0])
                xmin=dc[0]
                xmax=xmin+20000*1    
                fignetwork = plotCurrentScapePyloricNetwork(casetemp, xmin,xmax) 
                fignetwork.savefig(newpathtostore+modelname+'.currentscape.temp.'+str(temp)+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.dur.'+str(dt*(xmax-xmin))+'.aligned-one-second.NETWORK.png', dpi=300)                 
                close('all')
            
            
            # May plot one cycles
            #ONE CYCLE
            if(len(dc)>2):
                xmin=dc[0]
                xmax=dc[1]
                print('one cycle min PD ' , dc[0],'  ',  dc[1])
                close('all')                
                fignetwork = plotCurrentScapePyloricNetwork(casetemp, xmin,xmax) 
                fignetwork.savefig(newpathtostore+modelname+'.currentscape.temp.'+str(temp)+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.dur.'+str(dt*(xmax-xmin))+'.one-cycle.NETWORK.png', dpi=300)                                 

            
            # May plot two cycles
            #TWO CYCLES
            if(len(dc)>2):
                xmin=dc[0]
                xmax=dc[2]
                print('two cycles min PD ' , dc[0],'  ',  dc[2])
                close('all')                
                fignetwork = plotCurrentScapePyloricNetwork(casetemp, xmin,xmax) 
                fignetwork.savefig(newpathtostore+modelname+'.currentscape.temp.'+str(temp)+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.dur.'+str(dt*(xmax-xmin))+'.two-cycles.NETWORK.png', dpi=300) 
    
            #THREE CYCLES
            if(len(dc)>3):
                xmin=dc[0]
                xmax=dc[3]
                print('two cycles min PD ' , dc[0],'  ',  dc[2])
                close('all')                
                fignetwork = plotCurrentScapePyloricNetwork(casetemp, xmin,xmax) 
                fignetwork.savefig(newpathtostore+modelname+'.currentscape.temp.'+str(temp)+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.dur.'+str(dt*(xmax-xmin))+'.three-cycles.NETWORK.png', dpi=300)                     
    
            #FOUR CYCLES
            if(len(dc)>4):
                xmin=dc[0]
                xmax=dc[4]
                print('two cycles min PD ' , dc[0],'  ',  dc[2])
                close('all')                
                fignetwork = plotCurrentScapePyloricNetwork(casetemp, xmin,xmax) 
                fignetwork.savefig(newpathtostore+modelname+'.currentscape.temp.'+str(temp)+'.xmin.'+str(xmin)+'.xmax.' + str(xmax)+'.dt.'+str(dt)+'.dur.'+str(dt*(xmax-xmin))+'.four-cycles.NETWORK.png', dpi=300)                     

            


                   