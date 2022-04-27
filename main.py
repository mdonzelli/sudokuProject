import numpy as np
from solver import Solver
from sudokuProvider import SudokuProvider
from nnsolver import NNSolver

if __name__ == '__main__':

    sudoku_provider = SudokuProvider("sudoku.csv")
    sudoku_provider.fetch_from_file(0, 50)
    this_sudoku = sudoku_provider.get_sudoku()
    mySolver = Solver(this_sudoku[0])
    success = mySolver.solve()
    print("found solution:", success)
    # mySolver.write_log()
    print("ref solution")
    print(this_sudoku[1])
    print("solver solution")
    print(mySolver.solution)

    print("\n\n======\n")

    success_list = []

    nnsolver = NNSolver("./saved_models/cnn_model4/")
    nnsolver.pad_for_cnn = True

    # nnsolver = NNSolver("./saved_models/hiddenLayer0_epochs003_samples200k/")
    # nnsolver.pad_for_cnn = False

    for i in range(3):
        print(i)
        this_sudoku = sudoku_provider.get_sudoku()

        # modified_solution = this_sudoku[1]
        # modified_solution[1, 3] = 0
        # modified_solution[4, 6] = 0
        # modified_solution[8, 8] = 0
        # modified_solution[0, 8] = 0

        nnsolver.set_problem(this_sudoku[0])
        success = nnsolver.solve()
        success_list.append(success)

        print("solver solution")
        print(nnsolver.solution)
        print("ref solution")
        print(this_sudoku[1])

    print(sum(success_list), "/", len(success_list))
    print("bye")


