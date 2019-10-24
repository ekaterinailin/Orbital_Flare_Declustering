import pytest
import numpy as np

from ..models import model_absolute_distance_influence

def test_model_absolute_distance_influence():
    time, base, peak, eccentricity = [0.5,2,3,4]
    output = model_absolute_distance_influence(time, base, peak, eccentricity)
    assert isinstance(output, float)
    
def test_model_inverse_distance_influence():
    pass
 
def test_model_absolute_distance_influence_with_maj_axis():    
    pass
    
def test_model_inverse_distance_influence_with_maj_axis():
    pass


