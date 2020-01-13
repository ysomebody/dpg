from dpg.bml import bml_vectors

class DigitalPatternGenerator_BML:
    def __init__(self, pattern_config):
        self._OP_MAP = {
            'r' : self._read,
            'w' : self._write,
            'r/w' : self._read_write
        }
        self.timeset_name = pattern_config['timeset_name']
        self.timeset_between_frames = pattern_config['timeset_between_frames']

    def generate(self, pattern_content):
        vectors = []
        for row in pattern_content:
            chip_id = row['ChipID']
            op_mode = row['OM']
            r_w = row['R/W'].lower()
            burst_length = row['Burst Length']
            fsn = row['FSN']
            addr = row['Start Address']
            data = row['Data']
            # if vectors:
                # vectors += spi_4w_vectors.wait(self.timeset_between_frames)
            op = self._OP_MAP[r_w]
            vectors += op(chip_id, op_mode, r_w, burst_length, fsn, addr, data)
        return vectors

    def _write(self, chip_id, op_mode, r_w, burst_length, fsn, addr, data):
        return (self._command_frame(chip_id, op_mode, r_w, burst_length, fsn)
              + bml_vectors.addr_frame(addr)
              + bml_vectors.data_frame(data)
        )

    def _read(self, chip_id, op_mode, r_w, burst_length, fsn, addr, data):
        return (self._read_collect(chip_id, burst_length, fsn, addr)

        )

    def _read_write(self, content_row):
        raise NotImplementedError

    def _read_collect(self, chip_id, burst_length, fsn, addr):
        return (self._command_frame(chip_id, bml_vectors.BML_OM_NORMAL, 'r', burst_length, fsn)
              + bml_vectors.addr_frame(addr)
              # Wait 40 timesets until data collection complete
              + bml_vectors.wait(40)
        )

    def _read_data_value(self, chip_id, burst_length, fsn, addr):
        return (self._command_frame(chip_id, bml_vectors.BML_OM_LOAD_DATA, 'r', burst_length, fsn)
            + bml_vectors.addr_frame(addr)
            # TODO
        )

    def _command_frame(self, chip_id, op_mode, r_w, burst_length, fsn):
        return (bml_vectors.sync_header()
              + bml_vectors.chip_select(chip_id)
              + bml_vectors.operation_mode(op_mode, r_w)
              + bml_vectors.burst_length(burst_length)
              + bml_vectors.fast_switch_number(fsn)
        )

if __name__ == "__main__":
    pass
