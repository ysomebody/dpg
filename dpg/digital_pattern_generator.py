import csv
from dpg.spi_4w.spi_4w import DigitalPatternGenerator_SPI4W

class DigitalPatternGenerator:
    def __init__(self, config_file, timeset_between_frames):
        self.config_file = config_file
        self.timeset_between_frames = timeset_between_frames

    def generate_digital_pattern_string(self):
        with open(self.config_file) as csvfile:
            configs = csv.DictReader(csvfile, delimiter=',')
            vectors = DigitalPatternGenerator_SPI4W(self.timeset_between_frames).generate(configs)
            return '\n'.join(v.get_statement() for v in vectors)

    def generate_digital_pattern_source_file(self, pattern_file):
        pass

if __name__ == '__main__':
    pass