import unittest
from dpg.utils import *


class Test_Utils(unittest.TestCase):
    def test_int_to_bits_msb_first(self):
        result = int_to_bits_msb_first('0x3ab', 12)
        expected = '001110101011'
        self.assertEqual(result, expected)

        result = int_to_bits_msb_first('939', 12)
        expected = '001110101011'
        self.assertEqual(result, expected)

    def test_int_to_bits_lsb_first(self):
        result = int_to_bits_lsb_first('0x3ab', 12)
        expected = '110101011100'
        self.assertEqual(result, expected)

        result = int_to_bits_lsb_first('939', 12)
        expected = '110101011100'
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
