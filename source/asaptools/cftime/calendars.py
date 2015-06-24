"""
A module containing CF-Convention calendars

Copyright 2015, University Corporation for Atmospheric Research
See the LICENSE.txt file for details
"""
from __builtin__ import int

# Names of all defined calendars
__CALENDARS__ = ['gregorian', 'standard',
                 'proleptic_gregorian',
                 'noleap', '365_day',
                 'all_leap', '366_day',
                 '360_day',
                 'julian',
                 'none']


#==============================================================================
# create_calendar - Factory function for creating CFCalendar instances
#==============================================================================
def create_calendar(name="standard", **kwargs):
    """
    Factory function to create CFCalendar objects by name

    Parameters:
        name (str): The CF-Convension name for a given calendar

    Keyword Arguments:
        kwargs (dict): Optional arguments to be passed to the CFCalendar
            constructor

    Returns:
        CFCalendar: A CFCalendar instance corresponding to the given name
    """

    # Check type
    if not isinstance(name, str):
        err_msg = "Name must be given as a string"
        raise TypeError(err_msg)

    return CFCalendar(name=name, **kwargs)
    #     err_msg = "Unrecognized calendar name " + name
    #     raise ValueError(err_msg)


#==============================================================================
# CFCalendar - CFCalendar Base Class
#==============================================================================
class CFCalendar(object):

    """
    Basic calendar class

    The base class of the CFCalendar hierarchy represents the most generic
    kind of calendar in the CF Conventions: the user-defined calendar.
    """

    def __init__(self, name, month_lengths, leap_year=None, leap_month=None):
        """
        Constructor

        Parameters:
            name (str): The string name to assign to the calendar type
            month_lengths (tuple): A list or tuple of length 12 with the
                integer number of days in each month (in a non-leap year)

        Keyword Arguments:
            leap_year (int): An example year to be considered a leap year.  
                All years that differ from this year by a multiple of 4 will
                be considered leap years.  If None, then no leap years are
                assumed.
            leap_month (int): An int from 1 to 12 that specifies the month
                to which 1 day will be added in leap years
        """

        # Check types
        if not isinstance(name, str):
            err_msg = "Calendar name must be given as a string or None"
            raise TypeError(err_msg)
        if not isinstance(month_lengths, (tuple, list)):
            err_msg = "Month lengths must be given as a tuple or list"
            raise TypeError(err_msg)
        if not isinstance(leap_year, (int, type(None))):
            err_msg = "Leap year must be given as an int or None"
            raise TypeError(err_msg)
        if not isinstance(leap_month, (int, type(None))):
            err_msg = "Leap month must be given as an int or None"
            raise TypeError(err_msg)

        # Check ranges
        if len(month_lengths) != 12:
            err_msg = "Month lengths must be a tuple or list of length 12"
            raise ValueError(err_msg)
        if leap_year:
            if leap_month is None:
                err_msg = "When leap_year is defined, leap_month must " + \
                    "also be defined"
            elif leap_month < 1 or leap_month > 12:
                err_msg = "Leap month must be an int in the range 1 to 12"
                raise ValueError(err_msg)

        # Store values
        self._name = name
        self._month_lengths = tuple(month_lengths)
        self._leap_year = leap_year
        self._leap_month = leap_month

    def name(self):
        """
        Return the name of the calendar
        """
        return self._name

    def is_leap_year(self, year):
        """
        Check if a given year is a leap year

        Parameters:
            year (int): The year to check if it is a leap year

        Returns:
            bool: True, if 'year' is a leap year.  False, otherwise.
        """

        # Check type
        if not isinstance(year, int):
            err_msg = "Year must be supplied as an int"
            raise TypeError(err_msg)

        # Check if there are leap years and if year is a leap year
        if self._leap_year and (year - self._leap_year) % 4 == 0:
            return True
        else:
            return False

    def days_in_month(self, month, year=None):
        """
        Return the number of days in the given month and year

        Parameters:
            month (int): The integer month in question (1 to 12)

        Keyword Arguments:
            year (int): The year in which the month in question occurs.
                If 'None', then ignore the effect of leap years.

        Returns:
            int: The number of days in the given month/year combination
        """

        # Check types
        if not isinstance(month, int):
            err_msg = "Month must be given as an int"
            raise TypeError(err_msg)
        if year and not isinstance(year, int):
            err_msg = "Year must be given as an int or None"
            raise TypeError(err_msg)

        # Check values
        if month < 1 or month > 12:
            err_msg = "Month must be given as an int from 1 to 12"
            raise ValueError(err_msg)

        # Return number of days in month
        if year and self.is_leap_year(year) and month == self._leap_month:
            return self._month_lengths[month - 1] + 1
        else:
            return self._month_lengths[month - 1]
