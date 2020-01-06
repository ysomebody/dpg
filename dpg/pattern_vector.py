class PatternVector:
    def __init__(self, pinstates, comment='', opcode='', timeset='-'):
        self.pinstates = pinstates
        self.comment = (' // ' + comment) if comment != '' else ''
        self.opcode = opcode
        self.timeset = timeset

    def get_statement(self):
        return f'{self.opcode:15}\t{self.timeset:15}\t' + '\t'.join(self.pinstates) + f';{self.comment}'

def to_statements(pattern_vector_list):
    return '\n'.join([v.get_statement() for v in pattern_vector_list])

if __name__ == "__main__":
    pass