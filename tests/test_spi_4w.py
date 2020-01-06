import unittest

from dpg.pattern_vector import to_statements
from dpg.spi_4w import spi_4w_vectors
from dpg.spi_4w.spi_4w import DigitalPatternGenerator_SPI4W


class Test_DigitalPatternGenerator_SPI4W(unittest.TestCase):
    def setUp(self):
        self.timeset_between_frames = 3
        self.pattern_name = 'test_dpgspi4'
        self.timeset_name = 'test_timeset'
        config = {
            'pattern_name' : self.pattern_name,
            'timeset_between_frames' : self.timeset_between_frames,
            'timeset_name' : self.timeset_name
            }
        self.dpg = DigitalPatternGenerator_SPI4W(config)

    def test_generate_ok(self):
        contents = [
            {'R/W':'W', 'Address':'0x101', 'Data':'0xcc'},
            {'R/W':'R', 'Address':'0x102'}
        ]
        result = to_statements(self.dpg.generate(contents))
        expected = to_statements(
              spi_4w_vectors.pattern_start(self.timeset_name)
            # Write 0x101 : 0xcc
            + spi_4w_vectors.frame_start()
            + spi_4w_vectors.write_cmd()
            + spi_4w_vectors.write_address('0x101')
            + spi_4w_vectors.write_data('0xcc')
            + spi_4w_vectors.frame_end()
            # Interframe wait
            + spi_4w_vectors.wait(self.timeset_between_frames)
            # Read 0x102
            + spi_4w_vectors.frame_start()
            + spi_4w_vectors.read_collect_cmd()
            + spi_4w_vectors.write_address('0x102')
            + spi_4w_vectors.write_data('0x0')
            + spi_4w_vectors.frame_end()
            + spi_4w_vectors.wait(10)
            + spi_4w_vectors.capture_start()
            + spi_4w_vectors.frame_start()
            + spi_4w_vectors.read_value_cmd()
            + spi_4w_vectors.write_address('0x0')
            + spi_4w_vectors.read_data()
            + spi_4w_vectors.capture_stop()
            + spi_4w_vectors.frame_end()
            # The end
            + spi_4w_vectors.pattern_end()
        )
        self.maxDiff = None
        self.assertEqual(result, expected)

    def test_generate_unsupported_mode(self):
        with self.assertRaises(KeyError) as ctx:
            contents = [{'R/W':'some-invalid-mode', 'Address':'0x101', 'Data':'0xcc'}]
            self.dpg.generate(contents)
        self.assertIn('some-invalid-mode', str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
