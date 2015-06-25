"""
A module containing CF-Convention calendars

Copyright 2015, University Corporation for Atmospheric Research
See the LICENSE.txt file for details
"""

import abc
from asaptools.cftime import datetime as cfdatetime


#==============================================================================
# create_calendar - Factory function for creating Calendar instances
#==============================================================================
def create_calendar(name="standard", **kwargs):
    """
    Factory function to create Calendar objects by name

    Parameters:
        name (str): The CF-Convension name for a given calendar

    Keyword Arguments:
        kwargs (dict): Optional arguments to be passed to the Calendar
            constructor

    Returns:
        Calendar: A Calendar instance corresponding to the given name
    """

    # Check type
    if not isinstance(name, str):
        err_msg = "Name must be given as a string"
        raise TypeError(err_msg)

    # Return the right kind of Calendar
    if name in ['gregorian', 'standard']:
        return CalendarStandard()
    elif name == 'proleptic_gregorian':
        return CalendarProlepticGregorian()
    elif name in ['noleap', '365_day']:
        return Calendar365Day()
    elif name in ['all_leap', '366_day']:
        return Calendar366Day()
    elif name == '360_day':
        return Calendar360Day()
    elif name == 'julian':
        return CalendarJulian()
    elif name == 'none':
        return CalendarNone()
    else:
        return CalendarGeneric(name=name, **kwargs)


#==============================================================================
# Calendar - Abstract Base Class for all Calendars
#==============================================================================
class Calendar(object):

    """
    An abstract base class for all Calendars
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
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

    @abc.abstractmethod
    def days_in_month(self, month, year=None):
        """
        Return the number of days in the given month (and year, if given)

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

    @abc.abstractmethod
    def days_in_year(self, year=None):
        """
        Returns the number of days in a year

        Keyword Arguments:
            year (int): The specific year in question.  If unspecified, then
                this method returns the nominal number of days in a non-leap
                year.

        Returns:
            int: The number of days in a nominal non-leap year, or the number
                of days in the specified year.
        """

        # Check input type
        if not isinstance(year, (int, type(None))):
            err_msg = "Year must be given as an int or None"
            raise TypeError(err_msg)

    @abc.abstractmethod
    def normalize_datetime(self, datetime):
        """
        Takes a DateTime object and normalizes its values

        NOTE: This can change the DateTime object's data

        Parameters:
            datetime (DateTime): A datetime object
        """

        # Check Type
        if not isinstance(datetime, cfdatetime.DateTime):
            err_msg = "Must supply a DateTime object as input"
            raise TypeError(err_msg)


