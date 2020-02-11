# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 13:07:24 2019

@author: smcko
"""

import numpy as np
import matplotlib.pyplot as plt
#import math as mt
#import pandas as pd

def elliptic2dsolve(xlength,ylength,ux,uy,q,k,m,n):
    def centdiffd2mat2d(m,n,delx,dely):
        #mat = np.zeros((n-1,n-1))

        cols = n*m

        diag = (np.zeros(cols) + 2)*(1/delx**2+1/dely**2)
        #print("diag:",diag.size)
        xdiag = (np.zeros(cols-n)-1)*(1/delx**2)
        #print("xdiag:",xdiag.size)
        ydiag = (np.array(([-1]*(n-1)+[0])*(m-1)+[-1]*(n-1)))*(1/dely**2)
        #print("ydiag:",ydiag.size)

        #print(diag_mults)

        mat = np.diagflat(diag) + np.diagflat(xdiag,k=n) + np.diagflat(xdiag,k=-n) + np.diagflat(ydiag,k=1) + np.diagflat(ydiag,k=-1)
        
        
        return mat

    def dx2elliptic2d(X,Y,q):
        return X*0+q#X+Y

    def createuovec(ugrid,delx,dely):
        ugrid[1,1:-1] -= ugrid[0,1:-1]/dely**2
        ugrid[-2,1:-1] -= ugrid[-1,1:-1]/dely**2
        ugrid[1:-1,1] -= ugrid[1:-1,0]/delx**2
        ugrid[1:-1,-2] -= ugrid[1:-1,-1]/delx**2
        return np.reshape(ugrid[1:-1,1:-1],ugrid[1:-1,1:-1].size)

    test = False ##bring commands to debugging
    # xlength = xlen
    # ylength = ylen
    # n = 20
    # m = 20
    ugrid = np.zeros((m+1,n+1))
    # uxo = 1
    # uxf = 2
    # uyo = 3
    # uyf = 10
    ugrid[:,0] = ux[0]
    ugrid[:,-1] = ux[1]
    ugrid[0,:] = uy[0]
    ugrid[-1,:] = uy[1]


    x = np.linspace(0,xlength,m+1)
    y = np.linspace(0,ylength,n+1)
    if test==True: print('x',x,'y',y)
    ygrid,xgrid = np.meshgrid(y,x)


    #print(xgrid)
    #print(ygrid)


    #xygrid = np.tile(xgrid,n+1).reshape((n+1,n+1))
    delx = abs(x[0]-x[1])
    dely = abs(y[0]-y[1])
    if test==True: print('delx',delx,'dely',dely)




    #ugrid[0]= uo
    #ugrid[-1] = uf
    #Y, X = np.meshgrid(xgrid[1:-1],xgrid[1:-1])

    #if test==True: print(xygrid)

    amat = centdiffd2mat2d(m-1,n-1,delx,dely) ##calculate matrix assuming central difference for 2nd deriv
    #if test==True: print(centdiffd2mat2d(n))
    if test==True: print("AMAT",amat)

    fmat = dx2elliptic2d(xgrid[1:-1,1:-1],ygrid[1:-1,1:-1],q)
    fvec = np.resize(fmat, fmat.size) ##calculate f(x)
    #uovec = np.zeros(fvec.size)
    uovec = createuovec(ugrid,delx,dely) #vector for boundary condition

    if test==True: print("FMAT",fmat)
    amatinv = np.linalg.inv(amat)
    #if test==True: print(amatinv)

    #k = .0001
    uout = np.dot(amatinv,fvec*(1/k)-uovec)
    if test==True: print(uout.reshape((m-1,n-1)))

    ugrid[1:-1,1:-1] = uout.reshape((m-1,n-1))

    return xgrid,ygrid,ugrid

#print(uout.reshape((n-1,n-1)))
# xgrid,ygrid,ugrid = elliptic2dsolve(3,4,[500,500],[1000,500],.1,5,5)
# plt.contourf(xgrid,ygrid,ugrid)
# plt.colorbar()
# print(xgrid)
# print(ygrid)
# print(ugrid)
# plt.show()