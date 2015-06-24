"""
CFTime Package -- Unit Tests for Calendars module

Copyright 2015, University Corporation for Atmospheric Research
See LICENSE.txt for details
"""

import unittest

from asaptools.cftime import calendars


class CalendarsTests(unittest.TestCase):

    def setUp(self):
        self.name_1 = "Cal #1"
        self.month_lengths_1 = [30] * 12
        self.leap_year_1 = None
        self.leap_month_1 = None
        self.cal_1 = calendars.create_calendar(
            self.name_1, month_lengths=self.month_lengths_1)

        self.name_2 = "Cal #2"
        self.month_lengths_2 = [31, 30, 31, 30, 31, 30, 31, 30, 30, 31, 30, 31]
        self.leap_year_2 = 1992
        self.leap_month_2 = 1
        self.cal_2 = calendars.create_calendar(
            self.name_2, month_lengths=self.month_lengths_2,
            leap_year=self.leap_year_2, leap_month=self.leap_month_2)

    def testCreateCalendar(self):
        self.assertIsInstance(self.cal_1, calendars.CFCalendar,
                              "Factory function failed to create calendar 1")
        self.assertIsInstance(self.cal_2, calendars.CFCalendar,
                              "Factory function failed to create calendar 2")

    def testName(self):
        self.assertEqual(self.cal_1.name(), self.name_1,
                         "Calender 1 has wrong name")
        self.assertEqual(self.cal_2.name(), self.name_2,
                         "Calender 2 has wrong name")

    def testIsLeapYear(self):
        self.assertEqual(self.cal_1.is_leap_year(1131), False,
                         "Calender 1 leap year computation is wrong")
        self.assertEqual(self.cal_1.is_leap_year(4), False,
                         "Calender 1 leap year computation is wrong")
        self.assertEqual(self.cal_2.is_leap_year(1131), False,
                         "Calender 2 leap year computation is wrong")
        self.assertEqual(self.cal_2.is_leap_year(self.leap_year_2 + 8), True,
                         "Calender 2 leap year computation is wrong")

    def testDaysInMonth(self):
        for i in range(12):
            self.assertEqual(self.cal_1.days_in_month(i + 1), 30,
                             "Calendar 1 days in month " +
                             str(i + 1) + " is wrong")
            self.assertEqual(self.cal_2.days_in_month(i + 1),
                             self.month_lengths_2[i],
                             "Calendar 2 days in month " +
                             str(i + 1) + " is wrong")
        self.assertEqual(self.cal_2.days_in_month(1, 1992 + 8), 32,
                         "Calendar 2 days in month 1 on leap year is wrong")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
