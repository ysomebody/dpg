from ..pattern_vector import PatternVector

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

def write_bits(bits_str, comment):
    return [PatternVector(['0', bit, 'X', '1'], comment=comment) for bit in bits_str]

def write_cmd():
    return write_bits('01000', 'Write Command')

def read_collect_cmd():
    return write_bits('01010', 'Read Collect Command')

def read_value_cmd():
    return write_bits('01000', 'Read Value Command')

def write_address(addr_str):
    return _write_hex(addr_str, 11, 'Address') #address is 11 bits

def write_data(data_str):
    return _write_hex(data_str, 16, 'Data') #data is 16 bits

def _write_hex(hex_str, num_bits, comment_prefix):
    comment = f'{comment_prefix} {hex_str}'
    data = int(hex_str, 0) # use radix 0 to parse '0x'
    bin_str = format(data, f'0{num_bits}b') # convert to num_bits binary string with leading 0's
    return write_bits(bin_str, comment)

def read_data():
    return [PatternVector(['0', 'X', 'V', '1'], comment='Read', opcode='capture')] * 16 # capture 16 bits of data


if __name__ == "__main__":
    pass