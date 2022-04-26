import pandas as pd
import numpy as np
import csv


class SudokuProvider:

    def __init__(self, filename):
        self._filename = filename
        self._problems = []
        self._solutions = []
        self._index = 0

    def fetch_from_file(self, idx_low, n_rows):
        self._problems = []
        self._solutions = []
        self._index = 0
        csv_df = pd.read_csv(self._filename, skiprows=1+idx_low, nrows=n_rows, header=None)
        problems = csv_df[0].to_list()
        solutions = csv_df[1].to_list()

        for entry in problems:
            self._problems.append(np.array([char for char in entry], dtype=np.int8).reshape((9, 9)))
        for entry in solutions:
            self._solutions.append(np.array([char for char in entry], dtype=np.int8).reshape((9, 9)))

    def get_sudoku(self):
        return_value = (self._problems[self._index], self._solutions[self._index])
        if self._index >= len(self._problems)-1:
            self._index = 0
        else:
            self._index += 1
        return return_value

    def get_all(self):
        return self._problems, self._solutions

    def count_lines_in_file(self):
        num_rows = 0
        for row in open(self._filename):
            num_rows += 1
        return num_rows


