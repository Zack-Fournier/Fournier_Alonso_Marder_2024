from pylab import *
from scipy import stats
import matplotlib.pyplot as plt

def getSpikesTimes(thres,V):
    times=[]
    for i in arange(0,len(V)-1):
        if(V[i]<thres and V[i+1]>thres):
            times.append(i)
    return array(times)

def getStats(st):
    dc=[]
    ibi=[]
    val=1000
    sb=[]
    eb=[]
    dt=0.1
    fs=[]
    for i in arange(0,len(st)-1):        
        if(i==0 or (st[i]-st[i-1] > val)):
            #print 'burst starts here ', st[i]
            starts= st[i]
            sb.append(st[i])

        if(st[i+1]-st[i] > val):
            #print 'burst ends here ', st[i]
            eb.append(st[i])
            ends = st[i]
            period = float(ends-starts+ st[i+1]-st[i])
            dc.append((ends-starts)/period)
            ibi.append(period)
            fs.append(1000*1./(period*dt))
    return [mean(fs), std(fs), mean(dc),std(dc)]


def getStats_dynamicthres(st):
    dc=[]
    ibi=[]
    # val=1000
    sb=[]
    eb=[]
    dt=0.1
    fs=[]

    isis = []
    for i in range(len(st)-1):  # get all isis and find modes
        time = st[i+1] - st[i]
        time = round(time, -1)
        isis.append(time)

    hist, bins = np.histogram(isis, bins=2)

    # Find the indices of the two highest peaks
    indices = np.argsort(hist)[-2:]
    peak1, peak2 = bins[indices]


    val = (0.5 * (peak1 - peak2)) + peak2

    for i in arange(0,len(st)-1):
        if(i==0 or (st[i]-st[i-1] > val)):
            starts= st[i]
            sb.append(st[i])

        if(st[i+1]-st[i] > val):
            eb.append(st[i])
            ends = st[i]
            period = float(ends-starts+ st[i+1]-st[i])
            dc.append((ends-starts)/period)
            ibi.append(period)
            if period*dt != 0:
                fs.append(1000*1./(period*dt))
            else:
                fs.append(0)

    if all(x for x in isis) == isis[0]:
        dc = zeros([1, 2])
        fs = fs

    if max(isis) - min(isis) < 1000:
        dc = zeros([1, 2])
        fs = fs

    return [mean(fs), std(fs), mean(dc), std(dc)]


def getStatsDt(st,isithres,dt):
    dc=[]
    ibi=[]
    val=isithres/dt
    sb=[]
    eb=[]
    fs=[]
    for i in arange(0,len(st)-1):        
        if(i==0 or (st[i]-st[i-1] > val)):
            starts= st[i]
            sb.append(st[i])        
        if(st[i+1]-st[i] > val):
            eb.append(st[i])
            ends = st[i]
            period = float(ends-starts+ st[i+1]-st[i])
            dc.append((ends-starts)/period)
            ibi.append(period)
            fs.append(1000*1./(period*dt))
    return [mean(fs), std(fs), mean(dc),std(dc)]
import numpy as np


def find_nearby_points(local_maxima_indices, derivative_maxima, derivative_minima, proximity_threshold):
    result_indices = []

    for maxima_idx in local_maxima_indices:
        # Find nearby maxima and minima indices within the proximity threshold
        nearby_maxima = [idx for idx in derivative_maxima if abs(idx - maxima_idx) <= proximity_threshold]
        nearby_minima = [idx for idx in derivative_minima if abs(idx - maxima_idx) <= proximity_threshold]

        # Check if there are both nearby maxima and minima
        if nearby_maxima and nearby_minima:
            # Include the local maxima index in the result
            result_indices.append(maxima_idx)

    return result_indices


# Function to fit a parabola
def parabola(x, a, b, c):
    return a * x**2 + b * x + c

# function to find maxima
def findmaxima(V):
    maxima = []
    dv = diff(V)
    for i in range(len(dv)-1):
        if dv[i] > 0 and dv[i+1] < 0:
            max = int(i+1)
            maxima.append(max)
    return maxima

# function to find minima
def findminima(V):
    minima = []
    dv = diff(V)
    for i in range(len(dv)-1):
        if dv[i] < 0 and dv[i+1] > 0:
            min = int(i+1)
            minima.append(min)
    return minima