#==============================================================================
# CalendarGeneric - CalendarGeneric Base Class
#==============================================================================
class CalendarGeneric(Calendar):

    """
    User-Defined calendar class

    The base class of the Calendar hierarchy represents the most generic
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
        self._year_length = sum(month_lengths)

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

        # Call abstract base class for type and value checking
        Calendar.is_leap_year(self, year)

        # Check if there are leap years and if year is a leap year
        if self._leap_year and (year - self._leap_year) % 4 == 0:
            return True
        else:
            return False

    def days_in_month(self, month, year=None):
        """
        Return the number of days in the given month (and year, if given)

        Parameters:
            month (int): The integer month in question (1 to 12)

        Keyword Arguments:
            year (int): The year in which the month in question occurs.
                If 'None', then ignore the effect of leap years.

        Returns:
            int: The number of days in the given month/year combination
        """

        # Call abstract base class for type and value checking
        Calendar.days_in_month(self, month, year)

        # Return number of days in month
        if year and self.is_leap_year(year) and month == self._leap_month:
            return self._month_lengths[month - 1] + 1
        else:
            return self._month_lengths[month - 1]

    def days_in_year(self, year=None):
        """
        Returns the number of days in a year

        Keyword Arguments:
            year (int): The specific year in question.  If unspecified, then
                this method returns the nominal number of days in a non-leap
                year.

        Returns:
            int: The number of days in a nominal non-leap year, or the number
                of days in the specified year.
        """

        # Call base class
        Calendar.days_in_year(self, year)

        # If year specified and it is a leap year, return year length + 1
        if year and self.is_leap_year(year):
            return self._year_length + 1
        else:
            return self._year_length

    def normalize_datetime(self, datetime):
        """
        Takes a DateTime object and normalizes its values

        NOTE: This can change the DateTime object's data

        Parameters:
            datetime (DateTime): A datetime object
        """

        # Call base class
        Calendar.normalize_datetime(self, datetime)

        # Check the DateTime tuple values
        (year, month, day, hour, minute, second, zone) = datetime._dttuple

        # Assume zone is valid

        # Check second
        while second >= 60.0:
            second -= 60.0
            minute += 1
        while second < 0.0:
            second += 60.0
            minute -= 1

        # Check minute
        while minute >= 60:
            minute -= 60
            hour += 1
        while minute < 0:
            minute += 60
            hour -= 1

        # Check hour
        while hour >= 24:
            hour -= 24
            day += 1
        while hour < 0:
            hour += 60
            day -= 1

        # Check day/month/year
        while day > self.days_in_month(month, year):
            day -= self.days_in_month(month, year)
            month += 1
            while month > 12:
                month -= 12
                year += 1
        while day < 1:
            month -= 1
            day += self.days_in_month(month, year)
            while month < 1:
                month += 12
                year -= 1

        # Overwrite the DateTime tuple
        datetime._dttuple = [year, month, day, hour, minute, second, zone]


#==============================================================================
# CalendarNone
#==============================================================================
class CalendarNone(CalendarGeneric):

    """
    Calendar Class with zero days in every month, no leap years, etc.

    This calendar effectively says that every day is the same.
    """

    def __init__(self):
        """
        Constructor
        """
        super(CalendarGeneric, self).__init__("none", month_lengths=[0] * 12)


#==============================================================================
# Calendar360Day
#==============================================================================
class Calendar360Day(CalendarGeneric):

    """
    Calendar Class with every year having 12 30-day months
    """

    def __init__(self):
        """
        Constructor
        """
        super(CalendarGeneric, self).__init__(
            "360_day", month_lengths=[30] * 12)


#==============================================================================
# Calendar365Day
#==============================================================================
class Calendar365Day(CalendarGeneric):

    """
    Gregorian-like Calendar Class with no leap years (365 days)
    """

    def __init__(self):
        """
        Constructor
        """
        super(CalendarGeneric, self).__init__(
            "365_day",
            month_lengths=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])


#==============================================================================
# Calendar366Day
#==============================================================================
class Calendar366Day(CalendarGeneric):

    """
    Gregorian-like Calendar Class with every year a leap year (366 days)
    """

    def __init__(self):
        """
        Constructor
        """
        super(CalendarGeneric, self).__init__(
            "366_day",
            month_lengths=[31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])

    def is_leap_year(self, year):
        """
        Check if a given year is a leap year

        Parameters:
            year (int): The year to check if it is a leap year

        Returns:
            bool: True, if 'year' is a leap year.  False, otherwise.
        """

        # Call abstract base class for type and value checking
        Calendar.is_leap_year(self, year)

        # Every year is a leap year
        return True

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

        # Call abstract base class for type and value checking
        Calendar.days_in_month(self, month, year)

        # Return number of days in month
        return self._month_lengths[month - 1]


#==============================================================================
# CalendarJulian
#==============================================================================
class CalendarJulian(CalendarGeneric):

    """
    Julian Calendar Class
    """

    def __init__(self):
        """
        Constructor
        """
        super(CalendarGeneric, self).__init__(
            "julian",
            month_lengths=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
            leap_year=0, leap_month=2)


#==============================================================================
# CalendarProlepticGregorian
#==============================================================================
class CalendarProlepticGregorian(CalendarGeneric):

    """
    Proleptic Gregorian Calendar Class
    """

    def __init__(self):
        """
        Constructor
        """
        super(CalendarGeneric, self).__init__(
            "proleptic_gregorian",
            month_lengths=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
            leap_year=0, leap_month=2)

    def is_leap_year(self, year):
        """
        Check if a given year is a leap year

        Parameters:
            year (int): The year to check if it is a leap year

        Returns:
            bool: True, if 'year' is a leap year.  False, otherwise.
        """

        # Call abstract base class for type and value checking
        Calendar.is_leap_year(self, year)

        # Gregorian leap years are as follows:
        # 1. The year must be divisible by 4 but not 100, or
        # 2. The year must be divisible by 400
        condition_1 = year % 4 == 0 and not year % 100 == 0
        condition_2 = year % 400 == 0
        if condition_1 or condition_2:
            return True
        else:
            return False


#==============================================================================
# CalendarStandard
#==============================================================================
class CalendarStandard(CalendarGeneric):

    """
    Mixed Julian/Gregorian Calendar Class
    """

    def __init__(self):
        """
        Constructor
        """
        super(CalendarGeneric, self).__init__(
            "standard",
            month_lengths=[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
            leap_year=0, leap_month=2)

    def is_leap_year(self, year):
        """
        Check if a given year is a leap year

        Parameters:
            year (int): The year to check if it is a leap year

        Returns:
            bool: True, if 'year' is a leap year.  False, otherwise.
        """

        # Call abstract base class for type and value checking
        Calendar.is_leap_year(self, year)

        # If year < 1582, then use the Julian rule, otherwise Gregorian
        if year < 1582:
            return CalendarJulian.is_leap_year(self, year)
        else:
            return CalendarProlepticGregorian.is_leap_year(self, year)
