import csv
from dpg.spi_4w import spi_4w_vectors

class DigitalPatternGenerator_SPI4W:
    def __init__(self, pattern_config):
        self.op_map = {
            'R' : self._read,
            'W' : self._write,
            'R/W' : self._read_write
        }
        self.timeset_name = pattern_config['timeset_name']
        self.timeset_between_frames = pattern_config['timeset_between_frames']

    def generate(self, pattern_content):
        vectors = []
        for row in pattern_content:
            if vectors:
                vectors += spi_4w_vectors.wait(self.timeset_between_frames)
            op = self.op_map[row['R/W']]
            vectors += op(row)
        return (
              spi_4w_vectors.pattern_start(self.timeset_name)
            + vectors
            + spi_4w_vectors.pattern_end()
        )

    def _write(self, content_row):
        return (
              spi_4w_vectors.frame_start()
            + spi_4w_vectors.write_cmd()
            + spi_4w_vectors.write_address(content_row['Address'])
            + spi_4w_vectors.write_data(content_row['Data'])
            + spi_4w_vectors.frame_end()
        )

    def _read(self, content_row):
        return (
              self._read_collect(content_row)
            + spi_4w_vectors.wait(10)
            + self._read_capture()
        )

    def _read_write(self, content_row):
        raise NotImplementedError

    def _read_collect(self, content_row):
        return (
              spi_4w_vectors.frame_start()
            + spi_4w_vectors.read_collect_cmd()
            + spi_4w_vectors.write_address(content_row['Address'])
            + spi_4w_vectors.write_data('0x0')
            + spi_4w_vectors.frame_end()
        )
        
    def _read_capture(self):
        return (
              spi_4w_vectors.capture_start()
            + spi_4w_vectors.frame_start()
            + spi_4w_vectors.read_value_cmd()
            + spi_4w_vectors.write_address('0x0')
            + spi_4w_vectors.read_data()
            + spi_4w_vectors.capture_stop()
            + spi_4w_vectors.frame_end()
        )

if __name__ == "__main__":
    pass