def spikefinder(V):

    import numpy as np
    from scipy.ndimage import gaussian_filter1d


    local_maxima_indices = findmaxima(V)
    local_maxima_values = V[local_maxima_indices]

    # Smooth the derivative for better spike detection
    derivative = np.gradient(gaussian_filter1d(V, sigma=1), edge_order=2)

    # Find spikes based on derivative
    high_derivative = findmaxima(derivative)
    low_derivative = findminima(derivative)

    # Filter spikes based on both voltage
    if V.max() > -25:
        Vth = V.max() - 25
    else:
        Vth = -25
    local_maxima_indices = [index for index in local_maxima_indices if V[index] > Vth]

    # Find common indices between local maxima and selected spikes
    proximity_threshold = 50
    common_indices = find_nearby_points(local_maxima_indices, high_derivative, low_derivative, proximity_threshold)

    # Create vector 'st' containing spike times (using index values as time steps)
    st = common_indices

    if abs(V.max()-V.min()) < 20:
        st = []

    return st


def getFreqAndDc(sol):

    dt = 0.1
    V1 = sol[:, 0]
    V2 = sol[:, 1]
    V3 = sol[:, 2]

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

    # align PD
    if len(be1) > len(bs1) and bs1[0] > be1[0]:
        be1 = be1[1:]
    if len(be1) < len(bs1) and bs1[-1] > be1[-1]:
        bs1 = bs1[:-1]
    if len(bs1) > 0 and len(be1) > 0:
        if len(be1) == len(bs1) and bs1[0] > be1[0]:
            bs1 = bs1[:-1]
            be1 = be1[1:]
    # align LP
    if len(be2) > len(bs2) and bs2[0] > be2[0]:
        be2 = be2[1:]
    if len(be2) < len(bs2) and bs2[-1] > be2[-1]:
        bs2 = bs2[:-1]
    if len(bs2) > 0 and len(be2) > 0:
        if len(be2) == len(bs2) and bs2[0] > be2[0]:
            bs2 = bs2[:-1]
            be2 = be2[1:]
    # align PY
    if len(be3) > len(bs3) and bs3[0] > be3[0]:
        be3 = be3[1:]
    if len(be3) < len(bs3) and bs3[-1] > be3[-1]:
        bs3 = bs3[:-1]
    if len(bs3) > 0 and len(be3) > 0:
        if len(be3) == len(bs3) and bs3[0] > be3[0]:
            bs3 = bs3[:-1]
            be3 = be3[1:]


    if(len(st1)>1):
        period = diff(bs1, axis=0)
        period1 = mean(period)
        fs1 = 10000*(1/period)
        dc1 = abs(((be1-bs1)/period1))
        rV1 = [mean(fs1), std(fs1), mean(dc1), std(dc1)]
    else:
        rV1=zeros(4)
    if(len(st2)>1):
        period = diff(bs2, axis=0)
        period2 = mean(period)
        fs2 = 10000*(1/period)
        dc2 = abs(((be2-bs2)/period2))
        rV2 = [mean(fs2), std(fs2), mean(dc2), std(dc2)]
    else:
        rV2=zeros(4)
    if(len(st3)>1):
        period = diff(bs3, axis=0)
        period3 = mean(period)
        fs3 = 10000*(1/period)
        dc3 = abs(((be3-bs3)/period3))
        rV3 = [mean(fs3), std(fs3), mean(dc3), std(dc3)]
    else:
        rV3=zeros(4)

    # double check that arrays were created
    if rV1 is None or len(rV1) == 0:
        rV1=zeros(4)

    if rV2 is None or len(rV2) == 0:
        rV2=zeros(4)

    if rV3 is None or len(rV3) == 0:
        rV3=zeros(4)

    return [rV1,rV2,rV3]
    
    
def getFreqAndDcDt(sol,isithres,dt):
    V1=sol[:,0][int(-len(sol[:,0])/2):]
    V2=sol[:,1][int(-len(sol[:,0])/2):]
    V3=sol[:,2][int(-len(sol[:,0])/2):]
    st1 = getSpikesTimes(-20, V1)
    st2 = getSpikesTimes(-20, V2)
    st3 = getSpikesTimes(-20, V3)
    
    if(len(st1)>1):
        rV1 = getStatsDt(st1,isithres,dt)
    else: rV1=zeros(4)
    if(len(st2)>1):
        rV2 = getStatsDt(st2,isithres,dt)
    else: rV2=zeros(4)
    if(len(st3)>1):
        rV3 = getStatsDt(st3,isithres,dt)
    else: rV3=zeros(4)

    return [rV1,rV2,rV3]


