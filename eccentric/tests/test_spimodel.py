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
    assert isinstance(output, float)
    parameters = [1,np.nan]
    with pytest.raises(ValueError):
        output = pm._negative_likelihood_function(parameters) 

def test_estimate_two_parameters():
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    output = pm.estimate_two_parameters()
    assert len(output) == 2
    assert output[0] > 0 
    assert output[1] >= 0
    
def test_intensity_function():
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    model = pm.intensity_function()
    assert type(model) == types.FunctionType
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), model ='default', n_orbits = 1)
    with pytest.raises(KeyError):
        model = pm.intensity_function()
        
def test_thinning():
    pm = SPI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    pm.thinning()
    assert len(pm.hom) + len(pm.inhom) == len(pm.data)


# Integration Test

import numpy as np

from ..synthetic import SyntheticFlares, HotJupiterHost
from ..spimodel import SPI_Model

import matplotlib.pyplot as plt
    

def test_integration():
    sf = SyntheticFlares(hjhost=HotJupiterHost(period=15, a=1., e=.3, first_periastron_time=7000.,), 
                         #period in days, a in AU, first periastron time must occur after first_observation time...
                         observation_deltat=105, # in days
                         cadence=6, #observations per hour
                         flares_per_day=.1, #in days^-1
                         first_observation_time=6999)# day
    phase = .7
    sf.generate_synthetic_flares(model="Gauss",
                             size=5, # number of SPI flares per periastron passage
                             width=0.02, # in days (standard deviation)
                             phase=phase) #  can be chosen from 0 to 1
    spi = SPI_Model(major_axis_a=sf.hjhost.major_axis_a,
                eccentricity=sf.hjhost.eccentricity,
                data=sf.all_flares.stacked_peak_time,
                n_orbits=sf.observation_deltat / sf.hjhost.period)
    a, b = spi.estimate_two_parameters()
    print(a,b)
    spi.thinning()
    print(len(spi.hom), len(spi.inhom))
    
    
    
    
    
    
    
    