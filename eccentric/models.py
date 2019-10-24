import numpy as np

def model_absolute_distance_influence(time, base, peak, eccentricity, major_axis_a =None):
    return base + peak*(eccentricity + 1 - np.sqrt((eccentricity - np.cos(2*np.pi*(time-1/2)))**2 + (1-eccentricity**2)*(np.sin(2*np.pi*(time-1/2))**2)))
    
def model_inverse_distance_influence(time, base, peak, eccentricity, major_axis_a = None):
    return base + peak/(np.sqrt((eccentricity - np.cos(2*np.pi*(time-1/2)))**2 + (1-eccentricity**2)*(np.sin(2*np.pi*(time-1/2))**2)))

def model_absolute_distance_influence_with_maj_axis(time, base, peak, eccentricity, major_axis_a):
    b = np.sqrt(major_axis_a**2/(1-eccentricity**2))
    return base + peak*(np.sqrt(major_axis_a**2-b**2) + major_axis_a - np.sqrt((np.sqrt(major_axis_a**2-b**2) 
                                                                               - major_axis_a*np.cos(2*np.pi*(time-1/2)))**2 + b**2*(np.sin(2*np.pi*(time-1/2))**2)))

def model_inverse_distance_influence_with_maj_axis(time, base, peak, eccentricity, major_axis_a):
    b = np.sqrt(major_axis_a**2/(1-eccentricity**2))
    return base + peak/(np.sqrt((np.sqrt(major_axis_a**2-b**2) - major_axis_a*np.cos(2*np.pi*(time-1/2)))**2 + b**2*(np.sin(2*np.pi*(time-1/2))**2)))
        