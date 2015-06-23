"""
A module containing the CFDateTime classes.

This module contains the CFDateTime, the CFDateTimeDelta, and the
CFCalendar classes.  These classes provide functionality for reading,
comparing, and measuring the differences between two date-time objects
defined with different calendaring specifications.

Copyright 2015, University Corporation for Atmospheric Research
See the LICENSE.txt file for details
"""


__INDICES__ = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

__ALIASES__ = {'year': 'years',
               'yrs': 'years',
               'yr': 'years',
               'month': 'months',
               'mons': 'months',
               'mon': 'months',
               'mos': 'months',
               'mo': 'months',
               'day': 'days',
               'd': 'days',
               'hour': 'hours',
               'hrs': 'hours',
               'hr': 'hours',
               'h': 'hours',
               'minute': 'minutes',
               'mins': 'minutes',
               'min': 'minutes',
               'second': 'seconds',
               'secs': 'seconds',
               'sec': 'seconds',
               's': 'seconds'}


#==============================================================================
# __alias_to_unit - Helper function to map unit aliases to standard unit names
#==============================================================================
def __alias_to_unit(alias):
    """
    Map a unit alias to a standard unit string

    Standard unit strings are mapped to themselves.

    Parameters:
        alias (str): The string alias for a given time unit

    Returns:
        str: The standard unit name of the alias
    """

    # Check Type
    if type(alias) is not str:
        err_msg = "Alias must be given as a string"
        raise TypeError(err_msg)

    # Map unit string to index
    if alias in __INDICES__:
        return alias
    elif alias in __ALIASES__:
        return __ALIASES__[alias]
    else:
        err_msg = "Unrecognized unit name \"" + unit + "\""


#==============================================================================
# __unit_to_index - Helper function to map unit names to tuple indices
#==============================================================================
def __unit_to_index(alias):
    """
    Map a unit string to a date-time tuple index

    Parameters:
        alias (str): The string name for a given time unit

    Returns:
        int: The integer index in a date-time tuple corresponding to that unit
    """

    # Check Type
    if type(alias) is not str:
        err_msg = "Unit name must be given as a string"
        raise TypeError(err_msg)

    # Map unit string to index
    return __INDICES__.index(__alias_to_unit(alias))


#==============================================================================
# __index_to_unit - Helper function to map date-time tuple index to unit name
#==============================================================================
def __index_to_unit(index):
    """
    Map an integer date-time tuple index to a standard unit name

    Parameters:
        index (int): The integer date-time tuple index

    Returns:
        str: The standard unit name corresponding to the date-time tuple index
    """

    # Check Type
    if type(index) is not int:
        err_msg = "Index must be an integer"
        raise TypeError(err_msg)

    # Check Bounds
    if index < 0 or index >= len(__INDICES__):
        err_msg = "Index (" + str(index) + ") out of bounds"
        raise ValueError(err_msg)

    # Return unit name
    return __INDICES__[index]


#==============================================================================
# CFDateTimeDelta - Object for Measuring Date-Time Durations
#==============================================================================
class CFDateTimeDelta(object):

    """
    CFDateTimeDelta -- Measures the difference between two CFDateTime objects

    The CFDateTimeDelta object acts as a measure of duration from an unknown
    (or unspecified) starting or reference point.  It can represent any amount
    of years, months, days, hours, minutes, or seconds, or any combination of
    these.  It can be both positive or negative components.
    """

    def __init__(self, **kwargs):
        """
        Constructor

        Keyword Arguments:
            kwargs: Can be 
        """
