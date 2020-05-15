# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 13:07:24 2019

@author: smcko
"""

import numpy as np
import matplotlib.pyplot as plt

xlength = 70
tspan = 100
tsteps = 300
n = 100
uo = 1
uf = 500
uto = 500
k=1
delt = .333
ufper = .7

def parab1dimp(xlength,delt,n,uo,uto,ufper,k):

    def centdiffd2mat(n):
        #mat = np.zeros((n-1,n-1))
        diag = np.zeros(n-1) + 2
        diag_1 = np.zeros(n-2) - 1
        mat = np.diagflat(diag) + np.diagflat(diag_1,k=1) + np.diagflat(diag_1,k=-1)
        return mat
        
    def genbcvec(n,delx,uo,uf):
        bcvec = np.zeros(n-1)
        bcvec[0] = -uo
        bcvec[-1] = -uf
        return bcvec*(1/delx**2)

    def dx2elliptic1d(x):
        return x**2

    test = False ##bring commands to debugging


    ###Spatial grid
    xgrid = np.linspace(0,xlength,n+1)
    delx = abs(xgrid[0]-xgrid[1])
    ugrid = np.zeros(n+1)
    ugrid[0]= uo
    ugrid[-1] = uto
    if test==True: print('xgrid',xgrid)

    ###Temporal grid
    #tgrid = np.linspace(0,tspan,tsteps+1)
    #delt = abs(tgrid[0]-tgrid[1])
    #print('delt:',delt)
    #if test == True: print('tgrid',tgrid)
    ugrid[1:-1] = uto

    ###Create A matrix
    amat = centdiffd2mat(n) * 1/(delx**2) ##calculate matrix assuming central difference for 2nd deriv
    if test==True: print(centdiffd2mat(n))
    if test==True: print(amat)

    ugrid0 = ugrid

    i=0
    maxtsteps = 50000
    #ufper=.25
    uf = uto
    ugrid_out = ugrid0

    while (uf/uto > ufper) and (i<maxtsteps):
        #ugrid0 = ugrid1
        ugrid1 = ugrid0
        uf= ugrid0[-2] #no flow boundary
        ugrid1[-1] = uf
        bcvec = genbcvec(n,delx,uo,uf)
        idmat = np.diagflat(np.zeros(n-1)+1)
        invmat = np.linalg.inv((idmat+delt*amat))
        ugrid1[1:-1] = np.dot(invmat,ugrid0[1:-1]-bcvec*delt)
        ugrid0=ugrid1
        #if i < 10:
            #plt.plot(xgrid,ugrid1)
        #if i<250:
        # if i%50==0:plt.plot(xgrid,ugrid1)
       # elif i%250==0: 
            #plt.plot(xgrid,ugrid1)
        # print('uavg:',ugrid1.mean())
        i+=1
        ugrid_out = np.row_stack((ugrid_out,ugrid0))

    #plt.show()
    return xgrid,ugrid_out


xgrid, ugrid_out = parab1dimp(xlength,delt,n,uo,uto,ufper,k)  