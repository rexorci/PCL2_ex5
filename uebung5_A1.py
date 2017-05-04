#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PCL 2, FS 17
# Übung 5, Aufgabe 1
# Autoren: Christoph Weber, Patrick Dueggelin
# Matrikel-Nr.: 10-924-231, 14-704-738


def get_edit_distance(list_from, list_to):
    pass


def main():
    testlist1_a = ['This', 'is', 'nice', 'cat', 'food', '.']
    testlist1_b = ['this', 'is', 'the', 'nice', 'cat', '.']
    get_edit_distance(testlist1_a, testlist1_b)

    # testlist2_a = ['The', 'cat', 'likes', 'tasty', 'fish', '.']
    # testlist2_b = ['The', 'cat', 'likes', 'fish', 'very', 'much', '.']
    # get_edit_distance(testlist2_a, testlist2_b)
    #
    # testlist3_a = ['I', 'have', 'adopted', 'cute', 'cats', '.']
    # testlist3_b = ['I', 'have', 'many', 'cats', '.']
    # get_edit_distance(testlist3_a, testlist3_b)

if __name__ == '__main__':
    main()