def getPhases(sol):
    V1=sol[:,0]
    V2=sol[:,1]
    V3=sol[:,2]
    st1 = getSpikesTimes(-10, V1)
    st2 = getSpikesTimes(-10, V2)
    st3 = getSpikesTimes(-10, V3)
    
    bs1 = array(st1[::-1][argwhere(diff(st1[::-1])<-1000)])[::-1]           
    be1 = array(st1[argwhere(diff(st1[::1])>1000)]) 
    bs2 = array(st2[::-1][argwhere(diff(st2[::-1])<-1000)])[::-1]           
    be2 = array(st2[argwhere(diff(st2[::1])>1000)])          
    bs3 = array(st3[::-1][argwhere(diff(st3[::-1])<-1000)])[::-1]                      
    be3 = array(st3[argwhere(diff(st3[::1])>1000)])

    if(len(bs1)>1 and len(bs2)>1 and len(bs3)>1):
        for i in range(1):
            if(bs1[0]>be1[0]): 
                be1=be1[1:]
        for i in range(1):
            if(bs2[0]>be2[0]): 
                be2=be2[1:]
        for i in range(1):
            if(bs3[0]>be3[0]): 
                be3=be3[1:]
                
        for i in range(1):
            if(bs1[0]>bs2[0]): 
                bs2=bs2[1:]
                be2=be2[1:]
        for i in range(1):
            if(bs1[0]>bs3[0]): 
                bs3=bs3[1:]
                be3=be3[1:]

        x = bs1
        y = be1
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell1off= r/period 
        
        x = bs1
        y = bs2
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell2on = r/period                         
                                            
        x = bs1
        y = be2
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell2off = r/period                                                                  
                                                                                                                                                                                            
        x = bs1
        y = bs3
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell3on = r/period                                                                                                                                                                                                                                                                                                         
        
        x = bs1
        y = be3
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell3off= r/period

        return [cell1off,cell2on,cell2off,cell3on,cell3off]

#############

