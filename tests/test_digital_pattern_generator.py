import unittest
from dpg.digital_pattern_generator import DigitalPatternGenerator

test_config = {
    'protocol': 'Test_Protocol',
    'pattern_name': 'Test_Pattern',
    'timeset_name': 'Timeset_Test',
    'pinlist': ['R_W', 'Data_In', 'Data_Out'],
    'content_file': 'test_content.csv'
}

test_content = [
    {'Command':'write', 'Address':'0x01', 'Data':'0xcc'},
    {'Command':'read',  'Address':'0x10', 'Data':''    }
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
        self.dpg = DigitalPatternGenerator(config=test_config, content=test_content)

    def test_generate_digital_pattern_source_string(self):
        src = self.dpg.generate_digital_pattern_source_string()
        expected_src = \
"""file_format_version 1.0;
timeset Timeset_Test;
pattern Test_Pattern (R_W,Data_In,Data_Out)
{
	               	Timeset_Test   	0	X	X; // Pattern Start
	               	-              	1	1	X; // Write 0xcc (bit 0)
	               	-              	1	1	X; // Write 0xcc (bit 1)
	               	-              	1	0	X; // Write 0xcc (bit 2)
	               	-              	1	0	X; // Write 0xcc (bit 3)
	               	-              	1	1	X; // Write 0xcc (bit 4)
	               	-              	1	1	X; // Write 0xcc (bit 5)
	               	-              	1	0	X; // Write 0xcc (bit 6)
	               	-              	1	0	X; // Write 0xcc (bit 7)
	capture_start(DATA_Read)	-              	0	X	X;
	capture        	-              	0	X	V; // Read
	capture        	-              	0	X	V; // Read
	capture        	-              	0	X	V; // Read
	capture        	-              	0	X	V; // Read
	capture        	-              	0	X	V; // Read
	capture        	-              	0	X	V; // Read
	capture        	-              	0	X	V; // Read
	capture        	-              	0	X	V; // Read
	capture_stop   	-              	0	X	X;
	halt           	-              	0	X	X; // Pattern End
}"""
        self.maxDiff = None
        self.assertEqual(src, expected_src)
        # TODO: Change to a mock generator

if __name__ == '__main__':
    unittest.main()