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

    def get_rows(self):
        return self.rows

    def get_columns(self):
        return self.columns

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
    while not strongly_dominated:
        new_m = column_compare(m, matrix.get_columns(), int(matrix.get_shape()[1]))


    return

def column_compare(m, columns, shape):
    temp_list = list()

    s = 0
    for i in columns:
        n = s % shape
        if len(temp_list) <= shape - 1:
            temp_list.append([int(i)])
        else:
            temp_list[n] += [int(i)]
        s += 1

    bo = temp_list[3] > temp_list[2]
    print(bo)
    return

def row_compare(self):
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

    strongly_dominated(matrix)

    print("End of Program")

filename = "./files/prog3A.txt"
do_strategy(filename)




