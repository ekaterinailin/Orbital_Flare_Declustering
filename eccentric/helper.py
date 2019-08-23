import numpy as np
import math

def find_nearest(array, value):
    """Find the nearest value to the
    entries in a given array."""
    idx = np.searchsorted(array, value, side="left")
 #   condition = 
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return array[idx-1]
    else:
        return array[idx]