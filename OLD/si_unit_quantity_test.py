import unittest

from natural import *

class TestBuiltins(unittest.TestCase):
    def test_unitless(self):
        unitless_1 = SiUnitQuantity(magnitude = 3.5)
        len_1 = SiUnitQuantity(magnitude = 2.7, exponents = {"length": 1})
        len_2 = SiUnitQuantity(magnitude = 1.9, exponents = {"length": 1})
        unitless_2 = len_1 / len_2
        self.assertTrue(unitless_1.is_unitless())
        self.assertTrue(unitless_2.is_unitless())
        self.assertFalse(len_1.is_unitless())
        self.assertFalse(len_2.is_unitless())

    def test_match_units(self):
        unitless_1 = SiUnitQuantity(magnitude = -0.7)
        unit_1 = SiUnitQuantity(magnitude = 0.2, exponents = {"length": 1, "mass": 2, "current": -1})
        unit_2 = SiUnitQuantity(magnitude = 104, exponents = {"length": 1, "mass": 2, "current": -1})
        unitless_2 = unit_1 / unit_2
        self.assertTrue(unitless_1.match_units(unitless_2))
        self.assertTrue(unitless_2.match_units(unitless_1))
        self.assertTrue(unit_1.match_units(unit_2))
        self.assertTrue(unit_2.match_units(unit_1))
        self.assertFalse(unit_1.match_units(unitless_2))
        self.assertFalse(unitless_1.match_units(unit_2))

    def test_str_simple_1(self):
        velocity_1 = SiUnitQuantity(magnitude = 7, exponents = {"length": 1, "time": -1})
        self.assertEqual(str(velocity_1), "7 m/s")
        
    def test_str_compound(self):
        pass # upcoming: compound units

    def test_str_as_repr(self):
        pass # upcoming: parser

class TestArithmetic(unittest.TestCase):
    def test_add_simple(self):
        unitless_1 = SiUnitQuantity(magnitude = 1.2) + SiUnitQuantity(magnitude = -0.9)
        self.assertTrue(unitless_1.is_unitless())
        self.assertAlmostEqual(unitless_1.magnitude, 0.3)
        energy_1 = SiUnitQuantity(magnitude = 2, exponents = {"length": 2, "mass": 1, "time": -2}) + SiUnitQuantity(magnitude = 2.7, exponents = {"length": 2, "mass": 1, "time": -2})
        energy_2 = SiUnitQuantity(magnitude = -0.4, exponents = {"length": 2, "mass": 1, "time": -2})
        self.assertTrue(energy_1.match_units(energy_2))
        self.assertAlmostEqual(energy_1.magnitude, 4.7)

    def test_add_unit_mismatch(self):
        unitless_1 = SiUnitQuantity(magnitude = 9)
        acc_1 = SiUnitQuantity(magnitude = 2, exponents = {"length": 1, "time": -2})
        power_1 = SiUnitQuantity(magnitude = 1.4e-5, exponents = {"length": 2, "mass": 1, "time": -3})
        with self.assertRaises(TypeError):
            bad_quantity_1 = unitless_1 + acc_1
        with self.assertRaises(TypeError):
            bad_quantity_2 = acc_1 + power_1

    def test_sub_simple(self):
        unitless_1 = SiUnitQuantity(magnitude = 1.2) - SiUnitQuantity(magnitude = -0.9)
        self.assertTrue(unitless_1.is_unitless())
        self.assertAlmostEqual(unitless_1.magnitude, 2.1)
        energy_1 = SiUnitQuantity(magnitude = 2, exponents = {"length": 2, "mass": 1, "time": -2}) - SiUnitQuantity(magnitude = 2.7, exponents = {"length": 2, "mass": 1, "time": -2})
        energy_2 = SiUnitQuantity(magnitude = 9.3, exponents = {"length": 2, "mass": 1, "time": -2})
        self.assertTrue(energy_1.match_units(energy_2))
        self.assertAlmostEqual(energy_1.magnitude, -0.7)

    def test_sub_unit_mismatch(self):
        unitless_1 = SiUnitQuantity(magnitude = 9)
        acc_1 = SiUnitQuantity(magnitude = 2, exponents = {"length": 1, "time": -2})
        power_1 = SiUnitQuantity(magnitude = 1.4e-5, exponents = {"length": 2, "mass": 1, "time": -3})
        with self.assertRaises(TypeError):
            bad_quantity_1 = unitless_1 - acc_1
        with self.assertRaises(TypeError):
            bad_quantity_2 = acc_1 - unitless_1
        with self.assertRaises(TypeError):
            bad_quantity_3 = acc_1 - power_1

if __name__ == "__main__":
    unittest.main(verbosity = 2)
