from dpg.pattern_vector import PatternVector
from dpg.utils import int_to_bits_lsb_first


def _write_bits(bits_str, comment):
    return [PatternVector(['1', 'X', bit, 'X', 'X'], comment=comment) for bit in bits_str]


def sync_header():
    return [
        PatternVector(['1', 'X', '0', 'X', 'X']),
        PatternVector(['1', 'X', '1', 'X', 'X'],
                      opcode='repeat(5)', comment='Sync header')
    ]


def chip_select(cid):
    if int(cid) < 0 or int(cid) > 31:
        raise ValueError(f"Invalid ChipID. Given {cid}; Expected: 0-31")
    bits = int_to_bits_lsb_first(cid, 5)
    bits = '0' + bits[0:4] + '0' + bits[4]
    return _write_bits(bits, comment=f'ChipID {cid}')

BML_OM_NORMAL = '0'
BML_OM_IMME_EFFECT = '1'
BML_OM_INIT_SLAVE_ID = '2'
BML_OM_LOAD_DATA = '3'

_OP_MODE_MAP = {
    #OP_MODE,              op_bits,    expected R/W,   Comment
    BML_OM_NORMAL:         ('00',      '*',            'Normal'),
    BML_OM_IMME_EFFECT:    ('10',      'w',            'ImmeEffect'),
    BML_OM_INIT_SLAVE_ID:  ('01',      'w',            'InitSlaveID'),
    BML_OM_LOAD_DATA:      ('11',      'r',            'LoadData')
}

def operation_mode(op_mode, r_w):
    try:
        op_bits, expected_r_w, comment = _OP_MODE_MAP[op_mode]
    except KeyError:
        raise ValueError(f"Invalid operation mode. Given: {op_mode}; Expected: 0-3. ")
    op_vectors = _write_bits(op_bits, comment=comment)
    if expected_r_w != '*' and r_w.lower() != expected_r_w:
        raise ValueError(f"Invalid R/W mode. Given: {r_w}; Expected: {expected_r_w}")
    return op_vectors + _rw_bit(r_w)


def _rw_bit(r_w):
    if r_w.lower() == 'w':
        return _write_bits('0', comment='Write')
    elif r_w.lower() == 'r':
        return _write_bits('1', comment='Read')
    else:
        raise ValueError(
            f"Invalid r/w mode. Given: {r_w}; Expected: r, w")

_BURST_LENGTH_MAP = {
    '0': '000',
    '2': '100',
    '3': '010',
    '4': '110',
    '5': '001',
    '8': '101',
    '16': '011',
    '32': '111'
}
def burst_length(len):
    bits = _BURST_LENGTH_MAP[len]
    return _write_bits(bits, comment=f'BurstLength {len}')


def fast_switch_number(fsn):
    bits = int_to_bits_lsb_first(fsn, 3)
    bits = '0' + bits + '0'
    return _write_bits(bits, comment=f'FSN {fsn}')


def addr_frame(addr_str):
    bits = int_to_bits_lsb_first(addr_str, 16)
    bits = '0' + bits[0:4] + '0' + bits[4:8] + '0' + bits[8:12] + '0' + bits[12:16]
    return _write_bits(bits, comment=f'Addr {addr_str}')


def data_frame(data_str):
    vectors = []
    data = data_str.split(';')
    for d in data:
        bits = int_to_bits_lsb_first(d, 8)
        bits = '0' + bits[0:4] + '0' + bits[4:8]
        vectors += _write_bits(bits, comment=f'Data {d}')
    return vectors


def wait(num_timesets):
    return [PatternVector(['1', 'X', '0', 'X', 'X'], opcode=f'repeat({num_timesets})', comment=f'Wait for {num_timesets} Timesets')]

if __name__ == "__main__":
    pass
