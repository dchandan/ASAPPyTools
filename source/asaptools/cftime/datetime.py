"""
CFTime.DateTime -- A module for describing date-time objects

Copyright 2015, University Corporation for Atmospheric Research
See the LICENSE.txt document or license details
"""

import calendars


#==============================================================================
# DateTime - A class that contains a single date-time with specified calendar
#==============================================================================
class DateTime(object):

    """
    DateTime - A class that contains a single date-time with specified calendar
    """

    def __init__(self, year, month, day, hour, minute, second,
                 zone=0.0, calendar="standard"):
        """
        Constructor

        Build a date-time from the (year, month, day, hour, minute, second)
        specified by input.  Additionally, the time-zone can be specified by
        a numeric UTC hour-offset (float), and the calendar associated with the
        date-time can be specified by the appropriate string name or specific
        Calendar class.

        NOTE: Without an associated Calendar object, the DateTime tuple
        (year, month, day, hour, minute, second) cannot be validated or
        verified.  Hence, except for type-checking, any value for the
        DateTime tuple quantitiees is accepted as input.  It is the Calendar's,
        responsibility to "normalize" these values to create a valid tuple.
        Hence, the DateTime object may not reflect exactly the numbers
        given as input.        

        Parameters:
            year (int): The numeric year.  If specified as a float, it is
                truncated to an integer.
            month (int): The numeric month, a number from 1 to 12.  If
                specified as a float, it is truncated to an integer.
            day (int): The numeric day of the month, a number from 1 to the
                number of days in the given month.  If specified as a float, 
                it is truncated to an integer.
            hour (int): The numeric hour in the day, a number from 0 to 23.
                If specified as a float, it is truncated to an integer.
            minute (int): The numeric minute in the hour, a number from 0 to
                59.  If specified as a float, it is truncated to an integer.
            second (float): The numeric second in the minute, a number in the
                range [0.,60.).  If specified as an int, it is converted to a
                float.

        Keyword Arguments:
            zone (float): The time-zone associated with the date-time.  It
                should be given as a floating point number specifying the
                UTC offset.  Defaults to 0.0.
            calendar (str, Calendar): The name (str) or instance of the
                specific Calendar class to associate with the date-time.  If
                a str, then the *create_calendar* factory function is used
                to create the Calendar instance internally.  If a CFCalendar,
                then this instance is used internally.
        """
        # Interpret the calendar argument
        if type(calendar) is str:
            self._calendar = calendars.create_calendar(calendar)
        elif isinstance(calendar, calendars.Calendar):
            self._calendar = calendar
        else:
            err_msg = "Unrecognized calendar input in DateTime object"
            raise TypeError(err_msg)

        # Convert input to desired type
        self._dttuple = [int(year), int(month), int(day),
                         int(hour), int(minute), float(second), float(zone)]

        # Normalize the data using the calendar
        self._calendar.normalize_datetime(self)
