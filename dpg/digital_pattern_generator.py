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
        body = self._generate_content_statements(config, content)
        head = ''
        tail = ''
        return '\n'.join([head, body, tail])

    def generate_digital_pattern_source_file(self, pattern_file):
        pass

    def _generate_content_statements(self, config, content):
        dpg = DigitalPatternGenerator_SPI4W(config)
        vectors = dpg.generate(content)
        return '\n'.join(v.get_statement() for v in vectors)

if __name__ == '__main__':
    pass