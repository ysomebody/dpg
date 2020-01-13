import unittest

from dpg.pattern_vector import to_statements
from dpg.bml import bml_vectors
from dpg.bml.digital_pattern_generator_bml import DigitalPatternGenerator_BML


class Test_DigitalPatternGenerator_BML(unittest.TestCase):
    def setUp(self):
        self.timeset_between_frames = 3
        self.pattern_name = 'test_dpgbml'
        self.timeset_name = 'test_timeset'
        config = {
            'pattern_name' : self.pattern_name,
            'timeset_between_frames' : self.timeset_between_frames,
            'timeset_name' : self.timeset_name
            }
        self.dpg = DigitalPatternGenerator_BML(config)

    def test_generate_ok(self):
        contents = [
            {'OM': '1', 'Burst Length': '2', 'FSN': '0', 'Start Address': '0x0100', 'Data': '0xFF;0xFF', 'R/W': 'W', 'ChipID': '1'},
            # {'R/W':'R', 'Address':'0x102'}
        ]
        result = to_statements(self.dpg.generate(contents))
        expected = to_statements(
              bml_vectors.sync_header()
            + bml_vectors.chip_select('1')
            + bml_vectors.operation_mode('1', 'W')
            + bml_vectors.burst_length('2')
            + bml_vectors.fast_switch_number('0')
            + bml_vectors.addr_frame('0x0100')
            + bml_vectors.data_frame('0xFF;0xFF')
        )
        self.maxDiff = None
        self.assertEqual(result, expected)

    # def test_generate_unsupported_mode(self):
    #     with self.assertRaises(KeyError) as ctx:
    #         contents = [{'R/W':'some-invalid-mode', 'Address':'0x101', 'Data':'0xcc'}]
    #         self.dpg.generate(contents)
    #     self.assertIn('some-invalid-mode', str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
