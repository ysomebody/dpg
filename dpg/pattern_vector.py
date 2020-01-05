class PatternVector:
    def __init__(self, pinstates, comment='', opcode=''):
        self.pinstates = pinstates
        self.comment = '// ' + comment if comment != '' else ''
        self.opcode = opcode
        self.timeset = '-'

    def get_statement(self):
        return f'{self.opcode:15}\t{self.timeset:15}\t' + '\t'.join(self.pinstates) + f'; {self.comment}'

if __name__ == "__main__":
    pass