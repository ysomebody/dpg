from dpg.pattern_vector import PatternVector
from dpg.utils import int_str_to_bit_str

def pattern_start(timeset_name):
    return [PatternVector(['1', '0', 'X', '0'], comment='Start of the pattern', timeset=timeset_name)]

def pattern_end():
    return [PatternVector(['X', 'X', 'X', 'X'], comment='End of the pattern', opcode='halt')]

def frame_start():
    return [PatternVector(['1', '0', 'X', '0'], comment='Start of SPI 4W Frame', opcode='repeat(5)')]

def frame_end():
    return [PatternVector(['1', '0', 'X', '0'], comment='End of SPI 4W Frame', opcode='repeat(5)')]

def wait(num_timeset):
    return [PatternVector(['1', '0', 'X', '0'], comment=f'Wait for {num_timeset} Timeset', opcode=f'repeat({num_timeset})')]

def capture_start():
    return [PatternVector(['1', '0', 'X', '0'], opcode='capture_start(DATA_Read)')]

def capture_stop():
    return [PatternVector(['1', '0', 'X', '1'], opcode='capture_stop')]

def _write_bits(bits_str, comment):
    return [PatternVector(['0', bit, 'X', '1'], comment=comment) for bit in bits_str]

def write_cmd():
    return _write_bits('01000', 'Write Command')

def read_collect_cmd():
    return _write_bits('01010', 'Read Collect Command')

def read_value_cmd():
    return _write_bits('01000', 'Read Value Command')

def write_address(addr_str):
    # Address is 11 bits
    return _write_bits(int_str_to_bit_str(addr_str, 11), comment=f'Address {addr_str}')

def write_data(data_str):
    # Data is 16 bits
    return _write_bits(int_str_to_bit_str(data_str, 16), comment=f'Data {data_str}')

def read_data():
    # capture 16 bits of data
    return [PatternVector(['0', 'X', 'V', '1'], comment='Read', opcode='capture')] * 16


if __name__ == "__main__":
    pass