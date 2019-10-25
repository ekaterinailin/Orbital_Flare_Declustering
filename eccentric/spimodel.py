#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 10:57:38 2019

@author: jens
"""

import warnings
import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize 
from .models import *

class SPI_Model():
    '''
    
    '''
    
    def __init__(self, major_axis_a = None, eccentricity = 0.5, data = None, model = 'absolute_distance_influence', n_orbits = None):
        '''
        
        '''
        self.major_axis_a = major_axis_a
        self.eccentricity = eccentricity
        self.n_orbits = n_orbits
        self.model = model
        self.data = data
        self.hom = []
        self.inhom = []
        self.MLE_params = None
        
    def intensity_function(self):
        '''
        
        '''
        model_dictionary = {'model_absolute_distance_influence' : model_absolute_distance_influence,
         'model_inverse_distance_influence' : model_inverse_distance_influence,
         'model_absolute_distance_influence_with_maj_axis' : model_absolute_distance_influence_with_maj_axis,
         'model_inverse_distance_influence_with_maj_axis' : model_inverse_distance_influence_with_maj_axis}
        
        if self.model not in ['absolute_distance_influence', 'inverse_distance_influence']:
            raise KeyError('Name not available among models. Use "absolute_distance_influence" or "inverse_distance_influence" instead.')
        else:    
            if self.major_axis_a is None and self.eccentricity is not None:
                warnings.warn('Length of major axis not set. Using eccentricity only.')
                if self.model == 'absolute_distance_influence': # goal in the end to estimate "base" and "peak". a and b are hyperparameters
                    return model_dictionary['model_absolute_distance_influence']
                elif self.model == 'inverse_distance_influence':
                    return model_dictionary['model_inverse_distance_influence']
            elif self.major_axis_a is not None and self.eccentricity is not None:
                if self.model == 'absolute_distance_influence':
                    return model_dictionary['model_absolute_distance_influence_with_maj_axis']
                elif self.model == 'inverse_distance_influence':
                    return model_dictionary['model_inverse_distance_influence_with_maj_axis']
            else:
                raise ValueError('At least eccentricity has to be passed to SPI_Model.')
                
    def _negative_likelihood_function(self, parameters):
        '''
        
        '''
        if np.nan in parameters:
            raise ValueError('Negative likelihood function received at least one nan-value but needs two floats.')
        # use equation sum lambda(x_i) - int lambda(x) dx
        # negative log likelihood to estimate parameters for a model depending on exactly two parameters
        parameter_a, parameter_b = parameters
        model = self.intensity_function()
        data_depending_term = -np.log(model(self.data, parameter_a, parameter_b, self.eccentricity, self.major_axis_a)).sum()
        compensator = self.n_orbits*quad(lambda x: model(x, parameter_a, parameter_b, self.eccentricity, self.major_axis_a),0,1)[0]
        return data_depending_term + compensator
        
    def estimate_two_parameters(self):
        '''
        
        '''
        if self.data is None or len(self.data) == 0:
            raise ValueError('No input data given.')
        # data as 1:n array
        # function depends on time, a, and b, represents intensity
        # data: event times
        max_likelihood_a, max_likelihood_b = minimize(self._negative_likelihood_function, [1,1], bounds = ((0, None), (0, None)))['x']
        return max_likelihood_a, max_likelihood_b

    def thinning(self):
        '''
        
        '''
        model = self.intensity_function()
        if self.MLE_params == None:
            self.MLE_params  = self.estimate_two_parameters()
        for event in self.data:
            u = np.random.rand()
            if u < (model(event, self.MLE_params[0], self.MLE_params[1],self.eccentricity, self.major_axis_a) - 
                    self.MLE_params[0]) / model(event, self.MLE_params[0], self.MLE_params[1], self.eccentricity, self.major_axis_a):
                self.inhom.append(event)
            else:
                self.hom.append(event)
