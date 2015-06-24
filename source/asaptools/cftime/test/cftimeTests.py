"""
Unit tests for the CFTime module

Copyright 2015, University Corporation for Atmospheric Research
See LICENSE.txt for details
"""

import unittest

from asaptools.cftime import cftime


class CFTimeTests(unittest.TestCase):

    def testAliasToUnit(self):
        for ualias, unit in cftime.__ALIASES__.items():
            self.assertEqual(cftime.alias_to_unit(ualias),
                             unit, "Failed to map alias " + ualias +
                             " to " + unit)
        self.assertRaises(ValueError, cftime.alias_to_unit,
                          'secondi')
        self.assertRaises(ValueError, cftime.alias_to_unit,
                          'y')

    def testUnitToIndex(self):
        for i in range(len(cftime.__INDICES__)):
            unit = cftime.__INDICES__[i]
            self.assertEqual(cftime.__unit_to_index__(unit), i,
                             "Failed to find index of unit " + unit)
        self.assertRaises(ValueError, cftime.__unit_to_index__,
                          'y')
        self.assertRaises(ValueError, cftime.__unit_to_index__,
                          'x')

    def testIndexToUnit(self):
        for i in range(len(cftime.__INDICES__)):
            self.assertEqual(cftime.__index_to_unit__(i),
                             cftime.__INDICES__[i],
                             'Failed to map index ' + str(i))
        self.assertRaises(IndexError, cftime.__index_to_unit__, -2)
        self.assertRaises(IndexError, cftime.__index_to_unit__, 7)

    def testIsDTTuple(self):
        arg = [1, 2, 3, 4, 5, 6]
        self.assertTrue(cftime.__is_dttuple__(arg),
                        "Failed to interpret date-time tuple " + str(arg))
        arg = [1, 2, 3, 4, 5, 6.8]
        self.assertTrue(cftime.__is_dttuple__(arg),
                        "Failed to interpret date-time tuple " + str(arg))
        arg = [1, 2, 3L, 4, 5, 6.8]
        self.assertTrue(cftime.__is_dttuple__(arg),
                        "Failed to interpret date-time tuple " + str(arg))
        arg = (1, 2, 3L, 4, 5, 6.8)
        self.assertTrue(cftime.__is_dttuple__(arg),
                        "Failed to interpret date-time tuple " + str(arg))
        arg = [1, 2, 3, 4]
        self.assertFalse(cftime.__is_dttuple__(arg),
                         "Failed to interpret date-time tuple " + str(arg))
        arg = [1, 2, 3, 4, 'a', 0L]
        self.assertFalse(cftime.__is_dttuple__(arg),
                         "Failed to interpret date-time tuple " + str(arg))
        arg = "123456"
        self.assertFalse(cftime.__is_dttuple__(arg),
                         "Failed to interpret date-time tuple " + str(arg))

    def testInitCFDateTimeDeltaParams(self):
        params = (1, 2L, 3, 4, 5, 6.2)
        obj = cftime.CFDateTimeDelta(*params)
        self.assertTupleEqual(obj._dttuple, params,
                              "Failed to construct CFDatTimeDelta")

    def testInitCFDateTimeDeltaTuple(self):
        params = (1, 2L, 3, 4, 5, 6.2)
        obj = cftime.CFDateTimeDelta(params)
        self.assertTupleEqual(obj._dttuple, params,
                              "Failed to construct CFDatTimeDelta")

    def testInitCFDateTimeDeltaList(self):
        params = (1, 2L, 3, 4, 5, 6.2)
        obj = cftime.CFDateTimeDelta(list(params))
        self.assertTupleEqual(obj._dttuple, params,
                              "Failed to construct CFDatTimeDelta")

    def testCFDateTimeDeltaAdd(self):
        dtd1 = cftime.CFDateTimeDelta([3, 3, 3, 3, 3, 3])
        dtd2 = cftime.CFDateTimeDelta([2, 2, 2, 2, 2, 2])
        result = dtd1 + dtd2
        expected = (5, 5, 5, 5, 5, 5)
        self.assertTupleEqual(result._dttuple, expected,
                              "CFDateTimeDelta addition failed")

    def testCFDateTimeDeltaSum(self):
        dtd1 = cftime.CFDateTimeDelta([3, 3, 3, 3, 3, 3])
        dtd2 = cftime.CFDateTimeDelta([2, 2, 2, 2, 2, 2])
        dtd3 = cftime.CFDateTimeDelta([1, 1, 1, 1, 1, 1])
        result = sum([dtd1, dtd2, dtd3])
        expected = (6, 6, 6, 6, 6, 6)
        self.assertTupleEqual(result._dttuple, expected,
                              "CFDateTimeDelta sum failed")

    def testCFDateTimeDeltaIAdd(self):
        dtd = cftime.CFDateTimeDelta([3, 3, 3, 3, 3, 3])
        result = cftime.CFDateTimeDelta([2, 2, 2, 2, 2, 2])
        result += dtd
        expected = (5, 5, 5, 5, 5, 5)
        self.assertTupleEqual(result._dttuple, expected,
                              "CFDateTimeDelta addition assignment failed")

    def testCFDateTimeDeltaSub(self):
        dtd1 = cftime.CFDateTimeDelta([3, 3, 3, 3, 3, 3])
        dtd2 = cftime.CFDateTimeDelta([2, 2, 2, 2, 2, 2])
        result = dtd1 - dtd2
        expected = (1, 1, 1, 1, 1, 1)
        self.assertTupleEqual(result._dttuple, expected,
                              "CFDateTimeDelta subtraction failed")
        result = dtd2 - dtd1
        expected = (-1, -1, -1, -1, -1, -1)
        self.assertTupleEqual(result._dttuple, expected,
                              "CFDateTimeDelta subtraction failed")

    def testCFDateTimeDeltaISub(self):
        dtd = cftime.CFDateTimeDelta([3, 3, 3, 3, 3, 3])
        result = cftime.CFDateTimeDelta([2, 2, 2, 2, 2, 2])
        result -= dtd
        expected = (-1, -1, -1, -1, -1, -1)
        self.assertTupleEqual(result._dttuple, expected,
                              "CFDateTimeDelta subtraction assignment failed")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
