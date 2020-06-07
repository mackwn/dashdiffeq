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
        ugrid[1:] = self.uto
        self.ugrid = ugrid

    def _setup_xgrid(self):
        self.xgrid = np.linspace(0,self.xlength,self.n+1)
        self.delx = abs(self.xgrid[0]-self.xgrid[1])
        

   
    def _implicit_timestep(self,ugrid):
        idmat = np.diagflat(np.zeros(self.n-1)+1)
        invmat = np.linalg.inv((idmat+self.delt*self.amat))
        return np.dot(invmat,ugrid[1:-1]-self.bcvec*self.delt)

    def _explicit_timestep():
        pass


    def setup(self):
        self._setup_xgrid()
        self._setup_ugrid()
        self.amat = self._centdiffd2mat() * self.k/(self.delx**2)
        self.bcvec = self._genbcvec() * (self.k/self.delx**2)
    
    def solve(self,delt,ufper,method='implicit',maxtsteps = 50000):

        if not (1 < delt <= 100): raise ValueError('Time step must be between 1 and 100')
        if not (.05 < ufper <= .95): raise ValueError('Percent decrease in temperature must be between 0.5 and 0.95')
        
        self.delt = delt
        self.ufper = ufper

        ugrid0 = self.ugrid
        self.i=0
        maxtsteps = 50000
        
        ugrid_out = ugrid0

        while ((self.uf-self.uo)/(self.uto-self.uo) > ufper) and (self.i<maxtsteps):

            ugrid1 = ugrid0
            self.uf= ugrid0[-2] #no flow boundary
            ugrid1[-1] = ugrid0[-2]
            self.bcvec = self._genbcvec() * (self.k/self.delx**2)
            ugrid1[1:-1] = self._implicit_timestep(ugrid0)
            ugrid0=ugrid1
            self.i+=1
            ugrid_out = np.row_stack((ugrid_out,ugrid0))

        self.ugrid_out = ugrid_out

if __name__ == "__main__":
    p = parabolic1d(3,1,1,100,50)
    p.setup()
    p.solve(50,.5)
    #print(p.ugrid_out.shape)
    #print(len(p.ugrid_out))
    #print(all([all([x1 <= x2 for x1, x2 in zip(tslice,tslice[1:])]) for tslice in p.ugrid_out]))

    for tslice in p.ugrid_out:
        print(tslice)
        #print([x1 <= x2 for x1, x2 in zip(tslice,tslice[1:])])
        print(tslice[-1])
        print(tslice[-2])