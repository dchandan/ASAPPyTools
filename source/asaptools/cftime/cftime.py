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
# alias_to_unit - Helper function to map unit aliases to standard unit names
#==============================================================================
def alias_to_unit(ualias):
    """
    Map a unit alias to a standard unit string

    Standard unit strings are mapped to themselves.

    Parameters:
        ualias (str): The string alias for a given time unit

    Returns:
        str: The standard unit name of the alias
    """

    # Check Type
    if not isinstance(ualias, str):
        err_msg = "Alias must be given as a string"
        raise TypeError(err_msg)

    # Map unit string to index
    if ualias in __INDICES__:
        return ualias
    elif ualias in __ALIASES__:
        return __ALIASES__[ualias]
    else:
        err_msg = "Unrecognized unit name \"" + ualias + "\""
        raise ValueError(err_msg)


#==============================================================================
# __unit_to_index__ - Helper function to map unit names to tuple indices
#==============================================================================
def __unit_to_index__(ualias):
    """
    Map a unit string to a date-time tuple index

    Parameters:
        ualias (str): The string name for a given time unit

    Returns:
        int: The integer index in a date-time tuple corresponding to that unit
    """

    # Check Type
    if not isinstance(ualias, str):
        err_msg = "Unit name must be given as a string"
        raise TypeError(err_msg)

    # Map unit string to index
    return __INDICES__.index(alias_to_unit(ualias))


#==============================================================================
# __index_to_unit__ - Helper function to map date-time tuple index to unit name
#==============================================================================
def __index_to_unit__(index):
    """
    Map an integer date-time tuple index to a standard unit name

    Parameters:
        index (int): The integer date-time tuple index

    Returns:
        str: The standard unit name corresponding to the date-time tuple index
    """

    # Check Type
    if not isinstance(index, (int, long)):
        err_msg = "Index must be an integer type"
        raise TypeError(err_msg)

    # Check Bounds
    if index < 0 or index >= len(__INDICES__):
        err_msg = "Index (" + str(index) + ") out of bounds"
        raise IndexError(err_msg)

    # Return unit name
    return __INDICES__[index]


#==============================================================================
# __is_dttuple__ -- Check if an argument is a proper date-time tuple
#==============================================================================
def __is_dttuple__(arg):
    """
    Check if a given argument is a properly-formed date-time tuple

    A properly-formed date-time tuple is a Python tuple containing
    5 integers and 1 (final) integer or float.  (Internally, the last
    item in the tuple is stored as a float, but it can be given as
    an int and converted.)

    Parameters:
        arg: Any object

    Returns:
        bool: True, if *arg* is a properly-formed date-time tuple.
            False, otherwise.
    """
    if not hasattr(arg, '__len__'):
        return False
    if len(arg) != len(__INDICES__):
        return False
    if not all([isinstance(a, (int, long)) for a in arg[:-1]]):
        return False
    if not isinstance(arg[-1], (int, long, float)):
        return False
    return True


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

    NOTE: Comparison operators cannot be implemented for this class because
    the number of days in a month, and the number of months in a day, etc.
    can vary depending on the calendar.
    """

    def __init__(self, *params, **kwargs):
        """
        Constructor

        Can be constructed from either a date-time tuple/list or a dict of
        unit-named values (e.g., {'years': 5, 'hours': -2}).  Keyword arguments
        overwrite parameters.  If nothing is supplied, then the default
        date-time tuple is equivalent to 0. Unrecognized keyword arguments
        will result in an error.

        Parameters:
            params: A date-time tuple

        Keyword Arguments:
            kwargs: Can be any dictionary of unit-named values
        """

        dtlist = [0 for _ in __INDICES__]

        # Check input parameters/arguments
        if __is_dttuple__(params):
            dtlist = params
        elif len(params) == 1 and __is_dttuple__(params[0]):
            dtlist = params[0]

        # Loop through keyword arguments and change values
        for ualias, uvalue in kwargs.items():
            uindex = __unit_to_index__(ualias)
            dtlist[uindex] = uvalue

        # Check final values
        if not __is_dttuple__(dtlist):
            err_msg = "Failed to construct date-time tuple " + str(dtlist)
            raise ValueError(err_msg)

        # Store the date-time tuple
        self._dttuple = tuple(dtlist)

    def __str__(self):
        output = []
        for value, unit in zip(self._dttuple, __INDICES__):
            if value != 0:
                output.append(str(value) + " " + unit)
        return ', '.join(output)

    def __repr__(self):
        return repr(self._dttuple)

    def __pos__(self):
        return CFDateTimeDelta(self._dttuple)

    def __neg__(self):
        neg_dttuple = [-x for x in self._dttuple]
        return CFDateTimeDelta(neg_dttuple)

    def __add__(self, other):
        """
        Addition operator

        Parameters:
            other (CFDateTimeDelta): An instance of a CFDateTimeDelta

        Returns:
            A CFDateTimeDelta instance with its date-time tuple equal to the 
            item-by-item sum of the individual date-time tuples
        """
        if isinstance(other, CFDateTimeDelta):
            add_dttuple = [x + y for x, y in
                           zip(self._dttuple, other._dttuple)]
            return CFDateTimeDelta(add_dttuple)
        else:
            return NotImplemented

    def __radd__(self, other):
        """
        Reflected addition operator

        Parameters:
            other (CFDateTimeDelta): An instance of a CFDateTimeDelta

        Returns:
            A CFDateTimeDelta instance with its date-time tuple equal to the 
            item-by-item sum of the individual date-time tuples
        """
        if other == 0:
            new_dttuple = self._dttuple
            return CFDateTimeDelta(new_dttuple)
        else:
            return self.__add__(other)

    def __iadd__(self, other):
        """
        Addition-assignment operator

        Parameters:
            other (CFDateTimeDelta): An instance of a CFDateTimeDelta

        Returns:
            A CFDateTimeDelta instance with its date-time tuple equal to the 
            item-by-item sum of the individual date-time tuples
        """
        if isinstance(other, CFDateTimeDelta):
            self._dttuple = tuple([x + y for x, y in
                                   zip(self._dttuple, other._dttuple)])
            return self
        else:
            return NotImplemented

    def __sub__(self, other):
        """
        Subtraction operator

        Parameters:
            other (CFDateTimeDelta): An instance of a CFDateTimeDelta

        Returns:
            A CFDateTimeDelta instance with its date-time tuple equal to the 
            item-by-item subtraction of the individual date-time tuples
        """
        if isinstance(other, CFDateTimeDelta):
            sub_dttuple = [x - y for x, y in
                           zip(self._dttuple, other._dttuple)]
            return CFDateTimeDelta(sub_dttuple)
        else:
            return NotImplemented

    def __isub__(self, other):
        """
        Subtraction-assignment operator

        Parameters:
            other (CFDateTimeDelta): An instance of a CFDateTimeDelta

        Returns:
            A CFDateTimeDelta instance with its date-time tuple equal to the 
            item-by-item subtraction of the individual date-time tuples
        """
        if isinstance(other, CFDateTimeDelta):
            self._dttuple = tuple([x - y for x, y in
                                   zip(self._dttuple, other._dttuple)])
            return self
        else:
            return NotImplemented


#==============================================================================
# CFDateTime - A
#==============================================================================
class CFDateTime(CFDateTimeDelta):

    """
    CFDateTime -- A specified date and time on a given calendar
    """
