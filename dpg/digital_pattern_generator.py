import os
import csv
import json
from dpg.spi_4w.spi_4w import DigitalPatternGenerator_SPI4W

class DigitalPatternGenerator:
    def __init__(self, config_file=None, config=None, content=None):
        if config_file:
            with open(config_file) as f:
                self.config = json.load(f)
            config_file_dir = os.path.dirname(os.path.abspath(config_file))
            content_file = os.path.join(config_file_dir, self.config['content_file'])
            with open(content_file) as f:
                csv_reader = csv.DictReader(f, delimiter=',')
                self.content = [row for row in csv_reader]
        elif config:
            self.config = config
            self.content = content
        else:
            raise Exception('Config file or config/content not specified.')

    def generate_digital_pattern_source_string(self):
        head = self._generate_head(
            self.config['pattern_name'],
            self.config['timeset_name'],
            self.config['pinlist']
        )
        body = self._generate_content_statements(self.config, self.content)
        tail = '}'
        return '\n'.join([head, body, tail])

    def generate_digital_pattern_source_file(self, pattern_file):
        pass

    def _generate_content_statements(self, config, content):
        dpg = DigitalPatternGenerator_SPI4W(config)
        vectors = dpg.generate(content)
        return '\n'.join('\t' + v.get_statement() for v in vectors)

    def _generate_head(self, pattern_name, timeset_name, pinlist):
        pinlist_str = ','.join(pinlist)
        return '\n'.join([
             'file_format_version 1.0;',
            f'timeset {timeset_name};',
            f'pattern {pattern_name} ({pinlist_str})',
             '{'
        ])

if __name__ == '__main__':
    pass