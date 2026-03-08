#from pylab import *
import numpy as np
from numpy import *

# This script is ver similar to the java class singleCompTemperature_slow_explicit.java
# Define the steady state activation/inactivation functions

def boltzSS(Volt, A, B):
    act = 1./(1. + np.exp((Volt + A)/B))
    return act


# time constant function
def tauX(Volt, CT, DT, AT, BT):
    timeconst = CT - DT/(1. + np.exp((Volt + AT)/BT))
    return timeconst


# special time constant function
def spectau(Volt, CT, DT, AT, BT, AT2, BT2):
    spec = CT + DT/(np.exp((Volt + AT)/BT) + np.exp((Volt + AT2)/BT2))
    return spec


# ionic currents
# q is the exponent of the activation variable m
def iIonic(g, m, h, q, Volt, Erev):
    flux = g*pow(m, q)*h*(Volt - Erev)
    return flux

# synaptic currents
def iSyn(gsyn, sact,Vpost,Esyn):
    isyn = gsyn*sact*(Vpost - Esyn)
    return isyn

# nernst equation
def CaNernst(CaIn, temp):
    R = 8.314*pow(10, 3)  # Ideal Gas Constant (*10^3 to put into mV)
    T = 273.15 + temp  # Temperature in Kelvin
    z = 2.0  # Valence of Caclium Ions
    Far = 96485.33  # Faraday's Constant
    CaOut = 3000.0  # Outer Ca Concentration (uM)
    CalRev = ((R*T)/(z*Far))*np.log(CaOut/CaIn)
    #print 'calrev ', CalRev
    return CalRev
    
def model(v,p,temp):
    reftemp=10
    V = v[:,0]
    NaM = v[:,1]
    NaH = v[:,2]
    CaTM = v[:,3]
    CaTH = v[:,4]
    CaSM = v[:,5]
    CaSH = v[:,6]
    HM = v[:,7]
    KdM = v[:,8]
    KCaM = v[:,9]
    AM = v[:,10]
    AH = v[:,11]
    IMIM = v[:,12]
    IntCa = v[:, 13]


    CaRev = CaNernst(IntCa, temp)
    C = 1.  # Capacitance (uF / cm^2)

    #fixed parameters
    Area = 0.628
    caF = 0.94
    Ca0 = 0.05

    # activation timescale of IMI
    tauIMI = 20

    tauIntCa = p[38]*10  # Calcium buffer time constant (ms)
    # Equilibrium Points of Calcium Sensors
    # p_g=[gNa, gCaT,gCaS,gA,gKCa,gKd,gH,g_leak]

# Fixed Maximal Conductances
    gNa  = p[0]    # Transient Sodium Maximal Conductance
    gCaT = p[1]    # Low Threshold Calcium Maximal Conductance
    gCaS = p[2]    # Slow Calcium Maximal Conductance
    gA   = p[3]    # Transient Potassium Maximal Conductance
    gKCa = p[4]    # Calcium Dependent Potassium Maximal Conductance
    gKd  = p[5]    # Potassium Maximal Conductance
    gH   = p[6]    # Hyperpolarization Activated Cation Maximal Conductance
    gL   = p[7]    # Leak Maximal Conductance
    gIMI = p[8]    # Neuromodulatory (IMI) Maximal Conductance

