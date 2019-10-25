import numpy as np

def ContainsNaN(func):
    def wrapper(*args, **kawrgs):
        if np.isnan(np.array(func(*args, **kawrgs))).any():
            raise ValueError('NaN-value detected. Check your input parameters.')
        elif np.isinf(np.array(func(*args,**kawrgs))).any():
            raise ValueError('Intensity is infinite. Check your input parameters.')
        return func(*args, **kawrgs)
    return wrapper

@ContainsNaN
def model_absolute_distance_influence(time, base, peak, eccentricity, major_axis_a =None):
    if eccentricity > 1 or eccentricity < 0:
        raise KeyError('The eccentricity has to be between 0 and 1.')
    elif base <= 0: 
        raise KeyError('The base rate has to be positive')
    elif peak < 0: 
        raise KeyError('The peak has to have non-negative height.')
    return base + peak*(eccentricity + 1 - np.sqrt((eccentricity - np.cos(2*np.pi*(time-1/2)))**2 + (1-eccentricity**2)*(np.sin(2*np.pi*(time-1/2))**2)))

@ContainsNaN   
def model_inverse_distance_influence(time, base, peak, eccentricity, major_axis_a = None):
    if eccentricity > 1 or eccentricity < 0:
        raise KeyError('The eccentricity has to be between 0 and 1.')
    return base + peak/(np.sqrt((eccentricity - np.cos(2*np.pi*(time-1/2)))**2 + (1-eccentricity**2)*(np.sin(2*np.pi*(time-1/2))**2)))

@ContainsNaN
def model_absolute_distance_influence_with_maj_axis(time, base, peak, eccentricity, major_axis_a):
    if eccentricity > 1 or eccentricity < 0:
        raise KeyError('The eccentricity has to be between 0 and 1.')
    elif base <= 0: 
        raise KeyError('The base rate has to be positive')
    elif peak < 0: 
        raise KeyError('The peak has to have non-negative height.')
    b = np.sqrt(major_axis_a**2*(1-eccentricity**2))
    return base + peak*(np.sqrt(major_axis_a**2-b**2) + major_axis_a - np.sqrt((np.sqrt(major_axis_a**2-b**2) 
                                                                               - major_axis_a*np.cos(2*np.pi*(time-1/2)))**2 + b**2*(np.sin(2*np.pi*(time-1/2))**2)))
    
@ContainsNaN
def model_inverse_distance_influence_with_maj_axis(time, base, peak, eccentricity, major_axis_a):
    if eccentricity > 1 or eccentricity < 0:
        raise KeyError('The eccentricity has to be between 0 and 1.')
    elif base <= 0: 
        raise KeyError('The base rate has to be positive')
    elif peak < 0: 
        raise KeyError('The peak has to have non-negative height.')
    b = np.sqrt(major_axis_a**2*(1-eccentricity**2))
    return base + peak/(np.sqrt((np.sqrt(major_axis_a**2-b**2) - major_axis_a*np.cos(2*np.pi*(time-1/2)))**2 + b**2*(np.sin(2*np.pi*(time-1/2))**2)))
        
