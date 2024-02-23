"""
    Program 3
    Professor: Dr. Vicki Allan
    Author: Paul Semadeni
    Date: February 16, 2024
"""
import pandas as pd

class Matrix:
    def __init__(self, shape, rows, columns):
        self.shape = shape
        self.rows = rows
        self.columns = columns

    def get_shape(self):
        return self.shape

    def set_shape(self, shape):
        self.shape = shape
        return

    def get_rows(self):
        return self.rows

    def set_rows(self, rows):
        self.rows = rows
        return

    def get_columns(self):
        return self.columns

    def set_columns(self, columns):
        self.columns = columns
        return

    def create_matrix(self):
        pairs = list()
        for i in range(len(self.rows)):
            p = [self.rows[i], self.columns[i]]
            pairs.append(p)

        shape = self.get_shape()
        matrix = list()
        temp_list = list()
        i = 1
        for pair in pairs:
            temp_list.append(pair)
            if i % int(shape[1]) == 0:
                matrix.append(temp_list)
                temp_list = []
            i += 1
        return matrix

def dominated(matrix, strategy):
    m = matrix.create_matrix()
    dominated = False
    col_cont = True
    row_cont = True
    i = 0
    while not dominated and i < 10:
        if int(matrix.get_shape()[1]) > 1:
            m, col_cont = column_compare(m, matrix, strategy)
        if int(matrix.get_shape()[0]) > 1:
            m, row_cont = row_compare(m, matrix, strategy)
        if not col_cont or not row_cont:
            dominated = True
        i += 1
    print(f"{ strategy } strategy: ", m)
    return

def column_compare(m, matrix, strategy):
    columns = matrix.get_columns()
    # Function can handle rows and columns
    shape = int(matrix.get_shape()[1])
    temp_list = list()
    # Create column list
    s = 0
    for i in columns:
        n = s % shape
        if len(temp_list) < shape:
            temp_list.append([int(i)])
        else:
            temp_list[n] += [int(i)]
        s += 1
    m, cont = update_matrix(m, matrix, temp_list, shape, "column", strategy)
    return m, cont

def row_compare(m, matrix, strategy):
    rows = matrix.get_rows()
    # Function can handle rows and columns
    shape = int(matrix.get_shape()[0])
    num_cols = int(matrix.get_shape()[1])
    temp_list = list()
    # Create column list
    s = 0
    n = 0
    for i in rows:
        # c = s % num_cols
        if s == 0:
            temp_list.append([int(i)])
        elif s == num_cols:
            temp_list.append([int(i)])
            n += 1
        else:
            temp_list[n] += [int(i)]
        s += 1
    m, cont = update_matrix(m, matrix, temp_list, shape, "row", strategy)
    return m, cont

def update_matrix(m, matrix, temp_list, shape, what, strategy):
    cont = True
    columns = matrix.get_columns()
    rows = matrix.get_rows()
    # Keep track of largest column value
    largest_val = temp_list[0]
    position = 0
    remove_position = list()
    keep_position = list()
    p = 0
    for i in temp_list:
        bigger_val = list()
        for j in range(len(i)):
            if i[j] >= largest_val[j]:
                bigger_val.append(True)
            # elif i[j] >= largest_val[j] and strategy == "strongly dominated":
            else:
                bigger_val.append(False)
        if False in bigger_val and strategy == "strongly dominated":
            remove_position.append(p)
        elif True not in bigger_val and strategy == "weakly dominated":
            remove_position.append(p)
        elif False not in bigger_val:
            largest_val = i
            position = p
            # if strategy == "strongly dominated":
            keep_position.append(p)
        else:
            keep_position.append(p)
        p += 1
    keep_position.insert(0, position)
    remove_position += keep_position
    # Remove item from position
    if position != remove_position[0]:
        if what == "column":
            for row in m:
                row.pop(remove_position[0])
        else:
            m.pop(remove_position[0])
        # Update the rows and columns in the matrix object (the shape is being updated)
        for i in range(len(columns)):
            if remove_position[0] == (i - 1) % shape:
                columns.pop(i - 1)
                rows.pop(i - 1)
        matrix.set_columns(columns)
        matrix.set_rows(rows)
        matrix.set_shape([len(m), len(m[0])])
    else:
        cont = False

    return m, cont