# p_Erev = [e_leak,e_na,e_k,e_h]
    EL = p[9]   # Leak Reversal Potential
    ENa = p[10]  # Sodium Reversal Potential
    ECaT = CaRev    # Low Threshold Calcium Reversal Potential
    ECaS = CaRev    # Slow Calcium Reversal Potential

    EIMI = -10    # IMI reversal potential
    EKd = p[11]   # Potassium Reversal Potential
    EKCa = p[11]  # Calcium Dependent Potassium Reversal Potential
    EA = p[11]    # Transient Potassium Reversal Potential
    
    EH = p[12]    # Hyperpolarization Activated Cation Reversal Potential
    
    # p_q10=[q10_gNa , q10_gNa_m , q10_gNa_h,q10_gCaT,q10_gCaT_m,q10_gCaT_h,q10_gCaS,q10_gCaS_m,q10_gCaS_h,q10_gA,q10_gA_m,q10_gA_h, q10_gKCa,q10_gKCa_m,q10_gKCa_h ,q10_gKdr,q10_gKdr_m,q10_gKdr_h,q10_gH,q10_gH_m,q10_gH_h, q10_g_leak,q10_tau_Ca]
    # p_q10=[
    q10_gNa 	= p[13]
    q10_gNa_m	= p[14]
    q10_gNa_h	= p[15]
    
    q10_gCaT 	= p[16]
    q10_gCaT_m	= p[17]
    q10_gCaT_h	= p[18]
    
    q10_gCaS 	= p[19]
    q10_gCaS_m	= p[20]
    q10_gCaS_h	= p[21]
    
    q10_gA = p[22]
    q10_gA_m = p[23]
    q10_gA_h = p[24]
    
    q10_gKCa   = p[25]
    q10_gKCa_m = p[26]
    q10_gKCa_h = p[27]
    
    q10_gKdr   = p[28]
    q10_gKdr_m = p[29]
    q10_gKdr_h = p[30]
    
    q10_gH   = p[31]
    q10_gH_m = p[32]
    q10_gH_h = p[33]
    
    q10_g_leak	= p[34]

    q10_g_imi   = p[35]
    q10_g_imi_m = p[36]
    q10_tau_Ca	= p[37]


    Iapp = p[39]

    # Steady State Gating Variables
    NaMinf  = boltzSS(V, 25.5, -5.29)  # m^3
    NaHinf  = boltzSS(V, 48.9, 5.18)  # h
    CaTMinf = boltzSS(V, 27.1, -7.20)  # m^3
    CaTHinf = boltzSS(V, 32.1, 5.50)  # h
    CaSMinf = boltzSS(V, 33.0, -8.1)  # m^3
    CaSHinf = boltzSS(V, 60.0, 6.20)  # h
    HMinf   = boltzSS(V, 70.0, 6.0)  # m
    KdMinf  = boltzSS(V, 12.3, -11.8)  # m^4
    KCaMinf = (IntCa/(IntCa + 3.0))*boltzSS(V, 28.3, -12.6)  # m^4
    AMinf   = boltzSS(V, 27.2, -8.70)  # m^3
    AHinf   = boltzSS(V, 56.9, 4.90)  # h
    IMIMinf = boltzSS(V, 55, -5)

    # Time Constants (ms)
    tauNaM 	= tauX(V, 1.32, 1.26, 120.0, -25.0) 																 	
    tauNaM = tauNaM * pow(q10_gNa_m, 		-(temp-reftemp)/10.)
    tauNaH 	= tauX(V, 0.0, -0.67, 62.9, -10.0)*tauX(V, 1.50, -1.00, 34.9, 3.60) 	
    tauNaH = tauNaH * pow(q10_gNa_h,-(temp-reftemp)/10.)
    tauCaTM 	= tauX(V, 21.7, 21.3, 68.1, -20.5) 																	
    tauCaTM= tauCaTM*	pow(q10_gCaT_m, 	-(temp-reftemp)/10.)
    tauCaTH 	= tauX(V, 105.0, 89.8, 55.0, -16.9)																	
    tauCaTH= tauCaTH*	pow(q10_gCaT_h,	  -(temp-reftemp)/10.)
    tauCaSM 	= spectau(V, 1.40, 7.00, 27.0, 10.0, 70.0, -13.0)										
    tauCaSM= tauCaSM* pow(q10_gCaS_m, 	-(temp-reftemp)/10.)
    tauCaSH 	= spectau(V, 60.0, 150.0, 55.0, 9.00, 65.0, -16.0)										
    tauCaSH= tauCaSH* pow(q10_gCaS_h,	  -(temp-reftemp)/10.)
    tauHM 		= tauX(V, 272.0, -1499.0, 42.2, -8.73)																
    tauHM	 = tauHM  * pow(q10_gH_m,  	  -(temp-reftemp)/10.)
    tauKdM		= tauX(V, 7.20, 6.40, 28.3, -19.2)																		
    tauKdM = tauKdM * pow(q10_gKdr_m, 	-(temp-reftemp)/10.)
    tauKCaM 	= tauX(V, 90.3, 75.1, 46.0, -22.7)																		
    tauKCaM= tauKCaM* pow(q10_gKCa_m ,	-(temp-reftemp)/10.)
    tauAM 		= tauX(V, 11.6, 10.4, 32.9, -15.2)																	
    tauAM	 = tauAM  * pow(q10_gA_m,-(temp-reftemp)/10.)
    tauAH 		= tauX(V, 38.6, 29.2, 38.9, -26.5)																	  
    tauAH	 = tauAH  * pow(q10_gA_h,-(temp-reftemp)/10.)
    tauIMI = tauIMI * pow(q10_g_imi_m,(temp-reftemp)/10.)

    # cout<<pow(q10_gNa_m, 		(temp-reftemp)/10.)<<endl
    gNa  = gNa	* pow(q10_gNa, 		(temp-reftemp)/10.)
    gCaT = gCaT * pow(q10_gCaT, 	(temp-reftemp)/10.)
    gCaS = gCaS	* pow(q10_gCaS, 	(temp-reftemp)/10.)
    gA   = gA  	* pow(q10_gA, 		(temp-reftemp)/10.)
    gKCa = gKCa	* pow(q10_gKCa, 	(temp-reftemp)/10.)
    gKd  = gKd  * pow(q10_gKdr, 	(temp-reftemp)/10.)
    gH   = gH   * pow(q10_gH, 		(temp-reftemp)/10.)
    gL   = gL   * pow(q10_g_leak,       (temp-reftemp)/10.)
    gIMI = gIMI * pow(q10_g_imi, (temp-reftemp)/10.)

    tauIntCa = tauIntCa * pow(q10_tau_Ca, -(temp-reftemp)/10.)

