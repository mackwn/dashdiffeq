# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 13:07:24 2019

@author: smcko
"""

import numpy as np
import matplotlib.pyplot as plt

class parabolic1d():
    def __init__(self,n,xlength,uo,uto,k):
        ### input data 
        n = int(round(n)) #round
        ### data validation
        if False in [type(arg) in [int,float] for arg in [n,xlength,uo,uto,k]]:
            raise TypeError('All inputs must be numeric (float or integer)')
        if True in [arg < 0 for arg in [n,xlength,uo,uto,k]]:
            raise ValueError('Negative inputs not allowed')
        if n < 2: raise ValueError('n must be equal or greater than 2')  
        if not .0001 < k < 1000: raise ValueError('k must be between .0001W/m^2 and 1,000W/m^2')
        if uo > uto: raise ValueError('uo (x=0, t=t) must be greater than uto (x=x, t=0)')
        #if not uo < uf < uto: raise ValueError('uf (x=X, t=t) must be between uo (x=0, t=t) and uto (x=x,t=0)')


        ### assignments
        self.n = n
        self.xlength = xlength
        self.uo = uo#uto *uper
        self.uto = uto
        self.uf = uto
        self.k = k
        

    def _centdiffd2mat(self):
        #mat = np.zeros((n-1,n-1))
        diag = np.zeros(self.n-1) + 2
        diag_1 = np.zeros(self.n-2) - 1
        amat = np.diagflat(diag) + np.diagflat(diag_1,k=1) + np.diagflat(diag_1,k=-1)
        return amat

    def _genbcvec(self):
        bcvec = np.zeros(self.n-1)
        bcvec[0] = -self.uo
        bcvec[-1] = -self.uf
        return bcvec


    def _setup_ugrid(self):
        ugrid = np.zeros(self.n+1)
        ugrid[0]= self.uo
        ugrid[1:-1] = self.uto
        self.ugrid = ugrid

    def _setup_xgrid(self):
        self.xgrid = np.linspace(0,xlength,self.n+1)
        self.delx = abs(xgrid[0]-xgrid[1])
        

   
    def _implicit_timestep(self,ugrid):
        idmat = np.diagflat(np.zeros(self.n-1)+1)
        invmat = np.linalg.inv((idmat+delt*self.amat))
        return np.dot(invmat,ugrid[1:-1]-self.bcvec*self.delt)

    def _explicit_timestep():
        pass


    def setup(self):
        self._setup_xgrid()
        self._setup_ugrid
        self.amat = self._centdiffd2mat() * self.k/(self.delx**2)
        self.bcvec = self._genbcvec() * (self.k/self.delx**2)
    
    def solve(self,delt,ufper,method='implicit',maxtsteps = 50000):
        
        self.delt = delt
        self.ufper = ufper

        ugrid0 = self.ugrid
        self.i=0
        maxtsteps = 50000
        
        ugrid_out = ugrid0

        while ((self.uf-self.uo)/(self.uto-self.uo) > ufper) and (self.i<maxtsteps):

            ugrid1 = ugrid0
            uf= ugrid0[-2] #no flow boundary
            ugrid1[-1] = uf
            self.bcvec = self._genbcvec() * (self.k/self.delx**2)
            ugrid1[1:-1] = self._implicit_timestep(ugrid0)
            ugrid0=ugrid1
            self.i+=1
            ugrid_out = np.row_stack((ugrid_out,ugrid0))

        self.ugrid_out = ugrid_out


    
   
   


def parab1dimp(xlength,delt,n,uo_per,uto,ufper,k):

    def centdiffd2mat(n):
        #mat = np.zeros((n-1,n-1))
        diag = np.zeros(n-1) + 2
        diag_1 = np.zeros(n-2) - 1
        mat = np.diagflat(diag) + np.diagflat(diag_1,k=1) + np.diagflat(diag_1,k=-1)
        return mat
        
    def genbcvec(n,delx,uo,uf,k):
        bcvec = np.zeros(n-1)
        bcvec[0] = -uo
        bcvec[-1] = -uf
        return bcvec*(k/delx**2)


    test = False ##bring commands to debugging

    print('past imports')
    #set u at x=0 based on percentage of initial temp
    uo = uo_per * uto
    ###Spatial grid
    n = int(round(n))
    xgrid = np.linspace(0,xlength,n+1)
    delx = abs(xgrid[0]-xgrid[1])
    ugrid = np.zeros(n+1)
    ugrid[0]= uo
    ugrid[-1] = uto
    if test==True: print('xgrid',xgrid)
    print('grids set up')
    ###Temporal grid
    #tgrid = np.linspace(0,tspan,tsteps+1)
    #delt = abs(tgrid[0]-tgrid[1])
    #print('delt:',delt)
    #if test == True: print('tgrid',tgrid)
    ugrid[1:-1] = uto

    ###Create A matrix
    amat = centdiffd2mat(n) * k/(delx**2) ##calculate matrix assuming central difference for 2nd deriv
    if test==True: print(centdiffd2mat(n))
    if test==True: print(amat)
    print('set up a mat')
    ugrid0 = ugrid

    i=0
    maxtsteps = 50000
    #ufper=.25
    uf = uto
    ugrid_out = ugrid0

    print('time loop started')
    while ((uf-uo)/(uto-uo) > ufper) and (i<maxtsteps):
        #ugrid0 = ugrid1
        ugrid1 = ugrid0
        uf= ugrid0[-2] #no flow boundary
        ugrid1[-1] = uf
        bcvec = genbcvec(n,delx,uo,uf,k)
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
    #finished time loop
    return xgrid,ugrid_out

if __name__ == "__main__":
    xlength = 70
    tspan = 100
    tsteps = 300
    n = 2
    uo_per = .2
    uf = 500
    uto = 500
    k=.5
    delt = .5
    ufper = .7
    xgrid, ugrid_out = parab1dimp(xlength,delt,n,uo_per,uto,ufper,k)  
    print(xgrid)
    print(ugrid_out)
    tframes = list(range(0,len(ugrid_out[:,0]),100))
    for tframe in tframes:
        plt.plot(xgrid,ugrid_out[tframe,:])
    print(ugrid_out.shape)
    plt.show()