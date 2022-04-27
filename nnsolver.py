import numpy as np
import tensorflow as tf
from sklearn.preprocessing import OneHotEncoder
import time

from evaluator import evaluate


class NNSolver:
    def __init__(self, model_path):
        self._model = tf.keras.models.load_model(model_path)
        self._initial_matrix = None
        self._solution = None
        self._pad_for_cnn = False

    @property
    def solution(self):
        return self._solution

    def set_problem(self, matrix):
        self._initial_matrix = matrix.copy()
        self._solution = np.zeros((9, 9), dtype=np.uint8)

    def solve(self):
        start = time.perf_counter()
        success = self._solve_internal()
        end = time.perf_counter()
        print("solving took", end - start, "s")
        print("solving was", "successful" if success else "not successful")
        return success

    def _solve_internal(self):
        if not evaluate(self._initial_matrix, False):
            return False

        current_solution = self._initial_matrix.flatten()
        counter = 0
        while not evaluate(current_solution.reshape(9, 9), True):
            print(counter, " ", end="")
            counter += 1
            mutable_mask = (current_solution == 0)

            if self._pad_for_cnn:
                one_hot_problem = NNSolver.to_one_hot(NNSolver.pad_matrix(current_solution.reshape(9, 9)))
                print("shape", one_hot_problem.shape)
            else:
                one_hot_problem = NNSolver.to_one_hot(current_solution).reshape(81, 10)

            prediction = self._model.predict(one_hot_problem.reshape(1, *one_hot_problem.shape))
            max_prob = 0.
            max_idx = None
            for i, entry in enumerate(prediction):
                if mutable_mask[i]:
                    local_max = np.amax(entry)
                    # do not accept max probability if this points to zero
                    if local_max > max_prob and np.argmax(prediction[i]) != 0:
                        max_prob = local_max
                        max_idx = i

            # no suitable prediction other than zero has been found
            if max_idx is None:
                print("no suitable prediction other than zero has been found")
                return False

            current_solution[max_idx] = np.argmax(prediction[max_idx])
            self._solution = current_solution.reshape(9, 9)
            if not evaluate(current_solution.reshape(9, 9), False):
                return False
        return True

    @property
    def pad_for_cnn(self):
        return self._pad_for_cnn

    @pad_for_cnn.setter
    def pad_for_cnn(self, value):
        self._pad_for_cnn = value

    @staticmethod
    def to_one_hot(sudoku):
        shape = sudoku.shape
        sudoku_flat = sudoku.reshape((sudoku.flatten().shape[0], 1))
        one_hot_encoder = OneHotEncoder(sparse=False)
        one_hot = one_hot_encoder.fit_transform(sudoku_flat)
        return one_hot.reshape(list(shape) + [10])

    @staticmethod
    def pad_matrix(matrix):
        output = np.concatenate((matrix, matrix, matrix), axis=0)
        output = np.concatenate((output, output, output), axis=1)
        return output[5:-5, 5:-5]