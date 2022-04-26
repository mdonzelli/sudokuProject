import numpy as np


def evaluate(matrix, final=False):
    assert(isinstance(matrix, np.ndarray))

    if not evaluate_rows(matrix, final):
        return False
    if not evaluate_cols(matrix, final):
        return False
    if not evaluate_blocks(matrix, final):
        return False
    return True


def evaluate_rows(matrix, final=False):
    for i in range(9):
        if not evaluate_section(matrix[i, :], final):
            return False
    return True


def evaluate_cols(matrix, final=False):
    for i in range(9):
        if not evaluate_section(matrix[:, i], final):
            return False
    return True


def evaluate_blocks(matrix, final=False):
    for i in [0, 3, 6]:
        for j in [0, 3, 6]:
            if not evaluate_section(matrix[i:i+3, j:j+3], final):
                return False
    return True


def evaluate_section(section, final=False):
    if final:
        for i in range(1, 10):
            if count_occurrences(section, i) != 1:
                return False
    else:
        for i in range(1, 10):
            if count_occurrences(section, i) > 1:
                return False
    return True


def count_occurrences(array, value):
    return (array == value).sum()



