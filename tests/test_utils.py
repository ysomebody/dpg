import unittest
from dpg.utils import *

class Test_Utils(unittest.TestCase):
    def test_int_str_to_bit_str(self):
        result = int_str_to_bit_str('0x3ab', 12)
        expected = '001110101011'
        self.assertEqual(result, expected)

        result = int_str_to_bit_str('18', 8)
        expected = '00010010'
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()