"""
A module containing CF-Convention time units and unit names 

Copyright 2015, University Corporation for Atmospheric Research
See the LICENSE.txt file for details
"""

# List the standard unit names in order of largest to smallest
__STANDARDS__ = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']

# List of aliases for each base name and to what it maps
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
# find_unit - Map unit aliases to standard unit names
#==============================================================================
def find_unit(ualias):
    """
    Map a unit alias to a standard unit string

    Standard unit names are mapped to themselves.

    Parameters:
        ualias (str): The string alias for a given time unit

    Returns:
        str: The standard unit name of the alias
    """

    # Check Type
    if not isinstance(ualias, str):
        err_msg = "Alias must be given as a string"
        raise TypeError(err_msg)

    # Lower case only
    lualias = ualias.lower()

    # Map unit string to index
    if lualias in __STANDARDS__:
        return lualias
    elif lualias in __ALIASES__:
        return __ALIASES__[lualias]
    else:
        err_msg = "Unrecognized unit name \"" + ualias + "\""
        raise ValueError(err_msg)