def getmeanPhases(sol):
    V1 = sol[:, 0]
    V2 = sol[:, 1]
    V3 = sol[:, 2]

    # get spike times
    st1 = spikefinder(V1)
    st2 = spikefinder(V2)
    st3 = spikefinder(V3)


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

    st1 = np.array(st1)
    st2 = np.array(st2)
    st3 = np.array(st3)

    bs1 = array(st1[::-1][argwhere(diff(st1[::-1]) < -val1)])[::-1]
    be1 = array(st1[argwhere(diff(st1[::1]) > val1)])
    bs2 = array(st2[::-1][argwhere(diff(st2[::-1]) < -val2)])[::-1]
    be2 = array(st2[argwhere(diff(st2[::1]) > val2)])
    bs3 = array(st3[::-1][argwhere(diff(st3[::-1]) < -val3)])[::-1]
    be3 = array(st3[argwhere(diff(st3[::1]) > val3)])


    if (len(bs1) > 1):

        for i in range(1):
            if (bs1[0] > be1[0]):
                be1 = be1[1:]
            if (bs1[0] < be1[0]) and len(bs1) > len(be1):
                bs1 = bs1[:-1]

        if len(bs2) > 1:
            for i in range(1):
                if (bs2[0] > be2[0]):
                    be2 = be2[1:]
                if len(bs2) > len(be2):
                    bs2 = bs2[:-1]
        else:
            be2 = np.zeros([1, 2])

        if len(bs3) > 1:
            for i in range(1):
                if (bs3[0] > be3[0]):
                    be3 = be3[1:]
                if len(bs3) > len(be3):
                    bs3 = bs3[:-1]
        else:
            be3 = np.zeros([1, 2])

        if len(bs2) > 1:
            for i in range(1):
                if (bs1[0] > bs2[0]):
                    bs2 = bs2[1:]
                    be2 = be2[1:]
        else:
            bs2 = np.zeros([1, 2])
            be2 = np.zeros([1, 2])

        if len(bs3) > 1:
            for i in range(1):
                if (bs1[0] > bs3[0]):
                    bs3 = bs3[1:]
                    be3 = be3[1:]
        else:
            bs3 = np.zeros([1, 2])
            be3 = np.zeros([1, 2])

    else:
        bs1 = np.zeros([1, 2])
        be1 = np.zeros([1, 2])
        bs2 = np.zeros([1, 2])
        be2 = np.zeros([1, 2])
        bs3 = np.zeros([1, 2])
        be3 = np.zeros([1, 2])


    # align PD
    if len(be1) > len(bs1) and bs1[0] > be1[0]:
        be1 = be1[1:]
    # if len(be1) > len(bs1) and bs1[0] < bs2[0]:
    #     be1 = be1[:-1]
    if len(be1) < len(bs1) and bs1[-1] > be1[-1]:
        bs1 = bs1[:-1]
    # if len(be1) < len(bs1) and bs1[0] < bs2[0]:
    #     be1 = be1[:-1]
    # align LP
    if len(be2) > len(bs2) and bs2[0] > be2[0]:
        be2 = be2[1:]
    if len(be2) < len(bs2) and bs2[-1] > be2[-1]:
        bs2 = bs2[:-1]
    # align PY
    if len(be3) > len(bs3) and bs3[0] > be3[0]:
        be3 = be3[1:]
    if len(be3) < len(bs3) and bs3[-1] > be3[-1]:
        bs3 = bs3[:-1]


    if not all(be1 == 0):
        x = bs1
        y = be1
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell1offs = r / period
        cell1off_mean = mean(cell1offs)

    else:
        cell1offs = [0]
        cell1off_mean = mean(be1)

    if not all(bs2 == 0):
        x = bs1
        y = bs2
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell2ons = r / period
        cell2on_mean = mean(cell2ons)


    else:
        cell2ons = [0]
        cell2on_mean = mean(bs2)

    if not all(be2 == 0):
        x = bs1
        y = be2
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell2offs = r / period
        cell2off_mean = mean(cell2offs)

    else:
        cell2offs = [0]
        cell2off_mean = mean(be2)

    if not all(bs3 == 0):
        x = bs1
        y = bs3
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell3ons = r / period
        cell3on_mean = mean(cell3ons)

    else:
        cell3ons = [0]
        cell3on_mean = mean(bs3)

    if not all(be3 == 0):
        x = bs1
        y = be3
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell3offs = r / period
        cell3off_mean = mean(cell3offs)

    else:
        cell3offs = [0]
        cell3off_mean = mean(be3)

    # if 2*len(cell2ons) < len(cell1offs) or 2*len(cell2offs) < len(cell1offs) or np.count_nonzero(cell1offs == 0) >= 1:
    if 2 * len(cell2ons) < len(cell1offs) or 2 * len(cell2offs) < len(cell1offs):
        cell2on_mean = 0
        cell2off_mean = 0


    # if 2*len(cell3ons) < len(cell1offs) or 2*len(cell3offs) < len(cell1offs) or np.count_nonzero(cell1offs == 0) >= 1:
    if 2 * len(cell3ons) < len(cell1offs) or 2 * len(cell3offs) < len(cell1offs):
        cell3on_mean = 0
        cell3off_mean = 0

    if cell1off_mean < 0 or cell1off_mean >= 1:
        cell1off_mean = 0

    if cell2on_mean < 0 or cell2on_mean >= 1:
        cell2on_mean = 0

    if cell2off_mean < 0 or cell2off_mean >= 1:
        cell2off_mean = 0

    if cell3on_mean < 0 or cell3on_mean >= 1:
        cell3on_mean = 0

    if cell3off_mean < 0 or cell3off_mean >= 1.1:
        cell3off_mean = 0


    return [cell1off_mean, cell2on_mean, cell2off_mean, cell3on_mean, cell3off_mean]


           
