import numpy as np
from solver import Solver
from sudokuProvider import SudokuProvider
from nnsolver import NNSolver

if __name__ == '__main__':

    sudoku_provider = SudokuProvider("sudoku.csv")
    sudoku_provider.fetch_from_file(0, 10)
    this_sudoku = sudoku_provider.get_sudoku()
    print(type(this_sudoku))
    this_sudoku = sudoku_provider.get_sudoku()
    print(this_sudoku)
    mySolver = Solver(this_sudoku[0])
    success = mySolver.solve()
    print("fund solution:", success)
    # mySolver.write_log()
    print("ref solution", this_sudoku[1])
    print("solver solution", mySolver.solution())

    print("======")

    sudoku_provider.fetch_from_file(11000, 12000)

    success_list = []

    # nnsolver = NNSolver("./saved_models/hiddenLayer0_epochs003_samples200k/")
    nnsolver = NNSolver("./saved_models/testModel/")
    # nnsolver = NNSolver("./saved_models/basicModel/")
    for i in range(10):
        print(i)
        this_sudoku = sudoku_provider.get_sudoku()

        modified_solution = this_sudoku[1]
        modified_solution[1, 3] = 0
        modified_solution[4, 6] = 0
        modified_solution[8, 8] = 0
        modified_solution[0, 8] = 0

        nnsolver.set_problem(modified_solution)
        success = nnsolver.solve()
        success_list.append(success)

    print(sum(success_list), "/", len(success_list))




    print("bye")


