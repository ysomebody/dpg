from dpg.pattern_vector import PatternVector
from dpg.utils import int_str_to_bit_str

# A mock up protocol for testing
# Pins: R_W, Data_In, Data_Out
# Data_In drives 8 bits of data when R_W is 1
# Data_Out reads 8 bits of data when R_W is 0

class DigitalPatternGenerator_Test_Protocol:
    def __init__(self, pattern_config):
        self.timeset_name = pattern_config['timeset_name']

    def generate(self, pattern_content):
        vectors = [PatternVector(['0', 'X', 'X'], comment='Pattern Start', timeset=self.timeset_name)]
        for row in pattern_content:
            cmd = row['Command'].lower()
            if cmd == 'write':
                vectors += self._write(row['Data'])
            elif cmd == 'read':
                vectors += self._read()
            else:
                raise Exception(f"Invalid command {cmd}")
        vectors += [PatternVector(['0', 'X', 'X'], comment='Pattern End', opcode='halt')]
        return vectors

    def _write(self, data):
        bit_str = int_str_to_bit_str(data, 8)
        vectors = []
        for i in range(0, 8):
            vectors.append(PatternVector(['1', bit_str[i], 'X'], comment=f'Write {data} (bit {i})'))
        return vectors

    def _read(self):
        return ([PatternVector(['0', 'X', 'X'], opcode='capture_start(DATA_Read)')]
              # reading 8 bits
              + [PatternVector(['0', 'X', 'V'], comment='Read', opcode='capture')] * 8
              + [PatternVector(['0', 'X', 'X'], opcode='capture_stop')]
        )

if __name__ == "__main__":
    pass
