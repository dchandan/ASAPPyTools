"""
Unit tests for the CFTime module

Copyright 2015, University Corporation for Atmospheric Research
See LICENSE.txt for details
"""

import unittest

from asaptools import cftime


class CFTimeTests(unittest.TestCase):

    def testAliasToUnit(self):
        u = cftime._alias_to_unit('secs')
        self.assertEqual(u, 'seconds',
                         'Failed to map alias')
        u = cftime._alias_to_unit('hour')
        self.assertEqual(u, 'hours',
                         'Failed to map alias')
        u = cftime._alias_to_unit('min')
        self.assertEqual(u, 'minutes',
                         'Failed to map alias')
        u = cftime._alias_to_unit('yrs')
        self.assertEqual(u, 'years',
                         'Failed to map alias')
        self.assertRaises(ValueError,
                          cftime._alias_to_unit,
                          'secondi')
        self.assertRaises(ValueError,
                          cftime._alias_to_unit,
                          'y')

    def testUnitToIndex(self):
        u = cftime._unit_to_index('yrs')
        self.assertEqual(u, 0,
                         'Failed to find index')
        u = cftime._unit_to_index('mos')
        self.assertEqual(u, 1,
                         'Failed to find index')
        u = cftime._unit_to_index('d')
        self.assertEqual(u, 2,
                         'Failed to find index')
        u = cftime._unit_to_index('h')
        self.assertEqual(u, 3,
                         'Failed to find index')
        u = cftime._unit_to_index('min')
        self.assertEqual(u, 4,
                         'Failed to find index')
        u = cftime._unit_to_index('s')
        self.assertEqual(u, 5,
                         'Failed to find index')
        self.assertRaises(ValueError,
                          cftime._unit_to_index,
                          'y')

    def testIndexToUnit(self):
        u = cftime._index_to_unit(0)
        self.assertEqual(u, 'years',
                         'Failed to map index')
        u = cftime._index_to_unit(1)
        self.assertEqual(u, 'months',
                         'Failed to map index')
        u = cftime._index_to_unit(2)
        self.assertEqual(u, 'days',
                         'Failed to map index')
        u = cftime._index_to_unit(3)
        self.assertEqual(u, 'hours',
                         'Failed to map index')
        u = cftime._index_to_unit(4)
        self.assertEqual(u, 'minutes',
                         'Failed to map index')
        u = cftime._index_to_unit(5)
        self.assertEqual(u, 'seconds',
                         'Failed to map index')
        self.assertRaises(ValueError,
                          cftime._index_to_unit,
                          -2)
        self.assertRaises(ValueError,
                          cftime._index_to_unit,
                          7)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
