#!/usr/bin/python

import numpy

def flatten(composite_array):
    return map(lambda x:x[0], composite_array)

def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    n=len(ages)
    residual_errors = (predictions - net_worths)
    data = zip(flatten(ages), flatten(net_worths), flatten(residual_errors))
    dtype=[('age', 'int'),('net_worth', 'float'),('error', 'float')]
    struc_data = numpy.sort(numpy.array(data, dtype=dtype), order='error')
    return struc_data[:(n*.9)]

    #failed to use common sort here... an error about getting np.boolean while expecting int, could not be explained
    #except as a quirk of using np data types, which I can not avoid situation
    #it would cost more to convert then to regular data types and sort. it is easier to sort numpy style



