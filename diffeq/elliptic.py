import numpy as np


class elliptic2d():
    def __init__(self,xlength,ylength,m,n,ux,uy,q,k):

        def dim_val(var):
            if (type(var) in (float,int)) and (var>0): return var
            else: raise(TypeError('Dimensions must be positive numbers'))
        def min_grid(var):
            if var >= 3: return var
            else: raise(ValueError('grid must have at least 3 points'))
        
        self.xlength = dim_val(xlength)
        self.ylength = dim_val(ylength)


        self.m = min_grid(dim_val(m))
        self.n = min_grid(dim_val(n))
     
        if type(ux) != list or len(ux) != 2: raise(TypeError('Ux must be a list of length 2'))
        if not all([100 <= u <= 1000 for u in ux]): raise(ValueError('Temp must be between 100 K and 1000 K'))
        self.ux = ux
        if type(uy) != list or len(uy) != 2: raise(TypeError('Uy must be a list of length 2'))
        if not all([100 <= u <= 1000 for u in uy]): raise(ValueError('Temp must be between 100 K and 1000 K'))
        self.uy = uy

 
        if not .00001 <= k <= .00101: raise(ValueError('Conductivity must be between .00001 and .00101'))
        self.q = q
        if not 0 <= q <= 1: raise(ValueError('Conductivity must be between 0 and 1'))
        self.k = k

    def _create_amat(self):
        def centdiffd2mat2d(m,n,delx,dely):
        #mat = np.zeros((n-1,n-1))
            cols = n*m

            diag = (np.zeros(cols) + 2)*(1/delx**2+1/dely**2)

            xdiag = (np.zeros(cols-n)-1)*(1/delx**2)

            ydiag = (np.array(([-1]*(n-1)+[0])*(m-1)+[-1]*(n-1)))*(1/dely**2)

            mat = np.diagflat(diag) + np.diagflat(xdiag,k=n) + np.diagflat(xdiag,k=-n) + np.diagflat(ydiag,k=1) + np.diagflat(ydiag,k=-1)
            
            
            return mat
        
        self.amat = centdiffd2mat2d(self.m-1,self.n-1,self.delx,self.dely)



    def _create_uovec(self):
        ugrid = self.ugrid
        ugrid[1,1:-1] -= ugrid[0,1:-1]/self.dely**2
        ugrid[-2,1:-1] -= ugrid[-1,1:-1]/self.dely**2
        ugrid[1:-1,1] -= ugrid[1:-1,0]/self.delx**2
        ugrid[1:-1,-2] -= ugrid[1:-1,-1]/self.delx**2
        self.uovec = np.reshape(ugrid[1:-1,1:-1],(ugrid[1:-1,1:-1].size,1))

    def _create_ugrid(self):
        ugrid = np.zeros((self.m+1,self.n+1))
        ugrid[:,0] = self.ux[0]
        ugrid[:,-1] = self.ux[1]
        ugrid[0,:] = self.uy[0]
        ugrid[-1,:] = self.uy[1]
        self.ugrid = ugrid

    def _create_spatial_grid(self):
        #this should maybe be x = f(n), y = f(m), X,Y = mesh(x,y)
        x = np.linspace(0,self.xlength,self.m+1)
        y = np.linspace(0,self.ylength,self.n+1)
        self.delx = abs(x[0]-x[1])
        self.dely = abs(y[0]-y[1])
        self.ygrid, self.xgrid = np.meshgrid(y,x)

    def _create_fmat(self):
        def dx2elliptic2d(X,Y,q):
            return X*0+q#X+Y
        fmat = dx2elliptic2d(self.xgrid[1:-1,1:-1],self.ygrid[1:-1,1:-1],self.q)
        self.fvec = np.resize(fmat, (fmat.size,1))


    
    def setup(self):
        self._create_spatial_grid()
        self._create_ugrid()
        self._create_uovec()
        self._create_amat()
        self._create_fmat()

    def solve(self):
        amatinv = np.linalg.inv(self.amat)
        uout = np.dot(amatinv,self.fvec*(1/self.k)-self.uovec)
        self.ugrid[1:-1,1:-1] = uout.reshape((self.m-1,self.n-1))