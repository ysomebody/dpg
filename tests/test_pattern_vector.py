import unittest
from dpg.pattern_vector import PatternVector, to_statements

class Test_PatternVector(unittest.TestCase):
    def test_get_statement(self):
        vector = PatternVector(['1', 'X'], 'this is comment', 'opcode')
        expected_statement = 'opcode         	-              	1	X; // this is comment'
        self.assertEqual(vector.get_statement(), expected_statement)

    def test_to_statements(self):
        vectors = [
            PatternVector(['1', 'X'], 'this is a comment', 'opcode1'),
            PatternVector(['V', '0'], 'another comment', 'opcode2'),
        ]
        expected_statement = '\n'.join([
            'opcode1        	-              	1	X; // this is a comment',
            'opcode2        	-              	V	0; // another comment'
        ])
        self.assertEqual(to_statements(vectors), expected_statement)

if __name__ == '__main__':
    unittest.main()