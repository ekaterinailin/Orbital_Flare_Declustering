import pytest
import types
from inspect import signature
import numpy as np

from ..spimodel import SPI_Model

def test_init_spimodel():
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    assert len(np.shape(pm.data)) == 1
    assert pm.n_orbits >= 1
    assert pm.eccentricity > 0 and pm.eccentricity < 1
    assert pm.model in ['absolute_distance_influence', 'inverse_distance_influence']
    assert pm.major_axis_a != np.inf
    if pm.major_axis_a is not None:
        assert pm.major_axis_a > 0

def test_negative_likelihood_function():
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    parameters = [1,2]
    output = pm._negative_likelihood_function(parameters) 
    assert output is float
    parameters = [1,np.nan]
    with pytest.raises(ValueError):
        output = pm._negative_likelihood_function(parameters) 

def test_spimodel_estimate_two_parameters():
    pass

def test_intensity_function():
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    model = pm.intensity_function()
    assert type(model) == types.functionType
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), model ='default', n_orbits = 1)
    with pytest.raises(KeyError):
        model = pm.intensity_function()
        
def test_thinning():
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    assert len(pm.hom) + len(pm.inhom) == len(pm.data)
