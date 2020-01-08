def int_str_to_bit_str(hex_str, num_bits):
    data = int(hex_str, 0) # use radix 0 to automatically deduce radix
    return format(data, f'0{num_bits}b') # convert to num_bits binary string with leading 0's

if __name__ == "__main__":
    pass