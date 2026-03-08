from pylab import *


def getSpikesTimes(thres,V):
    times=[]
    for i in arange(0,len(V)-1):
        if(V[i]<thres and V[i+1]>thres):
            times.append(i)
    return array(times)


def getDownwardCrossings(thres,V):
    times=[]
    for i in arange(0,len(V)-1):
        if(V[i]>thres and V[i+1]<=thres):
            times.append(i)
    return array(times)

def getStats(st,isithres,dt):
    #dt=0.1
    dc=[]
    ibi=[]
    val=isithres/dt
    sb=[]
    eb=[]
    fs=[]
    started=False
#    print(len(st))
    for i in arange(1,len(st)-1):        
        if((st[i]-st[i-1] > val)):
            #print 'burst starts here ', st[i]
            starts= st[i]
            sb.append(st[i])        
            started=True
        if(st[i+1]-st[i] > val):
            #print 'burst ends here ', st[i]
            if(started):
                eb.append(st[i])
                ends = st[i]
                period = float(ends-starts+ st[i+1]-st[i])
                #print period
                dc.append((ends-starts)/period)
                ibi.append(period)
                fs.append(1000*1./(period*dt))
    #return [mean(fs), std(fs), mean(dc),std(dc)]
    return [fs, dc]

