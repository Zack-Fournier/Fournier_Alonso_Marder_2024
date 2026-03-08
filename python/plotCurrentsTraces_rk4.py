from pylab import * 
def findFirstMinima(trace):
    mintrace = min(trace)
    minlocs = argwhere(trace<mintrace+0.1)
    r = min(minlocs)
    return r


def plotCurrentTraces(currs, temp):

    # create currents object
    currents = currs

    # create individual current matrices
    tracess = currents[0:3, :]
    curr1 = currents[3:13, :]
    curr2 = currents[13:23, :]
    curr3 = currents[23:33, :]
    syn_currs = currents[33:40, :]

    lims=[]
    for i in range(9):
        aux=[]

        aux.extend(curr1[i, :])
        aux.extend(curr2[i, :])
        aux.extend(curr3[i, :])

        limsna = [min(aux),max(aux)]
        lims.append(limsna)

    lims_syn=[]
    for i in range(7):
        aux=[]

        aux.extend(syn_currs[i, :])
        limsna = [min(aux),max(aux)]
        lims_syn.append(limsna)

    refs0=[]
    c = curr1
    for i in range(10):
        cur = c[i, :]
        refs0.append([min(cur),max(cur)])    
    
    refs1=[]
    c = curr2
    for i in range(10):
        cur = c[i, :]
        refs1.append([min(cur),max(cur)])

    refs2=[]
    c = curr3
    for i in range(10):
        cur = c[i, :]
        refs2.append([min(cur), max(cur)])

    refs3=[]
    c = syn_currs
    for i in range(7):
        cur = c[i, :]
        refs3.append([min(cur),max(cur)])

    close('all') 
    figure(figsize=(15,10))
    labels = ('Na','CaT','CaS', 'A', 'KCa', 'Kd', 'H', 'L', 'IMI')
    figs=[]
    for who in range(10):
        f = figure(figsize=(15,10))

        AB = tracess[0, :]
        LP = tracess[1, :]
        PY = tracess[2, :]

        # Use AB-PD current
        c = curr1

        # initialize plot
        xmin=0
        xmax=len(AB)
        subplot2grid((10,4),(0,0))
        ylabel('V [mV]')
        title('AB-PD') 
        plot(AB,color='blue')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        ylim(-70,30)
        yticks(linspace(-70, 30, 5))
        xlim(xmin,xmax)
        subplot2grid((10,4),(0,1))
        title('LP')
        plot(LP,color='blue')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        ylim(-70,30)
        xlim(xmin,xmax)
        subplot2grid((10,4),(0,2))
        title('PY')
        plot(PY,color='blue')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        ylim(-70,30)
        xlim(xmin,xmax)
        subplot2grid((10,4),(0,3))
        title('SYN')
        axis('off')
        for i in range(9):
            subplot2grid((10,4),(i+1,0))
            plot(c[i,:],color='black')
            plot(ones(len(c[i,:]))*refs0[i][0],color='red', ls='dashed')
            plot(ones(len(c[i,:]))*refs0[i][1],color='red', ls='dashed')
            ylim(lims[i][0],lims[i][1])
            xlim(xmin,xmax)
            yticks(np.linspace(lims[i][0], lims[i][1], 5))
            #locator_params(axis='y', nticks=3)
            ylabel(labels[i] + ' [nA]')
            plt.gca().xaxis.set_major_locator(plt.NullLocator())

        # Use LP current
        c = curr2
        for i in range(9):
            subplot2grid((10,4),(i+1,1))
            plot(c[i,:],color='black')
            plot(ones(len(c[i,:]))*refs1[i][0],color='red', ls='dashed')
            plot(ones(len(c[i,:]))*refs1[i][1],color='red', ls='dashed')
            ylim(lims[i][0],lims[i][1])
            xlim(xmin,xmax)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())

        # Use PY current
        c = curr3
        for i in range(9):
            subplot2grid((10,4),(i+1,2))
            plot(c[i,:],color='black')
            plot(ones(len(c[i,:]))*refs2[i][0],color='red', ls='dashed')
            plot(ones(len(c[i,:]))*refs2[i][1],color='red', ls='dashed')
            ylim(lims[i][0],lims[i][1])
            xlim(xmin,xmax)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
            plt.gca().yaxis.set_major_locator(plt.NullLocator())

        # Use Syn Currents
        c = syn_currs
        labels_syn = ('ABPY_g','ABPY_c','ABLP_g', 'ABLP_c', 'LPPY_g', 'PYLP_g', 'LPAB_g')
        for i in range(7):
            ax =subplot2grid((10,4),(i+1,3))
            plot(c[i,:],color='black')
            plot(ones(len(c[i,:]))*refs3[i][0],color='red', ls='dashed')
            plot(ones(len(c[i,:]))*refs3[i][1],color='red', ls='dashed')
            ylim(lims_syn[i][0],lims_syn[i][1])
            yticks(linspace(lims_syn[i][0],lims_syn[i][1], 5))
            xlim(xmin,xmax)
            ylabel(labels_syn[i])
            ax.yaxis.tick_right()
            ax.yaxis.set_label_position("right")
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
        #savefig(pathtostore+'currents.full.temp.'+str(temp)+'.png',dpi=300)
        subplots_adjust(left=0.1, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.3)
        figs.append(f)
    return figs