def getPhasesSpikeTimes(st1,st2,st3):
    #V1=sol[:,0][-len(sol[:,0])/2:]
    #V2=sol[:,1][-len(sol[:,0])/2:]
    #V3=sol[:,2][-len(sol[:,0])/2:]
    #st1 = getSpikesTimes(-10, V1)
    #st2 = getSpikesTimes(-10, V2)
    #st3 = getSpikesTimes(-10, V3)

    st1 = np.array(st1)
    st2 = np.array(st2)
    st3 = np.array(st3)
    
    bs1 = array(st1[::-1][argwhere(diff(st1[::-1])<-1000)])[::-1]           
    be1 = array(st1[argwhere(diff(st1[::1])>1000)]) 
    bs2 = array(st2[::-1][argwhere(diff(st2[::-1])<-1000)])[::-1]           
    be2 = array(st2[argwhere(diff(st2[::1])>1000)])          
    bs3 = array(st3[::-1][argwhere(diff(st3[::-1])<-1000)])[::-1]                      
    be3 = array(st3[argwhere(diff(st3[::1])>1000)])          
    if(len(bs1)>1 and len(bs2)>1 and len(bs3)>1):
        for i in range(1):
            if(bs1[0]>be1[0]): 
                be1=be1[1:]
        for i in range(1):
            if(bs2[0]>be2[0]): 
                be2=be2[1:]
        for i in range(1):
            if(bs3[0]>be3[0]): 
                be3=be3[1:]
                
        for i in range(1):
            if(bs1[0]>bs2[0]): 
                bs2=bs2[1:]
                be2=be2[1:]
        for i in range(1):
            if(bs1[0]>bs3[0]): 
                bs3=bs3[1:]
                be3=be3[1:]        
        #this one is wrong. no reason to remove burst from 3 if they come before 2
        #for i in range(1):
        #    if(bs2[0]>bs3[0]): 
        #        bs3=bs3[1:]
        #        be3=be3[1:]
        x = bs1
        y = be1
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell1off= r/period 
        
        x = bs1
        y = bs2
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell2on = r/period                         
                                            
        x = bs1
        y = be2
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell2off = r/period                                                                  
                                                                                                                                                                                            
        x = bs1
        y = bs3
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell3on = r/period                                                                                                                                                                                                                                                                                                         
        
        x = bs1
        y = be3
        aux=min(len(x),len(y))
        xx =array(x[:aux])
        yy =array(y[:aux])
        r=mean(yy-xx)
        period=mean(diff(bs1,axis=0))
        cell3off= r/period
        return [cell1off,cell2on,cell2off,cell3on,cell3off]


