import pytest
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


##solve

@pytest.fixture 
def setup_parabolic1d():
    prblc1d = parabolic1d(5,10,250,500,1.5)
    prblc1d.setup()
    return prblc1d

@pytest.fixture 
def solved_parabolic1d():
    prblc1d = parabolic1d(5,10,250,500,1.5)
    prblc1d.setup()
    prblc1d.solve()
    return prblc1d
    