def plotCurrentTracesEachNeuron(currs, temp):

    # create currents object
    currents = currs

    # create individual current matrices
    tracess = currents[0:3, :]
    curr1 = currents[3:13, :]
    curr2 = currents[13:23, :]
    curr3 = currents[23:33, :]
    syn_currs = currents[33:40, :]

    # create plot limits object
    limspd=[]
    limslp=[]
    limspy=[]

    for i in range(10):

        auxpd=[]
        auxlp=[]
        auxpy=[]

        auxpd=curr1[i, :]
        auxlp=curr2[i, :]
        auxpy=curr3[i, :]

        # for tempcase in currents:
        limsspd = [min(auxpd),max(auxpd)]
        limsslp = [min(auxlp),max(auxlp)]
        limsspy = [min(auxpy),max(auxpy)]
        limspd.append(limsspd)
        limslp.append(limsslp)
        limspy.append(limsspy)
    lims_syn=[]
    for i in range(7):
        aux=[]
        aux.extend(syn_currs[i, :])
        limsna = [min(aux),max(aux)]
        lims_syn.append(limsna)     

    # refs for AB-PD
    refs0=[]
    c = curr1
    for i in range(10):
        cur = c[i, :]
        refs0.append([min(cur),max(cur)])

    # refs for LP
    refs1=[]
    c = curr2
    for i in range(10):
        cur = c[i, :]
        refs1.append([min(cur),max(cur)])

    # refs for PY
    refs2=[]
    c = curr3
    for i in range(10):
        cur = c[i, :]
        refs2.append([min(cur),max(cur)])

    close('all') 
    #figure(figsize=(5,10))
    labels = ('Na','CaT','CaS', 'A', 'KCa', 'Kd', 'H', 'L', 'IMI')
    figs=[]
    for who in range(9):

        # set traces
        AB = tracess[0, :]
        LP = tracess[1, :]
        PY = tracess[2, :]


        # use AB-PD current
        c = curr1
        xmin=0
        xmax=len(AB)
        fpd = figure(figsize=(4,12))
        subplot2grid((10,1),(0,0))
        ylabel('V [mV]')
        title('AB-PD') 
        plot(AB,color='blue')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        ylim(-70,30)
        yticks(linspace(-70, 30, 5))
        xlim(xmin,xmax)
        for i in range(9):
            subplot2grid((10,1),(i+1,0))
            plot(c[i,:],color='black')
            plot(ones(len(c[i,:]))*refs0[i][0],color='red', ls='dashed')
            plot(ones(len(c[i,:]))*refs0[i][1],color='red', ls='dashed')
            ylim(limspd[i][0],limspd[i][1])
            xlim(xmin,xmax)
            yticks(floor(np.linspace(limspd[i][0], limspd[i][1], 5)))
            #locator_params(axis='y', nticks=3)
            ylabel(labels[i] + ' [nA]')
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
        subplots_adjust(left=0.35, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.3)
        
        # Use LP current
        c = curr2
        flp = figure(figsize=(4,12))
        subplot2grid((10,1),(0,0))
        title('LP')
        plot(LP,color='blue')
        ylabel('V [mV]')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        ylim(-70,30)
        xlim(xmin,xmax)
        for i in range(9):
            subplot2grid((10,1),(i+1,0))
            plot(c[i,:],color='black')
            plot(ones(len(c[i,:]))*refs1[i][0],color='red', ls='dashed')
            plot(ones(len(c[i,:]))*refs1[i][1],color='red', ls='dashed')
            ylim(limslp[i][0],limslp[i][1])
            ylabel(labels[i] + ' [nA]')
            yticks(floor(np.linspace(limslp[i][0], limslp[i][1], 5)))
            xlim(xmin,xmax)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())
        subplots_adjust(left=0.35, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.3)

        # Use PY current
        c = curr3
        fpy = figure(figsize=(4,12))
        subplot2grid((10,1),(0,0))
        title('PY')
        plot(PY,color='blue')
        ylabel('V [mV]')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        ylim(-70,30)
        xlim(xmin,xmax)
        for i in range(9):
            subplot2grid((10,1),(i+1,0))
            plot(c[i,:],color='black')
            plot(ones(len(c[i,:]))*refs2[i][0],color='red', ls='dashed')
            plot(ones(len(c[i,:]))*refs2[i][1],color='red', ls='dashed')
            ylim(limspy[i][0],limspy[i][1])
            ylabel(labels[i] + ' [nA]')
            yticks(floor(np.linspace(limspy[i][0], limspy[i][1], 5)))
            xlim(xmin,xmax)
            plt.gca().xaxis.set_major_locator(plt.NullLocator())

        #savefig(pathtostore+'currents.full.temp.'+str(temp)+'.png',dpi=300)
        subplots_adjust(left=0.35, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.3)
        figs.append([fpd,flp,fpy])
    return figs


def plotCurrents(curr):
    fig=figure()
    labels = ('Na','CaT','CaS', 'A', 'KCa', 'Kd', 'H', 'L')
    ylims=[[-500,0],[-5,0],[-50,0],[0,20],[0,30],[0,1000],[-20,20],[-5,15] ]
    fig =figure(figsize=(9,9))
    for mm,c in enumerate(curr[:]):
        clf()
        currents = array(c[1][0:9])
        currents = currents[:,50000:]
        title('currents') 
        for n,i in enumerate(currents):
            subplot(8,1,n+1)
            ylabel(labels[n] + ' [nA]')
            t=linspace(0,len(i)/10000.,len(i))
            plot(t,i,color='black')
            ylim(ylims[n][0],ylims[n][1])
            plt.yticks(linspace(ylims[n][0], ylims[n][1], 5.0))
            xlim(0,5)
            if(n<7): plt.gca().xaxis.set_major_locator(plt.NullLocator())
            #tight_layout(pad=0.4, w_pad=0.4, h_pad=1.0)
            if(n==7):xlabel('time [secs]') 
        fig.subplots_adjust(left=0.3)
        savefig(pathtostore+'temp.'+str(mm)+'.png',dpi=500)