def getPhases_wStd(sol):
    V1 = sol[:, 0]
    V2 = sol[:, 1]
    V3 = sol[:, 2]

    # get dynamic threshold
    PD_thres = max(sol[:, 0]) - 0.25 * (max(sol[:, 0]) - min(sol[:, 0]))
    if max(sol[:, 0]) < -25:
        PD_thres = -25
    LP_thres = max(sol[:, 1]) - 0.25 * (max(sol[:, 1]) - min(sol[:, 1]))
    if max(sol[:, 1]) < -25:
        LP_thres = -25
    PY_thres = max(sol[:, 2]) - 0.25 * (max(sol[:, 2]) - min(sol[:, 2]))
    if max(sol[:, 2]) < -25:
        PY_thres = -25


    # get spike times
    st1 = getSpikesTimes(PD_thres, sol[:, 0])
    st2 = getSpikesTimes(LP_thres, sol[:, 1])
    st3 = getSpikesTimes(PY_thres, sol[:, 2])

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

    # print(isis3)

    if val1 > 3000:
        val1 = 1500
    if val2 > 3000:
        val2 = 1500
    if val3 > 3000:
        val3 = 1500

    bs1 = array(st1[::-1][argwhere(diff(st1[::-1]) < -val1)])[::-1]
    be1 = array(st1[argwhere(diff(st1[::1]) > val1)])
    bs2 = array(st2[::-1][argwhere(diff(st2[::-1]) < -val2)])[::-1]
    be2 = array(st2[argwhere(diff(st2[::1]) > val2)])
    bs3 = array(st3[::-1][argwhere(diff(st3[::-1]) < -val3)])[::-1]
    be3 = array(st3[argwhere(diff(st3[::1]) > val3)])

    if (len(bs1) > 1):

        for i in range(1):
            if (bs1[0] > be1[0]):
                be1 = be1[1:]
            if (bs1[0] < be1[0]) and len(bs1) > len(be1):
                bs1 = bs1[:-1]

        if len(bs2) > 1:
            for i in range(1):
                if (bs2[0] > be2[0]):
                    be2 = be2[1:]
                if len(bs2) > len(be2):
                    bs2 = bs2[:-1]
        else:
            be2 = np.zeros([1, 2])

        if len(bs3) > 1:
            for i in range(1):
                if (bs3[0] > be3[0]):
                    be3 = be3[1:]
                if len(bs3) > len(be3):
                    bs3 = bs3[:-1]
        else:
            be3 = np.zeros([1, 2])

        if len(bs2) > 1:
            for i in range(1):
                if (bs1[0] > bs2[0]):
                    bs2 = bs2[1:]
                    be2 = be2[1:]
        else:
            bs2 = np.zeros([1, 2])
            be2 = np.zeros([1, 2])

        if len(bs3) > 1:
            for i in range(1):
                if (bs1[0] > bs3[0]):
                    bs3 = bs3[1:]
                    be3 = be3[1:]
        else:
            bs3 = np.zeros([1, 2])
            be3 = np.zeros([1, 2])

    else:
        bs1 = np.zeros([1, 2])
        be1 = np.zeros([1, 2])
        bs2 = np.zeros([1, 2])
        be2 = np.zeros([1, 2])
        bs3 = np.zeros([1, 2])
        be3 = np.zeros([1, 2])


    if not all(be1 == 0):
        x = bs1
        y = be1
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell1offs = r / period
        cell1off_mean = mean(cell1offs)
        cell1off_std = std(cell1offs)
    else:
        cell1offs = [0]
        cell1off_mean = mean(be1)
        cell1off_std = std(be1)

    if not all(bs2 == 0):
        x = bs1
        y = bs2
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell2ons = r / period
        cell2on_mean = mean(cell2ons)
        cell2on_std = std(cell2ons)
    else:
        cell2ons = [0]
        cell2on_mean = mean(bs2)
        cell2on_std = std(bs2)

    if not all(be2 == 0):
        x = bs1
        y = be2
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell2offs = r / period
        cell2off_mean = mean(cell2offs)
        cell2off_std = std(cell2offs)
    else:
        cell2offs = [0]
        cell2off_mean = mean(be2)
        cell2off_std = std(be2)

    if not all(bs3 == 0):
        x = bs1
        y = bs3
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell3ons = r / period
        cell3on_mean = mean(cell3ons)
        cell3on_std = std(cell3ons)
    else:
        cell3ons = [0]
        cell3on_mean = mean(bs3)
        cell3on_std = std(bs3)

    if not all(be3 == 0):
        x = bs1
        y = be3
        aux = min(len(x), len(y))
        xx = array(x[:aux])
        yy = array(y[:aux])
        r = yy - xx
        period = diff(bs1, axis=0)
        aux2 = min(len(r), len(period))
        r = array(r[:aux2])
        period = array(period[:aux2])
        cell3offs = r / period
        cell3off_mean = mean(cell3offs)
        cell3off_std = std(cell3offs)
    else:
        cell3offs = [0]
        cell3off_mean = mean(be3)
        cell3off_std = std(be3)

    if cell1off_mean == 0:
        cell1off_mean = 0
        cell2on_mean = 0
        cell2off_mean = 0
        cell3on_mean = 0
        cell3off_mean = 0
        cell1off_std = 0
        cell2on_std = 0
        cell2off_std = 0
        cell3on_std = 0
        cell3off_std = 0

    if 2*len(cell2ons) < len(cell1offs) or 2*len(cell2offs) < len(cell1offs) or np.count_nonzero(cell1offs == 0) >= 1:
        cell2on_mean = 0
        cell2off_mean = 0
        cell2on_std = 0
        cell2off_std = 0

    if 2*len(cell3ons) < len(cell1offs) or 2*len(cell3offs) < len(cell1offs) or np.count_nonzero(cell1offs == 0) >= 1:
        cell3on_mean = 0
        cell3off_mean = 0
        cell3on_std = 0
        cell3off_std = 0

    if cell1off_mean < 0 or cell1off_mean >= 1:
        cell1off_mean = 0
        cell1off_std = 0

    if cell2on_mean < 0 or cell2on_mean >= 1:
        cell2on_mean = 0
        cell2on_std = 0

    if cell2off_mean < 0 or cell2off_mean >= 1:
        cell2off_mean = 0
        cell2off_std = 0

    if cell3on_mean < 0 or cell2on_mean >= 1:
        cell3on_mean = 0
        cell3on_std = 0

    if cell3off_mean < 0 or cell3off_mean >= 1:
        cell3off_mean = 0
        cell3off_std = 0


    return [cell1off_mean, cell2on_mean, cell2off_mean, cell3on_mean, cell3off_mean, cell1off_std, cell2on_std, cell2off_std, cell3on_std, cell3off_std]