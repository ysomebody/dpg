import unittest
from dpg.pattern_vector import PatternVector

class Test_PatternVector(unittest.TestCase):
    def test_get_statement(self):
        vector_statement = PatternVector(['1', 'X'], 'this is comment', 'opcode').get_statement()
        expected_statement = 'opcode         	-              	1	X; // this is comment'
        self.assertEqual(vector_statement, expected_statement)

if __name__ == '__main__':
    unittest.main()