import unittest
from dpg.digital_pattern_generator import DigitalPatternGenerator

test_config = {
    'protocol': 'SPI_4W',
    'pattern_name': 'Test_Pattern',
    'timeset_name': 'Timeset_Test',
    'pinlist': ['PinA', 'PinB'],
    'content_file': 'test_content.csv'
}

test_content = [
    {'Address':'0x101', 'Data':'0xcc'},
    {'Address':'0x102', 'Data':'0x0'}
]

class Test_DigitalPatternGenerator_Constructor(unittest.TestCase):
    def test_init_from_file(self):
        dpg = DigitalPatternGenerator(config_file = r'tests\test_config.json')
        self.assertEqual(dpg.config, test_config)
        self.assertEqual(dpg.content, test_content)

    def test_init_from_arguments(self):
        dpg = DigitalPatternGenerator(config=test_config, content=test_content)
        self.assertEqual(dpg.config, test_config)
        self.assertEqual(dpg.content, test_content)

    def test_init_fail(self):
        with self.assertRaises(Exception) as ctx:
            _ = DigitalPatternGenerator()
        self.assertIn('not specified', str(ctx.exception))

class Test_DigitalPatternGenerator(unittest.TestCase):
    def setUp(self):
        test_content = [
            {'Address':'0x101', 'Data':'0xcc', 'R/W':'W'},
            {'Address':'0x102', 'Data':'0x0', 'R/W':'R'}
        ]
        self.dpg = DigitalPatternGenerator(config=test_config, content=test_content)

    def test_generate_digital_pattern_source_string(self):
        pass
        #srcstr = self.dpg.generate_digital_pattern_source_string()
        #print(srcstr)
        # TODO: Change to a mock generator

if __name__ == '__main__':
    unittest.main()