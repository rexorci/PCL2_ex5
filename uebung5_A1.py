#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 5, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738

del_cost = 1
ins_cost = 1
sub_cost = 1


def calculate_edit_distance(list_source, list_target):
    """    
    :param list_source: list of strings/chars from which the distance is calculated
    :param list_target: list of strings/chars to which the distance is calculated
    :return: None
    """
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

            # The matrix contains MatrixEntries, which contain cost plus the origination used for the backtrace
            dist_matrix[row][col].set_value(del_val, sub_val, ins_val)

    print_output(list_source, list_target, dist_matrix, n, m)


def get_sub_cost(token_source, token_target):
    """    
    :param token_source: token of the source list
    :param token_target: token of the target list
    :return: int
    """
    if token_source == token_target:
        return 0
    else:
        return sub_cost


def backtrace(dist_matrix, n, m):
    """
    Walks one of the cheapest paths backward that lead to the minimum cost 
    :param dist_matrix: distance matrix
    :param n: length of source list
    :param m: length of target list
    :return: List of characters containing one of the following: '', 'D', 'I', 'S'
    """
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
                # substitute the same letter has cost = 0
                operations.insert(0, '')
        elif dist_matrix[curr_row][curr_col].top_arrow\
                or (curr_row != 0 and curr_col == 0):  # boundary condition (first column)
            curr_row -= 1
            operations.insert(0, 'D')
            curr_value = dist_matrix[curr_row][curr_col].value

        elif dist_matrix[curr_row][curr_col].left_arrow\
                or (curr_row == 0 and curr_col != 0):  # boundary condition (first row)
            curr_col -= 1
            operations.insert(0, 'I')
            curr_value = dist_matrix[curr_row][curr_col].value
    return operations


def print_output(list_source, list_target, dist_matrix, n, m):
    """
    Shows (on the console) the minimum modification that have to be done to come from list_source to list_target
    :param list_source: list of strings/chars from which the distance is calculated
    :param list_target: list of strings/chars to which the distance is calculated
    :param dist_matrix: Distance Matrix
    :param n: length of source list
    :param m: length of target list
    :return: None
    """
    # print_matrix(dist_matrix, n, m)

    backtrace_list = backtrace(dist_matrix, n, m)

    output_source = ''
    output_connectors = ''
    output_target = ''
    output_modification = ''

    counter_source = 0
    counter_target = 0

    for entry in backtrace_list:
        # to achieve a nice layout we construct the 4 output lines first
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
    """    
    Helper function to visualize the arrows used in the backtrace
    :param dist_matrix: distance matrix
    :param n: length of source list
    :param m: length of target list
    :return: None
    """
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
    """
    Object used for representation of the cell content of the matrix. Arrows point to possible directions for 
    a backtrace.
    """

    value = 0
    left_arrow = False
    diagonal_arrow = False
    top_arrow = False

    def __init__(self):
        self.value = 0

    def set_init_value(self, init_value):
        """        
        :param init_value: cell content value 
        :return: None 
        """
        self.value = init_value

    def set_value(self, del_val, sub_val, ins_val):
        """        
        :param del_val: cost if delete is executed in this step
        :param sub_val: cost if substitution is executed in this step
        :param ins_val:  cost if insert is executed in this step
        :return: None
        """
        # all the directions with the minimum value are possible directions for a backtrace
        self.value = min(del_val, sub_val, ins_val)
        self.top_arrow = self.value == del_val
        self.diagonal_arrow = self.value == sub_val
        self.left_arrow = self.value == ins_val


def main():
    testlist1_a = ['This', 'is', 'nice', 'cat', 'food', '.']
    testlist1_b = ['this', 'is', 'the', 'nice', 'cat', '.']
    calculate_edit_distance(testlist1_a, testlist1_b)

    # testlist2_a = ['The', 'cat', 'likes', 'tasty', 'fish', '.']
    # testlist2_b = ['The', 'cat', 'likes', 'fish', 'very', 'much', '.']
    # calculate_edit_distance(testlist2_a, testlist2_b)

    # testlist3_a = ['I', 'have', 'adopted', 'cute', 'cats', '.']
    # testlist3_b = ['I', 'have', 'many', 'cats', '.']
    # calculate_edit_distance(testlist3_a, testlist3_b)

if __name__ == '__main__':
    main()
