def to_statements(pattern_vector_list):
    return '\n'.join([v.get_statement() for v in pattern_vector_list])

if __name__ == "__main__":
    pass