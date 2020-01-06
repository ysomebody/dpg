import csv
import json
from dpg.spi_4w.spi_4w import DigitalPatternGenerator_SPI4W

class DigitalPatternGenerator:
    def __init__(self, pattern_config_file, pattern_content_file):
        self.config_file = pattern_config_file
        self.content_file = pattern_content_file

    def generate_digital_pattern_string(self):
        with open(self.config_file) as f:
            config = json.load(f)
        with open(self.content_file) as f:
            csv_reader = csv.DictReader(f, delimiter=',')
            content = [row for row in csv_reader]
        vectors = DigitalPatternGenerator_SPI4W(config).generate(content)
        return '\n'.join(v.get_statement() for v in vectors)

    def generate_digital_pattern_source_file(self, pattern_file):
        pass

if __name__ == '__main__':
    pass