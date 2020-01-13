import unittest

from dpg.pattern_vector import PatternVector, to_statements
from dpg.bml.bml_vectors import *


class Test_bml_vectors(unittest.TestCase):
    def _expect_writing_bits(self, bits_str, comment):
        return to_statements([PatternVector(['1', 'X', bit, 'X', 'X'], comment=comment) for bit in bits_str])

    def test_pattern_start(self):
        result = to_statements(sync_header())
        expected = to_statements([
            PatternVector(['1', 'X', '0', 'X', 'X']),
            PatternVector(['1', 'X', '1', 'X', 'X'], opcode='repeat(5)', comment='Sync header'),
        ])
        self.assertEqual(result, expected)

    def test_chip_select(self):
        result = to_statements(chip_select('30'))
        expected = self._expect_writing_bits('0011101', 'ChipID 30')
        self.assertEqual(result, expected)

    def test_chip_select_out_of_range(self):
        with self.assertRaises(Exception) as ctx:
            chip_select('-1')
            self.assertIn('-1', str(ctx.exception))

        with self.assertRaises(Exception) as ctx:
            chip_select('32')
            self.assertIn('32', str(ctx.exception))

    def test_operation_mode(self):
        test_cases = [
            #Input:           Expected Ouput:
            #op_mode, r_w,    op_bits, op comment,    r_w bit, r_w comment
            ('0',     'r',    '00',    'Normal',      '1',     'Read'),
            ('0',     'w',    '00',    'Normal',      '0',     'Write'),
            ('1',     'w',    '10',    'ImmeEffect',  '0',     'Write'),
            ('2',     'w',    '01',    'InitSlaveID', '0',     'Write'),
            ('3',     'r',    '11',    'LoadData',    '1',     'Read')
        ]
        for (op_mode, r_w, exp_op_bits, exp_op_comment, exp_rw_bit, exp_rw_comment) in test_cases:
            with self.subTest(f'Operation Mode={op_mode}, R/W={r_w}'):
                result = to_statements(operation_mode(op_mode, r_w))
                expected_result = '\n'.join([
                    self._expect_writing_bits(exp_op_bits, exp_op_comment),
                    self._expect_writing_bits(exp_rw_bit, exp_rw_comment)
                ])
                self.assertEqual(result, expected_result)

    def test_operation_mode_out_of_range(self):
        with self.assertRaises(Exception) as ctx:
            operation_mode('8','r')
            self.assertIn('8', str(ctx.exception))

    def test_rw_mode_out_of_range(self):
        with self.assertRaises(Exception) as ctx:
            operation_mode('0', 'abc')
            self.assertIn('abc', str(ctx.exception))

    def test_incorrect_rw_mode(self):
        test_cases = [
            # OM, R/W
            ('1', 'r'),
            ('2', 'r'),
            ('3', 'w'),
        ]
        for (op_mode, r_w) in test_cases:
            with self.subTest(f'Mode={op_mode}, R/W={r_w}'):
                with self.assertRaises(Exception) as ctx:
                    operation_mode(op_mode, r_w)
                    self.assertIn(r_w, str(ctx.exception))

    def test_burst_length(self):
        test_cases = [
            #len, expected result
            ('0', self._expect_writing_bits('000', 'BurstLength 0')),
            ('2', self._expect_writing_bits('100', 'BurstLength 2')),
            ('3', self._expect_writing_bits('010', 'BurstLength 3')),
            ('4', self._expect_writing_bits('110', 'BurstLength 4')),
            ('5', self._expect_writing_bits('001', 'BurstLength 5')),
            ('8', self._expect_writing_bits('101', 'BurstLength 8')),
            ('16', self._expect_writing_bits('011', 'BurstLength 16')),
            ('32', self._expect_writing_bits('111', 'BurstLength 32')),
        ]
        for (len, expected_result) in test_cases:
            with self.subTest(f'Burst Length={len}'):
                result = to_statements(burst_length(len))
                self.assertEqual(result, expected_result)

    def test_burst_length_out_of_range(self):
        with self.assertRaises(Exception) as ctx:
            burst_length('6')
        self.assertIn('6', str(ctx.exception))

    def test_fast_switch_number(self):
        result = to_statements(fast_switch_number('6'))
        expected_result = self._expect_writing_bits('00110', 'FSN 6')
        self.assertEqual(result, expected_result)

    def test_addr_frame(self):
        result = to_statements(addr_frame('0xabcd'))
        expected_result = self._expect_writing_bits('01011000110110100101', 'Addr 0xabcd')
        self.maxDiff = None
        self.assertEqual(result, expected_result)

    def test_data_frame(self):
        result = to_statements(data_frame('0xab;0xcd'))
        expected_result = '\n'.join([
            self._expect_writing_bits('0110100101', 'Data 0xab'),
            self._expect_writing_bits('0101100011', 'Data 0xcd')
        ])
        self.maxDiff = None
        self.assertEqual(result, expected_result)

    def test_wait(self):
        result = to_statements(wait(3))
        expected_result = PatternVector(['1', 'X', '0', 'X', 'X'], opcode=f'repeat(3)', comment=f'Wait for 3 Timesets').get_statement()
        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
