import pytest
import numpy as np

from ..models import *

def test_model_absolute_distance_influence():
    # Use case parameter values
    time, base, peak, eccentricity = [0.5,2,3,0.7]
    output = model_absolute_distance_influence(time, base, peak, eccentricity)
    assert isinstance(output, float)
    assert output > 0
    time, base, peak, eccentricity = [0.5,2,np.inf,0.7]
    with pytest.raises(ValueError):
        output = model_absolute_distance_influence(time, base, peak, eccentricity)
    
    time, base, peak, eccentricity = [0.5,2,3, np.nan]
    with pytest.raises(ValueError):
        output = model_absolute_distance_influence(time, base, peak, eccentricity)
    
    
    
def test_model_inverse_distance_influence():
    # Use case parameter values
    time, base, peak, eccentricity = [0.5,2,3,0.7]
    output = model_inverse_distance_influence(time, base, peak, eccentricity)
    assert isinstance(output, float)
    assert output > 0
    time, base, peak, eccentricity = [0.5,2,np.inf,0.7]
    with pytest.raises(ValueError):
        output = model_inverse_distance_influence(time, base, peak, eccentricity)
    
    time, base, peak, eccentricity = [0.5,2,3, np.nan]
    with pytest.raises(ValueError):
        output = model_inverse_distance_influence(time, base, peak, eccentricity)
    
    
    
def test_model_absolute_distance_influence_with_maj_axis(): 
    # Use case parameter values
    time, base, peak, eccentricity, majors_axis_a = [0.5,2,3,0.7,1.5]
    output = model_absolute_distance_influence_with_maj_axis(time, base, peak, eccentricity, majors_axis_a)
    assert isinstance(output, float)   
    assert output > 0
    time, base, peak, eccentricity, majors_axis_a = [0.5,2,np.inf,0.7,1.5]
    with pytest.raises(ValueError):
        output = model_absolute_distance_influence_with_maj_axis(time, base, peak, eccentricity, majors_axis_a)
    
    time, base, peak, eccentricity, majors_axis_a = [0.5,2,3, np.nan,1.5]
    with pytest.raises(ValueError):
        output = model_absolute_distance_influence_with_maj_axis(time, base, peak, eccentricity, majors_axis_a)
  
    
     
    
def test_model_inverse_distance_influence_with_maj_axis():
    # Use case parameter values
    time, base, peak, eccentricity, majors_axis_a = [0.5,2,3,0.7,1.5]
    output = model_inverse_distance_influence_with_maj_axis(time, base, peak, eccentricity, majors_axis_a)
    assert isinstance(output, float)
    assert output > 0
    time, base, peak, eccentricity, majors_axis_a = [0.5,2,np.inf,0.7,1.5]
    with pytest.raises(ValueError):
        output = model_inverse_distance_influence_with_maj_axis(time, base, peak, eccentricity, majors_axis_a)
   
    time, base, peak, eccentricity, majors_axis_a = [0.5,2,3, np.nan,1.5]
    with pytest.raises(ValueError):
        output = model_inverse_distance_influence_with_maj_axis(time, base, peak, eccentricity, majors_axis_a)
    
    

