#!/usr/bin/env python

import numpy as np

class Transformer:
    """
    holds a reference to a line, and can perform arbitrary transformations on the original underlying data.
    Original underlying data is always stored, so e.g. you don't perform translation on top of translation.
    """
    def __init__(self, line):
        self.line = line
        self.originalY = line.get_ydata()

    def transformY(self, function):
        self.line.set_ydata(function(self.originalY))

def translate(data, distance):
    """
    "Shifts" a numpy ndarray a distance by inserting NaNs
    at either the beginning or end, and truncating the other side.

    Parameters:
    data (ndarray): the data to translate
    distance (int): the distance to shift. Can be negative for a left shift.
    """
    # TODO: if distance is not an integer, return data as is
    # TODO: check that data is really an ndarray
    distance = int(distance)
    toReturn = np.empty_like(data)
    if distance > 0:
        # shift to the right
        toReturn[:distance] = np.nan
        toReturn[distance:] = data[:-distance]
    elif distance < 0:
        toReturn[distance:] = np.nan
        toReturn[:distance] = data[-distance:]
    else:
        toReturn = data
    return toReturn

def translateLambdaGenerator(distance):
    """generate a function to pass to Transformer.transformY from only a distance"""
    return lambda data: translate(data, distance)