# Ionic Currents (mV / ms)
    iNa  = 	iIonic(gNa	, NaM	, NaH	, 3	, V, ENa)*Area
    iCaT = 	iIonic(gCaT	, CaTM, CaTH, 3	, V, ECaT)*Area
    iCaS = 	iIonic(gCaS	, CaSM, CaSH, 3	, V, ECaS)*Area
    iH   = 	iIonic(gH		, HM	, 1		, 1	, V, EH)*Area
    iKd  = 	iIonic(gKd	, KdM	, 1		, 4	, V, EKd)*Area
    iKCa = 	iIonic(gKCa	, KCaM, 1		, 4	, V, EKCa)*Area
    iA   = 	iIonic(gA		, AM	, AH	, 3	, V, EA)*Area
    iL   = 	iIonic(gL		, 1		, 1		, 1	, V, EL)*Area
    iIMI = iIonic(gIMI   , IMIM,   1,  1,  V, EIMI)
    
    labels = ('gNa', 'gCaT', 'gCaS', 'gA', 'gKCa', 'gKd', 'gH', 'gL', 'gIMI')
    r = [iNa,iCaT,iCaS,iA,iKCa,iKd,iH,iL,iIMI]
    return r

def getSynCurrents(sol, p, temp):
    cell1 = sol[:,0:14]
    cell2 = sol[:,14:14*2]
    cell3 = sol[:,14*2:14*3]
    reftemp=10
    syn = sol[:,14*3:(14*3)+7]
    VABPD = cell1[:,0]
    VLP = cell2[:,0]
    VPY = cell3[:,0]

    Eglut = -70.0
    Echol = -80.0
    pdim = 40
    syn_q10 = p[3*pdim + (7): 3*pdim + (7)+(7*2)];
	    
    ABPYglut=syn[:,0]
    ABPYchol=syn[:,1]
    ABLPglut=syn[:,2]
    ABLPchol=syn[:,3]
    LPPYglut=syn[:,4]
    PYLPglut=syn[:,5]
    LPABglut=syn[:,6]
    g_syn =p[3*pdim: (3*pdim) + 7]

    iABPYglut = iSyn(pow(syn_q10[0],(temp-reftemp)/10.) * g_syn[0], ABPYglut, VPY, Eglut);
    iABPYchol = iSyn(pow(syn_q10[1],(temp-reftemp)/10.) * g_syn[1], ABPYchol, VPY,  Echol);
    iABLPglut = iSyn(pow(syn_q10[0],(temp-reftemp)/10.) * g_syn[2], ABLPglut, VLP, Eglut);
    iABLPchol = iSyn(pow(syn_q10[1],(temp-reftemp)/10.) * g_syn[3], ABLPchol, VLP, Echol);
    iLPPYglut = iSyn(pow(syn_q10[0],(temp-reftemp)/10.) * g_syn[4], LPPYglut, VPY,   Eglut);
    iPYLPglut = iSyn(pow(syn_q10[0],(temp-reftemp)/10.) * g_syn[5], PYLPglut, VLP, Eglut);
    iLPABglut = iSyn(pow(syn_q10[0],(temp-reftemp)/10.) * g_syn[6], LPABglut, VABPD, Eglut);
    return [iABPYglut,iABPYchol,iABLPglut,iABLPchol,iLPPYglut,iPYLPglut,iLPABglut]
    
