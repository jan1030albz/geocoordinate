import unittest  # NOQA
from customexceptions import InvalidArgument  # NOQA
from geocoordinate import GeoCoordinate  # NOQA


class GeoCoordinateTest(unittest.TestCase):
    def test_validations(self):
        """Tests the argument validations if it will raise a certain exception when the user inputs arguments
        that will cause alot more problems in the future, especially in calculations."""
        # if any of the argument is negative
        self.assertRaises(InvalidArgument, GeoCoordinate, *(-1, 2, 3))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(1, -2, 3))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(1, 2, -3))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(-1, -2, 3))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(-1, 2, -3))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(1, -2, -3))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(-1, -2, -3))
        # if minutes and/or seconds >= 60:
        # Note that if user inputs 59.99999999 in seconds, will not raise any exception.
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0, 60, 60))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0, 60, 0))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0, 0, 60))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0, 61, 61))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0, 61, 0))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0, 0, 61))
        # if degrees and/or minutes is float:
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0.0, 0.0, 0))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0, 0.0, 0))
        self.assertRaises(InvalidArgument, GeoCoordinate, *(0.0, 0, 0))
        # if positional arguments are zero, and negative=True
        self.assertRaises(InvalidArgument, GeoCoordinate,
                          *(0, 0, 0), negative=True)

    def test_basic_arithmetic_ops(self):
        op_1 = GeoCoordinate(1, 0, 0)
        op_neg1 = GeoCoordinate(1, 0, 0, True)
        op_2 = GeoCoordinate(0, 30, 0)
        op_neg2 = GeoCoordinate(0, 30, 0, True)
        op_secclose1 = GeoCoordinate(0, 0, 23.499)
        op_negsecclose1 = GeoCoordinate(0, 0, 23.499, True)
        op_secclose2 = GeoCoordinate(0, 0, 36.499, )
        op_negsecclose2 = GeoCoordinate(0, 0, 36.499, True)
        op_minclose1 = GeoCoordinate(0, 29, 23.499)
        op_negminclose1 = GeoCoordinate(0, 29, 23.499, True)
        op_minclose2 = GeoCoordinate(0, 30, 36.499)
        op_negminclose2 = GeoCoordinate(0, 30, 36.499, True)
        # -----ADDITION----- #
        # GeoCoordinate + integer = GeoCoordinate
        self.assertEqual(op_1 + 1.5, GeoCoordinate(2, 30, 0))
        self.assertEqual(1.5 + op_1, GeoCoordinate(2, 30, 0))
        self.assertIsInstance(op_1 + 1.5, GeoCoordinate)
        self.assertIsInstance(1.5 + op_1, GeoCoordinate)
        # Test positive + positive
        self.assertEqual(op_1 + op_2, GeoCoordinate(1, 30, 0))
        self.assertEqual(op_2 + op_1, GeoCoordinate(1, 30, 0))
        # Test positive + negative = positive
        self.assertEqual(op_1 + op_neg2, GeoCoordinate(0, 30, 0))
        self.assertEqual(op_neg2 + op_1, GeoCoordinate(0, 30, 0))
        # Test positive + negative = negative
        self.assertEqual(op_neg1 + op_2, GeoCoordinate(0, 30, 0, True))
        self.assertEqual(op_2 + op_neg1, GeoCoordinate(0, 30, 0, True))
        # Test negative + negative
        self.assertEqual(op_neg1 + op_neg2, GeoCoordinate(1, 30, 0, True))
        self.assertEqual(op_neg2 + op_neg1, GeoCoordinate(1, 30, 0, True))
        # Test result close to 60 seconds
        self.assertEqual(op_secclose1 + op_secclose2, GeoCoordinate(0, 1, 0))
        self.assertEqual(op_negsecclose1 + op_negsecclose2,
                         GeoCoordinate(0, 1, 0, True))
        # Test result close to 60 minutes, 60 seconds and results to 1 degree flat
        self.assertEqual(op_minclose1 + op_minclose2, GeoCoordinate(1, 0, 0))
        self.assertEqual(op_negminclose1 + op_negminclose2,
                         GeoCoordinate(1, 0, 0, True))
        # -----SUBTRACTION----- #
        # Test positive - positive
        self.assertEqual(op_1 - op_2, GeoCoordinate(0, 30, 0))
        self.assertEqual(op_2 - op_1, GeoCoordinate(0, 30, 0, True))
        # Test positive - negative = positive
        self.assertEqual(op_1 - op_neg2, GeoCoordinate(1, 30, 0))
        self.assertEqual(op_2 - op_neg1, GeoCoordinate(1, 30, 0))
        # Test negative - postive = negative
        self.assertEqual(op_neg2 - op_1, GeoCoordinate(1, 30, 0, True))
        self.assertEqual(op_neg1 - op_2, GeoCoordinate(1, 30, 0, True))
        # Test negative - negative
        self.assertEqual(op_neg1 + op_neg2, GeoCoordinate(1, 30, 0, True))
        self.assertEqual(op_neg2 + op_neg1, GeoCoordinate(1, 30, 0, True))
        # -----MULTIPLICATION----- #
        # Note that in multiplication, order won't matter
        # Integers
        self.assertEqual(15 * op_1, GeoCoordinate(15, 0, 0))
        self.assertEqual(-15 * op_1, GeoCoordinate(15, 0, 0, True))
        self.assertEqual(15 * op_neg1, GeoCoordinate(15, 0, 0, True))
        self.assertEqual(-15 * op_neg1, GeoCoordinate(15, 0, 0))
        self.assertEqual(4 * op_2, GeoCoordinate(2, 0, 0))
        self.assertEqual(-4 * op_2, GeoCoordinate(2, 0, 0, True))
        self.assertEqual(4 * op_neg2, GeoCoordinate(2, 0, 0, True))
        self.assertEqual(-4 * op_neg2, GeoCoordinate(2, 0, 0))
        # Floats
        self.assertEqual(1.5 * op_1, GeoCoordinate(1, 30, 0))
        self.assertEqual(-1.5 * op_1, GeoCoordinate(1, 30, 0, True))
        self.assertEqual(1.5 * op_neg1, GeoCoordinate(1, 30, 0, True))
        self.assertEqual(-1.5 * op_neg1, GeoCoordinate(1, 30, 0))
        # Float, but will involve seconds
        op_mul1 = GeoCoordinate(0, 30, 30)
        op_negmul1 = GeoCoordinate(0, 30, 30, True)
        self.assertEqual(1.5 * op_mul1, GeoCoordinate(0, 45, 45))
        self.assertEqual(-1.5 * op_mul1, GeoCoordinate(0, 45, 45, True))
        self.assertEqual(1.5 * op_negmul1, GeoCoordinate(0, 45, 45, True))
        self.assertEqual(-1.5 * op_negmul1, GeoCoordinate(0, 45, 45))
        # Float, but will involve seconds and degrees
        self.assertEqual(2.5 * op_mul1, GeoCoordinate(1, 16, 15))
        self.assertEqual(-2.5 * op_mul1, GeoCoordinate(1, 16, 15, True))
        self.assertEqual(2.5 * op_negmul1, GeoCoordinate(1, 16, 15, True))
        self.assertEqual(-2.5 * op_negmul1, GeoCoordinate(1, 16, 15))
        # -----DIVISION----- #
        # Note that in division, order matters
        op_div1 = GeoCoordinate(2, 30, 0)
        self.assertEqual(op_1 / 2, GeoCoordinate(0, 30, 0))
        self.assertEqual(2 / op_1, GeoCoordinate(2, 0, 0))
        self.assertEqual(op_div1 / 15, GeoCoordinate(0, 10, 0))
        self.assertEqual(15 / op_div1, GeoCoordinate(6, 0, 0))

    def test_equal_comparison_ops(self):
        # Test abs_tol (absolute tolerance)
        # MODIFIED 0.0000001 vs MODIFIED 0.00001 vs DEFAULT 0.000001
        # MODIFIED -----------------------------------------------------------
        GeoCoordinate.set_comparison_tolerance(
            abs_tol=0.0000001)
        # absolutely no difference
        self.assertEqual(GeoCoordinate(1, 0, 0),
                         GeoCoordinate(1, 0, 0))
        # Decimal Degrees equivalent to 0.1
        self.assertNotEqual(GeoCoordinate(0, 6, 0),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.01
        self.assertNotEqual(GeoCoordinate(0, 0, 36),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.001
        self.assertNotEqual(GeoCoordinate(0, 0, 3.6),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.0001
        self.assertNotEqual(GeoCoordinate(0, 0, 0.36),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.00001
        self.assertNotEqual(GeoCoordinate(0, 0, 0.036),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.000001 (10cm-50cm precision)
        self.assertNotEqual(GeoCoordinate(0, 0, 0.0036),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.0000001 (1cm-50cm precision)
        self.assertEqual(GeoCoordinate(0, 0, 0.00036),
                         GeoCoordinate(0, 0, 0))
        # 59.9963  in seconds (0.0036 diff from 60 seconds or 1 minute), increment minutes, 60 in minutes, increment degrees
        # Will not round up
        self.assertNotEqual(GeoCoordinate(1, 59, 59.9963),
                            GeoCoordinate(2, 0, 0))
        self.assertEqual(GeoCoordinate(1, 59, 59.9964),
                         GeoCoordinate(2, 0, 0))

        # DEFAULT ------------------------------------------------------------
        GeoCoordinate.set_comparison_tolerance(abs_tol=0.000001)
        # absolutely no difference
        self.assertEqual(GeoCoordinate(1, 0, 0),
                         GeoCoordinate(1, 0, 0))
        # Decimal Degrees equivalent to 0.1
        self.assertNotEqual(GeoCoordinate(0, 6, 0),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.01
        self.assertNotEqual(GeoCoordinate(0, 0, 36),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.001
        self.assertNotEqual(GeoCoordinate(0, 0, 3.6),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.0001
        self.assertNotEqual(GeoCoordinate(0, 0, 0.36),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.00001
        self.assertNotEqual(GeoCoordinate(0, 0, 0.036),
                            GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.000001 (10cm-50cm precision)
        self.assertEqual(GeoCoordinate(0, 0, 0.0036),
                         GeoCoordinate(0, 0, 0))
        # Decimal Degrees equivalent to 0.0000001 (1cm-50cm precision)
        self.assertEqual(GeoCoordinate(0, 0, 0.00036),
                         GeoCoordinate(0, 0, 0))
        # 59.999 in seconds, increment minutes, 60 in minutes, increment degrees
        self.assertNotEqual(GeoCoordinate(1, 59, 59.9963),
                            GeoCoordinate(2, 0, 0))
        self.assertEqual(GeoCoordinate(1, 59, 59.9964),
                         GeoCoordinate(2, 0, 0))

    def test_lt_gt_comparison_ops(self):
        # Default absolute tolerance
        GeoCoordinate.set_comparison_tolerance(abs_tol=0.000001)
        self.assertGreater(GeoCoordinate(1, 0, 0.0037),
                           GeoCoordinate(1, 0, 0.0))
        self.assertEqual(GeoCoordinate(1, 0, 0.0036),
                         GeoCoordinate(1, 0, 0.0))
        self.assertGreater(GeoCoordinate(1, 0, 0.0),
                           GeoCoordinate(1, 0, 0.0, negative=True))
        self.assertGreater(GeoCoordinate(1, 0, 59.999),
                           GeoCoordinate(1, 0, 59.99))
        # A difference of greater than 0.0036 seconds will be considered not equal
        self.assertGreater(GeoCoordinate(1, 1, 0),
                           GeoCoordinate(1, 0, 59.9963))
        # A difference of less than or equal to 0.0036 seconds will be considered equal
        self.assertEqual(GeoCoordinate(1, 1, 0),
                         GeoCoordinate(1, 0, 59.9964))
        # A difference of less than or equal to 0.0036 seconds will be considered equal
        self.assertEqual(GeoCoordinate(1, 0, 0.0036),
                         GeoCoordinate(1, 0, 0.0))
        # the lefthand rounds seconds to 60, reset to zero, and increments minutes by 1
        # while the righthand remains the same
        # this is greater than comparison
        self.assertGreaterEqual(GeoCoordinate(1, 0, 59.9964),
                                GeoCoordinate(1, 0, 59.9963))
        # this is equal comparison
        self.assertGreaterEqual(GeoCoordinate(1, 0, 59.9965),
                                GeoCoordinate(1, 0, 59.9964))

    # __str__ and __repr__
    def test_presentation(self):
        # REPR
        self.assertEqual(repr(GeoCoordinate(1, 2, 3)),
                         'GeoCoordinate(1, 2, 3, negative=False)')
        self.assertEqual(repr(GeoCoordinate(1, 2, 3, negative=True)),
                         'GeoCoordinate(1, 2, 3, negative=True)')
        # STR
        self.assertEqual(str(GeoCoordinate(1, 2, 3)), '1° 2\' 3"')
        self.assertEqual(str(GeoCoordinate(1, 2, 3, negative=True)), '-1° 2\' 3"')  # NOQA


if __name__ == '__main__':
    unittest.main()
