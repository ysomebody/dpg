
def _int_str_to_bit_str(int_str, num_bits, msb_first):
    """
    Convert an integer string to num_bits bits string.
    Example:
        int_string_to_bit_str('0x5', 4) -> '0101'
        int_string_to_bit_str('0x3', 4, msb_first=false) -> '1010'
    """
    data = int(int_str, 0)  # use radix 0 to automatically deduce radix
    # convert to num_bits binary string with leading 0's
    bit_str = format(data, f'0{num_bits}b')
    return bit_str if msb_first else bit_str[::-1]


def int_to_bits_msb_first(int_str, num_bits):
    """
    Convert an integer string to num_bits bits string with most significant bit first.
    Example:
        int_str_to_bit_str_msb_first('0x3', 4) -> '0011'
    """
    return _int_str_to_bit_str(int_str, num_bits, msb_first=True)


def int_to_bits_lsb_first(int_str, num_bits):
    """
    Convert an integer string to num_bits bits string with most significant bit first.
    Example:
        int_str_to_bit_str_lsb_first('0x3', 4) -> '1100'
    """
    return _int_str_to_bit_str(int_str, num_bits, msb_first=False)

if __name__ == "__main__":
    pass
