import pytest
import numpy as np
from diffeq.elliptic import elliptic2d

########init

##test inputs are positive
def test_inputs_are_positive():
    pass

def test_dimensions_are_positive_ints_or_floats():
    bad_dims = [[100],'a',-5]
    for bad_dim in bad_dims:
        with pytest.raises(TypeError):
            elliptic2d(bad_dim,10,10,10,[500,500],[500,500],1,.001)
        with pytest.raises(TypeError):
            elliptic2d(10,bad_dim,10,10,[500,500],[500,500],1,.001)
        with pytest.raises(TypeError):
            elliptic2d(10,10,bad_dim,10,[500,500],[500,500],1,.001)
        with pytest.raises(TypeError):
            elliptic2d(10,10,10,bad_dim,[500,500],[500,500],1,.001)
        

def test_grid_at_least_three():
    with pytest.raises(ValueError):
        elliptic2d(10,10,2,10,[500,500],[500,500],1,.001)
    with pytest.raises(ValueError):
        elliptic2d(10,10,10,2,[500,500],[500,500],1,.001)

def test_heat_transfer_is_reasonable():
    with pytest.raises(ValueError):
        elliptic2d(10,10,10,10,[500,500],[500,500],2,.0001)
    with pytest.raises(ValueError):
        elliptic2d(10,10,10,10,[500,500],[500,500],-1,.0001)

def test_conductivity_is_reasonable(): ###this should raise an error!!
    #.00001,.00101
    with pytest.raises(ValueError):
        elliptic2d(10,10,10,10,[500,500],[500,500],1,.000001)
    with pytest.raises(ValueError):
        elliptic2d(10,10,10,10,[500,500],[500,500],1,.01)

##test ranges of inputs
def test_temp_inputs_are_list_of_len_two():
    bad_temp_inputs = [[200],[200,200,200],"aa",3]
    for bad_temp_input in bad_temp_inputs:
        with pytest.raises(TypeError):
            elliptic2d(10,10,10,10,ux=bad_temp_inputs,uy=[500,500],q=1,k=.001)
        with pytest.raises(TypeError):
            elliptic2d(10,10,10,10,ux=[500,500],uy=bad_temp_input,q=1,k=.001)

def test_initial_temps_in_reasonable_ranges():
    #xlength,ylength,ux,uy,q,k,m,n
    extrema = [[50,500],[500,50],[5000,500],[500,5000]]
    for extremum in extrema:
        with pytest.raises(ValueError):
            elliptic2d(10,10,10,10,ux=extremum,uy=[500,500],q=1,k=.001)
        with pytest.raises(ValueError):
            elliptic2d(10,10,10,10,ux=[500,500],uy=extremum,q=1,k=.001)
    
    

#######setup
#test dimiensions of grids
def test_spatial_grid_dimensions_correct(setup_ellip2d):
    # grid should be one greater than the number of input 'cells' - 'm' cells need 'm+1' nodes
    assert setup_ellip2d.xgrid.shape == (setup_ellip2d.m+1,setup_ellip2d.n+1)
    assert setup_ellip2d.ygrid.shape == (setup_ellip2d.m+1,setup_ellip2d.n+1)
    


def test_ugrid_dimensions_correct(setup_ellip2d):
    # grid should be one greater than the number of input 'cells' - 'm' cells need 'm+1' nodes
    assert setup_ellip2d.ugrid.shape == (setup_ellip2d.m+1,setup_ellip2d.n+1)

def test_uovec_dimensions(setup_ellip2d):
    assert setup_ellip2d.uovec.shape == ((setup_ellip2d.m-1)*(setup_ellip2d.n-1),1)


def test_fmat_dimensions_correct(setup_ellip2d):
    assert setup_ellip2d.fvec.shape == ((setup_ellip2d.m-1)*(setup_ellip2d.n-1),1)

def test_amat_dimensions_correct(setup_ellip2d):
    assert setup_ellip2d.amat.shape == ((setup_ellip2d.m-1)*(setup_ellip2d.n-1),(setup_ellip2d.m-1)*(setup_ellip2d.n-1))

def test_amat_diagonals_correct():

    pass

def test_solver(solved_ellip2d):
    assert solved_ellip2d.ugrid.shape == (solved_ellip2d.m+1,solved_ellip2d.n+1)

#test boundary conditions

#test step size

#test a matrix dimensions

#test a matrx diagnols

#test output vector format

#fmap format


######solve
#test ugrid format
@pytest.fixture 
def setup_ellip2d():
    ell2d = elliptic2d(10,10,10,10,[500,500],[500,500],1,.0001)
    ell2d.setup()
    return ell2d

@pytest.fixture 
def solved_ellip2d():
    ell2d = elliptic2d(10,10,10,10,[500,500],[500,500],1,.0001)
    ell2d.setup()
    ell2d.solve()
    return ell2d