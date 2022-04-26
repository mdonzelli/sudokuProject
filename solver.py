import numpy as np

from evaluator import evaluate


class Solver:
    def __init__(self, matrix):
        self._initial_matrix = matrix.copy()
        self._solution = np.zeros((9, 9), dtype=np.uint8)
        self._mutable_mask = self._initial_matrix == 0
        self._log = []
        self._activate_log = False

        self._i = 0
        self._j = 0

    def solution(self):
        return self._solution

    def solve(self):
        if not evaluate(self._initial_matrix, False):
            return False

        self._solution = self._initial_matrix.copy()

        self._i = 0
        self._j = 0

        if not self._mutable_mask[self._i, self._j]:
            success = self.advance_to_allowed_idx()
            if not success:
                return True
        counter = 0
        while True:
            if self.activate_log:
                self._log.append(self._solution.copy())
            counter += 1
            if counter % 1000 == 0:
                print(counter, self._i, self._j)
            if self._solution[self._i, self._j] < 9:
                self._solution[self._i, self._j] += 1
                if evaluate(self._solution, False):
                    success = self.advance_to_allowed_idx()
                    if not success:
                        return True
                else:
                    pass # continue
            else:
                self._solution[self._i, self._j] = 0
                success = self.revert_to_allowed_idx()
                if not success:
                    return False

    def advance_idx(self):
        if self._j == 8:
            self._j = 0
            self._i += 1
        else:
            self._j +=1

    def advance_to_allowed_idx(self):
        while True:
            self.advance_idx()
            if self._i > 8:
                return False
            if self._mutable_mask[self._i, self._j]:
                break
        return True

    def revert_idx(self):
        if self._j == 0:
            self._j = 8
            self._i -= 1
        else:
            self._j -=1

    def revert_to_allowed_idx(self):
        while True:
            self.revert_idx()
            if self._i < 0:
                return False
            if self._mutable_mask[self._i, self._j]:
                break
        return True

    def write_log(self):
        outfile = open("log.txt", "w")
        for entry in self._log:
            for number in entry.flatten():
                outfile.write(str(number))
            outfile.write("\n")
        outfile.close()

    @property
    def activate_log(self):
        return self._activate_log

    @activate_log.setter
    def activate_log(self, value):
        self._activate_log = value
