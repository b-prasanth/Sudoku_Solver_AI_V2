from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Helper functions to generate and solve Sudoku puzzles
def generate_new_sudoku():
    grid = [[0 for _ in range(9)] for _ in range(9)]
    fill_sudoku(grid)
    remove_random_cells(grid, 40)  # Remove 40 random cells to create a puzzle
    return grid

def fill_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if fill_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def remove_random_cells(grid, count):
    attempts = count
    while attempts > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if grid[row][col] != 0:
            grid[row][col] = 0
            attempts -= 1

def is_valid(grid, row, col, num):
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if grid[i][j] == num:
                return False
    return True

def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

@app.route('/generate', methods=['GET'])
def generate():
    puzzle = generate_new_sudoku()
    return jsonify(puzzle)

@app.route('/solve', methods=['POST'])
def solve():
    grid = request.json
    if solve_sudoku(grid):
        return jsonify(grid)
    else:
        return jsonify({"error": "Unable to solve the puzzle"}), 400

if __name__ == '__main__':
    app.run(debug=True)
