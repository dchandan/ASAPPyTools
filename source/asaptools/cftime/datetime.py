"""
CFTime.DateTime -- A module for describing date-time objects

Copyright 2015, University Corporation for Atmospheric Research
See the LICENSE.txt document or license details
"""


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
        a numeric UTC offset (int), and the calendar associated with the
        date-time can be specified by the appropriate string name or specific
        CFCalendar class.

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
            calendar (str, CFCalendar): The name (str) or instance of the
                specific CFCalendar class to associate with the date-time.  If
                a str, then the *create_calendar* factory function is used
                to create the CFCalendar instance internally.  If a CFCalendar,
                then this instance is used internally.
        """

        # Check Types
