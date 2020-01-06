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

    def generate(self, configs):
        vectors = spi_4w_vectors.pattern_start(self.timeset_name)
        for config in configs:
            op = self.op_map[config['R/W']]
            vectors += spi_4w_vectors.wait(self.timeset_between_frames)
            vectors += op(config)
        vectors += spi_4w_vectors.pattern_end()
        return vectors


    def _write(self, config):
        return (
              spi_4w_vectors.frame_start()
            + spi_4w_vectors.write_cmd()
            + spi_4w_vectors.write_address(config['Address'])
            + spi_4w_vectors.write_data(config['Data'])
            + spi_4w_vectors.frame_end()
        )

    def _read(self, config):
        return (
              self._read_collect(config)
            + spi_4w_vectors.wait(10)
            + self._read_capture(config)
        )

    def _read_write(self, config):
        raise NotImplementedError

    def _read_collect(self, config):
        return (
              spi_4w_vectors.frame_start()
            + spi_4w_vectors.read_collect_cmd()
            + spi_4w_vectors.write_address(config['Address'])
            + spi_4w_vectors.write_data('0x0')
            + spi_4w_vectors.frame_end()
        )
        
    def _read_capture(self, config):
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
    with open(r'testdata\spi_4w.csv') as csvfile:
        configs = csv.DictReader(csvfile, delimiter=',')
        vectors = DigitalPatternGenerator_SPI4W(3).generate(configs)
        print('\n'.join(v.get_statement() for v in vectors))
   