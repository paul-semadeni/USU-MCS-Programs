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

def strongly_dominated(matrix):
    m = matrix.create_matrix()
    strongly_dominated = False
    i = 0
    while not strongly_dominated and i < 10:
        if int(matrix.get_shape()[1]) > 1:
            m = column_compare(m, matrix)
        if int(matrix.get_shape()[0]) > 1:
            m = row_compare(m, matrix)
        if len(m) == 1 and len(m[0]) == 1:
            strongly_dominated = True
        i += 1
    print("Strongly dominated strategy: ", m)
    return m

def column_compare(m, matrix):
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
    m = update_matrix(m, matrix, temp_list, shape, "column")
    return m

def row_compare(m, matrix):
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
    m = update_matrix(m, matrix, temp_list, shape, "row")
    return m

def update_matrix(m, matrix, temp_list, shape, what):
    columns = matrix.get_columns()
    rows = matrix.get_rows()
    # Keep track of largest column value
    largest_val = temp_list[0]
    position = 0
    remove_position = list()
    p = 0
    for i in temp_list:
        bigger_val = list()
        for j in range(len(i)):
            if i[j] >= largest_val[j]:
                bigger_val.append(True)
            elif i[j] <= largest_val[j]:
                bigger_val.append(False)
        if False in bigger_val:
            remove_position.append(p)
        else:
            largest_val = i
            position = p
        p += 1
    remove_position.append(position)
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
    # else:
    #     print("Cannot remove last position")
    return m

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

    strongly_dominated(matrix)

    print("End of Program")

filename = "./files/prog3A.txt"
do_strategy(filename)




