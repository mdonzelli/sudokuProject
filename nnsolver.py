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
        while not evaluate(current_solution.reshape(9, 9), True):
            mutable_mask = (current_solution == 0)

            one_hot_problem_flat = NNSolver.to_one_hot(current_solution)

            prediction = self._model.predict(one_hot_problem_flat.reshape(1, *one_hot_problem_flat.shape))
            max_prob = 0.
            max_idx = None
            for i, entry in enumerate(prediction):
                if mutable_mask[i]:
                    local_max = np.amax(entry)
                    if local_max > max_prob:
                        max_prob = local_max
                        max_idx = i

            current_solution[max_idx] = np.argmax(prediction[max_idx])
            self._solution = current_solution.reshape(9, 9)
            if not evaluate(current_solution.reshape(9, 9), False):
                return False
        return True


    @staticmethod
    def to_one_hot(sudoku):

        sudoku_flat = sudoku.reshape(81, 1)
        one_hot_encoder = OneHotEncoder(sparse=False)
        one_hot_flat = one_hot_encoder.fit_transform(sudoku_flat)
        return one_hot_flat