def pareto_optimal(matrix):
    m = matrix.create_matrix()
    column_large_nums = [[],[]]
    i = 0
    while i < int(matrix.get_shape()[1]):
        one = m[0]
        two = m[1]
        if one[i][1] > two[i][1]:
            column_large_nums[0].append(i)
        else:
            column_large_nums[1].append(i)
        i += 1

    row_large_nums = list()
    i = 0
    for row in m:
        large_num = 0
        row_large_nums.append([])
        j = 0
        for col in row:
            if int(col[0]) > large_num:
                row_large_nums[i].clear()
                row_large_nums[i].append(j)
                large_num = int(col[0])
            elif int(col[0]) == large_num:
                row_large_nums[i].append(j)
            j += 1
        i += 1

    pareto_optimal = [[],[]]
    i = 0
    for row in column_large_nums:
        for col in row:
            if col in row_large_nums[i]:
                pareto_optimal[i].append(m[i][col])
        i += 1
    print("pareto optimal: ", pareto_optimal)
    return

def maximin(matrix):
    m = matrix.create_matrix()
    column_large_nums = list()
    i = 0
    for row in m:
        large_num = 0
        column_large_nums.append([])
        j = 0
        for col in row:
            if int(col[1]) > large_num:
                column_large_nums[i].clear()
                column_large_nums[i].append(int(col[1]))
                large_num = int(col[1])
            j += 1
        i += 1
    row_large_nums = []
    i = 0
    while i < int(matrix.get_shape()[1]):
        one = m[0]
        two = m[1]
        if one[i][0] > two[i][0]:
            row_large_nums.append(int(one[i][0]))
        else:
            row_large_nums.append(int(two[i][0]))
        i += 1
    maximin = []
    small_col = column_large_nums[0][0]
    i = 0
    for row in column_large_nums:
        for col in row:
            if col <= small_col:
                maximin.append(i)
        i += 1
    small_row = row_large_nums.index(min(row_large_nums))
    maximin.append(small_row)
    print("maximin: ", m[maximin[0]][maximin[1]])
    return

def minimax(matrix):
    m = matrix.create_matrix()
    column_small_nums = list()
    i = 0
    for row in m:
        small_num = 0
        column_small_nums.append([])
        j = 0
        for col in row:
            if int(col[1]) <= small_num:
                column_small_nums[i].clear()
                column_small_nums[i].append(int(col[1]))
                small_num = int(col[1])
            j += 1
        i += 1
    row_small_nums = []
    i = 0
    while i < int(matrix.get_shape()[1]):
        one = m[0]
        two = m[1]
        if one[i][0] < two[i][0]:
            row_small_nums.append(int(one[i][0]))
        else:
            row_small_nums.append(int(two[i][0]))
        i += 1
    minimax = []
    small_col = column_small_nums[0][0]
    i = 0
    for row in column_small_nums:
        for col in row:
            if col >= small_col:
                minimax.clear()
                minimax.append(i)
        i += 1
    small_row = row_small_nums.index(max(row_small_nums))
    minimax.append(small_row)
    print("minimax: ", m[minimax[0]][minimax[1]])
    return

def read_file(filename):
    shape = list()
    rows = list()
    columns = list()
    with open(filename, "r") as file:
        s = 0
        for i in file:
            i = i.strip().split(" ")
            if s == 0:
                shape += i
            elif s == 1:
                rows += i
            elif s == 2:
                columns += i
            else:
                print("Out of range")
            s += 1
        matrix = Matrix(shape, rows, columns)
    return matrix

def do_strategy(filename):
    matrix = read_file(filename)
    dominated(matrix, "strongly dominated")
    matrix = read_file(filename)
    dominated(matrix, "weakly dominated")
    matrix = read_file(filename)
    pareto_optimal(matrix)
    matrix = read_file(filename)
    maximin(matrix)
    matrix = read_file(filename)
    minimax(matrix)

    print("End of Program")

filename = "./files/prog3A.txt"
do_strategy(filename)




