import unittest

from dpg.pattern_vector import PatternVector, to_statements
from dpg.spi_4w.spi_4w_vectors import *

class Test_spi_4w_vectors(unittest.TestCase):

    def test_pattern_start(self):
        result = to_statements(pattern_start('Test_Timeset'))
        expected = PatternVector(['1', '0', 'X', '0'], comment='Start of the pattern', timeset='Test_Timeset').get_statement()
        self.assertEqual(result, expected)

    def test_pattern_end(self):
        result = to_statements(pattern_end())
        expected = PatternVector(['X', 'X', 'X', 'X'], comment='End of the pattern', opcode='halt').get_statement()
        self.assertEqual(result, expected)

    def test_frame_start(self):
        result = to_statements(frame_start())
        expected = PatternVector(['1', '0', 'X', '0'], comment='Start of SPI 4W Frame', opcode='repeat(5)').get_statement()
        self.assertEqual(result, expected)

    def test_frame_end(self):
        result = to_statements(frame_end())
        expected = PatternVector(['1', '0', 'X', '0'], comment='End of SPI 4W Frame', opcode='repeat(5)').get_statement()
        self.assertEqual(result, expected)

    def test_wait(self):
        result = to_statements(wait(3))
        expected = PatternVector(['1', '0', 'X', '0'], comment=f'Wait for 3 Timeset', opcode=f'repeat(3)').get_statement()
        self.assertEqual(result, expected)

    def test_capture_start(self):
        result = to_statements(capture_start())
        expected = PatternVector(['1', '0', 'X', '0'], opcode='capture_start(DATA_Read)').get_statement()
        self.assertEqual(result, expected)

    def test_capture_stop(self):
        result = to_statements(capture_stop())
        expected = PatternVector(['1', '0', 'X', '1'], opcode='capture_stop').get_statement()
        self.assertEqual(result, expected)

    def test_write_cmd(self):
        result = to_statements(write_cmd())
        expected = to_statements([
            PatternVector(['0', '0', 'X', '1'], comment='Write Command'),
            PatternVector(['0', '1', 'X', '1'], comment='Write Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Write Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Write Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Write Command'),
        ])
        self.assertEqual(result, expected)

    def test_read_collect_cmd(self):
        result = to_statements(read_collect_cmd())
        expected = to_statements([
            PatternVector(['0', '0', 'X', '1'], comment='Read Collect Command'),
            PatternVector(['0', '1', 'X', '1'], comment='Read Collect Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Read Collect Command'),
            PatternVector(['0', '1', 'X', '1'], comment='Read Collect Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Read Collect Command'),
        ])
        self.assertEqual(result, expected)

    def test_read_value_cmd(self):
        result = to_statements(read_value_cmd())
        expected = to_statements([
            PatternVector(['0', '0', 'X', '1'], comment='Read Value Command'),
            PatternVector(['0', '1', 'X', '1'], comment='Read Value Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Read Value Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Read Value Command'),
            PatternVector(['0', '0', 'X', '1'], comment='Read Value Command'),
        ])
        self.assertEqual(result, expected)

    def test_write_address(self):
        result = to_statements(write_address('0x3cd'))
        # 0x3cd = 011 1100 1101 b
        expected = to_statements([
            PatternVector(['0', '0', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '1', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '1', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '1', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '1', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '0', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '0', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '1', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '1', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '0', 'X', '1'], comment='Address 0x3cd'),
            PatternVector(['0', '1', 'X', '1'], comment='Address 0x3cd'),
        ])
        self.assertEqual(result, expected)

    def test_write_data(self):
        result = to_statements(write_data('0xabcd'))
        # 0xabcd = 1010 1011 1100 1101 b
        expected = to_statements([
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '0', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '0', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '0', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '0', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '0', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '0', 'X', '1'], comment='Data 0xabcd'),
            PatternVector(['0', '1', 'X', '1'], comment='Data 0xabcd'),
        ])
        self.maxDiff = None
        self.assertEqual(result, expected)

    def test_read_data(self):
        result = to_statements(read_data())
        expected = to_statements([PatternVector(['0', 'X', 'V', '1'], comment='Read', opcode='capture')] * 16)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()