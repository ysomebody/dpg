import os
script_dir = os.path.dirname(os.path.abspath(__file__))

try:
    import dpg
except ImportError:
    # In case the package is not installed, search the parent folder for
    # the package.
    import sys
    parent_dir = os.path.dirname(script_dir)
    sys.path.append(parent_dir)

from dpg.digital_pattern_generator import DigitalPatternGenerator

if __name__ == '__main__':
    config_file = os.path.join(script_dir, 'config_spi_4w.csv')
    pattern_file = os.path.join(script_dir, 'pattern_spi_4w.digipatsrc')
    dpg = DigitalPatternGenerator(config_file, pattern_file, 5)
    print(dpg.generate_digital_pattern_src())
