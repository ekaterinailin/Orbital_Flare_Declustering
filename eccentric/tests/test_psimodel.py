import pytest
from inspect import signature
import numpy as np

from ..psimodel import PSI_Model

def test_init_psimodel():
    pm = PSI_Model(major_axis_a = None, eccentricity = 0.5, data = np.linspace(0,1,10), n_orbits = 1)
    assert len(np.shape(pm.data)) == 1
    assert pm.n_orbits >= 1
    assert pm.eccentricity > 0 and pm.eccentricity < 1
    assert pm.model in ['absolute_distance_influence', 'inverse_distance_influence']
    assert pm.major_axis_a != np.inf
    if pm.major_axis_a is not None:
        assert pm.major_axis_a > 0

def test_psimodel_estimate_two_parameters():
    #how do I test that act
    pass

def test_intensity_function():
    pass

def test_thinning():
    pass
