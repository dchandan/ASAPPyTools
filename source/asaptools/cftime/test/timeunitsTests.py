"""
CFTime Package -- Unit Tests for TimeUnits module

Copyright 2015, University Corporation for Atmospheric Research
See LICENSE.txt for details
"""

import unittest

from asaptools.cftime import timeunits


class TimeUnitsTests(unittest.TestCase):

    def setUp(self):
        self.alias_map = timeunits.__ALIASES__
        for stdunit in timeunits.__STANDARDS__:
            self.alias_map[stdunit] = stdunit
        for alias, stdunit in self.alias_map.items():
            self.alias_map[alias.upper()] = stdunit
        self.bad_names = ['secondi', 'y', 'x', '32h']
        self.bad_types = [1, 1.23, [1], (5, 3)]

    def testFindUnit(self):
        for ualias, stdunit in self.alias_map.items():
            self.assertEqual(timeunits.find_unit(ualias),
                             stdunit, "Failed to map alias " + ualias +
                             " to " + stdunit)
        for ualias in self.bad_names:
            self.assertRaises(ValueError, timeunits.find_unit, ualias)
        for ualias in self.bad_types:
            self.assertRaises(TypeError, timeunits.find_unit, ualias)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
