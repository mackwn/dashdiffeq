import pytest
import numpy as np
from diffeq.parabolic import parabolic1d

##Initialize
def test_raises_exception_on_non_numeric_arguments():
    inputs = [5,50,400,500,1]
    for i in range(0,len(inputs)):
        test_input = inputs
        test_input[i] = str(test_input[i])
        with pytest.raises(TypeError):
            parabolic1d(test_input[0],test_input[1],test_input[2],test_input[3],test_input[4])

def test_inputs_must_be_positive():
    inputs = [5,50,400,500,1]
    for i in range(0,len(inputs)):
        test_input = inputs
        test_input[i] = -test_input[i]
        with pytest.raises(ValueError):
            parabolic1d(test_input[0],test_input[1],test_input[2],test_input[3],test_input[4])

def test_grid_must_have_two_cells_three_nodes():
    with pytest.raises(ValueError):
        parabolic1d(1,40,400,500,1)

def test_conducitivity_must_be_realistic():
    with pytest.raises(ValueError):
        parabolic1d(15,40,400,500,k=.00001)
    with pytest.raises(ValueError):
        parabolic1d(15,40,400,500,k=10000)

def test_temp_must_be_decreasing():
    with pytest.raises(ValueError):
        parabolic1d(15,40,500,400,1)


##set up grid
def test_xgrid_length_is_n_plus_one(setup_parabolic1d):
    assert len(setup_parabolic1d.xgrid) == setup_parabolic1d.n + 1
def test_delx_is_length_over_n(setup_parabolic1d):
    assert setup_parabolic1d.delx == setup_parabolic1d.xlength/setup_parabolic1d.n
def test_initial_temp_vector_at_x0(setup_parabolic1d):
    assert setup_parabolic1d.ugrid[0] == setup_parabolic1d.uo
def test_initial_temp_vector_is_xto(setup_parabolic1d):
    assert (setup_parabolic1d.ugrid[1:] - setup_parabolic1d.uto).sum() == 0
def test_bc_vector_length(setup_parabolic1d):
    assert len(setup_parabolic1d.bcvec) == setup_parabolic1d.n-1
def test_bc_vector_startend_with_uouf(setup_parabolic1d):
    k = setup_parabolic1d.k
    delx = setup_parabolic1d.delx
    bc =setup_parabolic1d.bcvec*delx**2/k
    assert bc[0] == -setup_parabolic1d.uo
    assert bc[-1] == -setup_parabolic1d.uto

def test_bc_vector_interior_is_zero(setup_parabolic1d):
    assert setup_parabolic1d.bcvec[1:-1].sum() == 0
def test_amat_dimensions(setup_parabolic1d):
    n = setup_parabolic1d.n
    assert setup_parabolic1d.amat.shape == (n-1,n-1)
def test_amat_lower_diagnal(setup_parabolic1d):
    n = setup_parabolic1d.n
    k = setup_parabolic1d.k
    delx = setup_parabolic1d.delx
    assert (np.diagonal(setup_parabolic1d.amat,-1) == (np.zeros(n-2) -1)/delx**2*k).all()
def test_amat_upper_diagnol(setup_parabolic1d):
    n = setup_parabolic1d.n
    k = setup_parabolic1d.k
    delx = setup_parabolic1d.delx
    assert (np.diagonal(setup_parabolic1d.amat,1) == (np.zeros(n-2) -1)/delx**2*k).all()
def test_amat_diagonal(setup_parabolic1d):
    n = setup_parabolic1d.n
    k = setup_parabolic1d.k
    delx = setup_parabolic1d.delx
    assert (np.diagonal(setup_parabolic1d.amat,0) == (np.zeros(n-1) + 2)/delx**2*k).all()

##solve

def test_delt_is_reasonable(setup_parabolic1d):
    with pytest.raises(ValueError):
        setup_parabolic1d.solve(delt=.9,ufper=.5)
    with pytest.raises(ValueError):
        setup_parabolic1d.solve(delt=101,ufper=.5)

def test_ufper_is_reasonable(setup_parabolic1d):
    with pytest.raises(ValueError):
        setup_parabolic1d.solve(delt=1,ufper=.04)
    with pytest.raises(ValueError):
        setup_parabolic1d.solve(delt=1,ufper=.96)

def test_output_has_output_mindim_2():
    p = parabolic1d(3,1,1,10000,999)
    p.setup()
    p.solve(100,.95)
    assert len(p.ugrid_out) > 2
    
def test_output_is_always_monotonic_decreasing(solved_parabolic1d):
    assert all([all([x1 <= x2 for x1, x2 in zip(tslice,tslice[1:])]) for tslice in solved_parabolic1d.ugrid_out]) == True
    
def test_time_boundary_condition_is_met(solved_parabolic1d):
    assert (solved_parabolic1d.ufper >= (solved_parabolic1d.ugrid_out[-1]-solved_parabolic1d.uo)/(solved_parabolic1d.uto - solved_parabolic1d.uo)).all()

@pytest.fixture 
def setup_parabolic1d():
    prb1d = parabolic1d(5,10,250,500,1.5)
    prb1d.setup()
    return prb1d

@pytest.fixture 
def solved_parabolic1d():
    prb1d = parabolic1d(5,10,250,500,4)
    prb1d.setup()
    prb1d.solve(10,.5)
    return prb1d
    