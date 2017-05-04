#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 5, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738

del_cost = 1
ins_cost = 1
sub_cost = 1


def get_edit_distance(list_source, list_target):
    n = len(list_source)
    m = len(list_target)

    # Initialize zeroth row/colum as distance from empty string
    dist_matrix = [[MatrixEntry() for x in range(m + 1)] for y in range(n + 1)]

    for row in range(1, n + 1):
        dist_matrix[row][0].set_init_value(dist_matrix[row - 1][0].value + del_cost)
    for col in range(1, m + 1):
        dist_matrix[0][col].set_init_value(dist_matrix[0][col - 1].value + ins_cost)

    # Recurrence relation
    for row in range(1, n + 1):
        for col in range(1, m + 1):
            del_val = dist_matrix[row - 1][col].value + del_cost
            sub_val = dist_matrix[row - 1][col - 1].value + get_sub_cost(list_source[row - 1], list_target[col - 1])
            ins_val = dist_matrix[row][col - 1].value + ins_cost

            dist_matrix[row][col].set_value(del_val, sub_val, ins_val)

    print_output(list_source, list_target, dist_matrix, n, m)


def get_sub_cost(token_source, token_target):
    if token_source == token_target:
        return 0
    else:
        return sub_cost


def backtrace(dist_matrix, n, m):
    operations = []
    curr_row = n
    curr_col = m
    curr_value = dist_matrix[n][m].value

    while True:
        if curr_row == 0 and curr_col == 0:
            break

        if dist_matrix[curr_row][curr_col].diagonal_arrow:
            curr_row -= 1
            curr_col -= 1
            if curr_value > dist_matrix[curr_row][curr_col].value:
                operations.insert(0, 'S')
                curr_value = dist_matrix[curr_row][curr_col].value
            else:
                operations.insert(0, '')
        elif dist_matrix[curr_row][curr_col].top_arrow\
                or (curr_row != 0 and curr_col == 0):
            curr_row -= 1
            operations.insert(0, 'D')
            curr_value = dist_matrix[curr_row][curr_col].value

        elif dist_matrix[curr_row][curr_col].left_arrow\
                or (curr_row == 0 and curr_col != 0):
            curr_col -= 1
            operations.insert(0, 'I')
            curr_value = dist_matrix[curr_row][curr_col].value
    return operations


def print_output(list_source, list_target, dist_matrix, n, m):
    # print_matrix(dist_matrix, n, m)

    backtrace_list = backtrace(dist_matrix, n, m)

    output_source = ''
    output_connectors = ''
    output_target = ''
    output_modification = ''

    counter_source = 0
    counter_target = 0

    for entry in backtrace_list:
        column_width = 0
        if entry == '' or entry == 'S':
            column_width = max(len(list_source[counter_source]), len(list_target[counter_target])) + 1
            output_source += list_source[counter_source].ljust(column_width)
            output_target += list_target[counter_target].ljust(column_width)
            output_modification += entry.ljust(column_width)
            counter_source += 1
            counter_target += 1
        elif entry == 'D':
            column_width = len(list_source[counter_source]) + 1
            output_source += list_source[counter_source].ljust(column_width)
            output_target += '*'.ljust(column_width)
            output_modification += entry.ljust(column_width)
            counter_source += 1
        elif entry == 'I':
            column_width = len(list_target[counter_target]) + 1
            output_source += '*'.ljust(column_width)
            output_target += list_target[counter_target].ljust(column_width)
            output_modification += entry.ljust(column_width)
            counter_target += 1

        output_connectors += '|'.ljust(column_width)

    print(output_source)
    print(output_connectors)
    print(output_target)
    print(output_modification)
    print('')
    print('Edit distance:', dist_matrix[n][m].value)


def print_matrix(dist_matrix, n, m):
    for row in range(1, n+1):
        row_string = ''
        for col in range(1, m+1):
            res_string = ''
            if dist_matrix[row][col].diagonal_arrow:
                res_string += '\\'
            if dist_matrix[row][col].top_arrow:
                res_string += '|'
            if dist_matrix[row][col].left_arrow:
                res_string += '-'
            row_string += '[' + res_string.ljust(3) + str(dist_matrix[row][col].value).ljust(2) + ']'
        print(row_string)
    print('')


class MatrixEntry(object):

    value = 0
    left_arrow = False;
    diagonal_arrow = False;
    top_arrow = False;

    def __init__(self):
        self.value = 0

    def set_init_value(self, init_value):
        self.value = init_value

    def set_value(self, del_val, sub_val, ins_val):
        self.value = min(del_val, sub_val, ins_val)
        self.top_arrow = self.value == del_val
        self.diagonal_arrow = self.value == sub_val
        self.left_arrow = self.value == ins_val


def main():
    # for same result as in slp3-chapter2, Figure 2.16 use sub_cost = 2!
    # book_a = 'intention'
    # book_b = 'execution'
    # get_edit_distance(book_a, book_b)

    testlist1_a = ['This', 'is', 'nice', 'cat', 'food', '.']
    testlist1_b = ['this', 'is', 'the', 'nice', 'cat', '.']
    get_edit_distance(testlist1_a, testlist1_b)

    # testlist2_a = ['The', 'cat', 'likes', 'tasty', 'fish', '.']
    # testlist2_b = ['The', 'cat', 'likes', 'fish', 'very', 'much', '.']
    # get_edit_distance(testlist2_a, testlist2_b)

    # testlist3_a = ['I', 'have', 'adopted', 'cute', 'cats', '.']
    # testlist3_b = ['I', 'have', 'many', 'cats', '.']
    # get_edit_distance(testlist3_a, testlist3_b)

if __name__ == '__main__':
    main()
