#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Vorlage
# Uebung 5, Aufgabe 2
"""This module uses a naive bayes classifier to identify the gender of names"""

import random

import itertools

from collections import defaultdict
from nltk.classify import NaiveBayesClassifier, accuracy
from pandas import *

class NaiveBayesClassifierNameGenderPrediction:
    """This class implements the naive bayes classification on gender 
    recognition of names"""

    def __init__(self, female_file, male_file):
        self.male_file = male_file
        self.female_file = female_file

        self.main()

    @staticmethod
    def extract_data(data_file):
        """extract the given data file"""
        extracted_file = open(data_file, 'r', encoding='utf-8')
        extracted_file = extracted_file.readlines()
        return extracted_file

    @staticmethod
    def evaluation(test_set, classifier):
        """Evaluate the classifier with the test set. Print the accuracy,
        precision, recall and f-measure."""
        # TODO: Evaluate the classifier with the test set. Print the
        # overall classifier accuracy, as well as precision, recall and
        # f-measure for male and female

        confusion_matrix = defaultdict(lambda : defaultdict(lambda: 0))
        for feature_set, label in test_set:
            confusion_matrix[label][classifier.classify(feature_set)] += 1

        df = DataFrame(confusion_matrix)
        df.add_prefix("a ")
        print(df)
        print("_________________________________")
        print("")

        #could generealize for any classes easily, ain't no body got time fo dat
        male_precision = confusion_matrix["male"]["male"] / (confusion_matrix["male"]["male"] + confusion_matrix["female"]["male"])
        male_recall = confusion_matrix["male"]["male"] / (confusion_matrix["male"]["male"] + confusion_matrix["male"]["female"])
        male_accuracy = (confusion_matrix["male"]["male"] + confusion_matrix["female"]["female"]) / (confusion_matrix["male"]["male"] + confusion_matrix["female"]["female"] + confusion_matrix["male"]["female"] + confusion_matrix["female"]["male"])
        male_f_measure = 2 * (male_precision * male_recall)/(male_precision + male_recall)

        print("male precison: ", male_precision)
        print("male recall: ", male_recall)
        print("male accuracy: ", male_accuracy)
        print("male f-measure: ", male_f_measure)

        print("_________________________________")
        print("")

        female_precision = confusion_matrix["female"]["female"] / (confusion_matrix["female"]["female"] + confusion_matrix["male"]["female"])
        female_recall = confusion_matrix["female"]["female"] / (confusion_matrix["female"]["female"] + confusion_matrix["female"]["male"])
        female_accuracy = (confusion_matrix["female"]["female"] + confusion_matrix["male"]["male"]) / (confusion_matrix["female"]["female"] + confusion_matrix["male"]["male"] + confusion_matrix["female"]["male"] + confusion_matrix["male"]["female"])
        female_f_measure = 2 * (female_precision * female_recall) / (female_precision + female_recall)

        print("female precison: ", female_precision)
        print("female recall: ", female_recall)
        print("female accuracy: ", female_accuracy)
        print("female f-measure: ", female_f_measure)

        print("_________________________________")
        print("")

    @staticmethod
    def gender_features(name):
        """Return a dictionary with all features to identify the gender of
        a name"""
        gender_features = {}
        c = 0
        for x in name:
            gender_features["letter_{}".format(c)] = name[c].lower()
            c += 1

        gender_features["f1"] = ord(name[-1]) - ord('a') + 1
        gender_features["f2"] = ord(name[-2]) - ord('a') + 1

        return gender_features
        # TODO: Add further features to maximise the classifier's performance.

    def get_training_and_test_labeled_features(self, female_training_data,
                                               male_training_data,
                                               female_test_data,
                                               male_test_data):
        """return a labeled dictionary of all features for the training
        and test data"""
        # TODO: return two feature, label lists, one for training and one 
        # for testing. Each list should be in the form 
        # [({feature1_name:feature1_value, ...}, label), ...]
        return list(itertools.chain(map(lambda name: (self.gender_features(name), "female"), female_training_data),
                                    map(lambda name: (self.gender_features(name), "male"), male_training_data))),\
               list(itertools.chain(map(lambda name: (self.gender_features(name), "female"), female_test_data),
                                    map(lambda name: (self.gender_features(name), "male"), male_test_data)))

    @staticmethod
    def get_train_and_test_data(male_data, female_data):
        """Split the male and female data into training and test data."""
        # TODO: Decide on how to split the male and female data into training
        # and test data. Turn the test and training data into lists which
        # contain each name as an element. Return these lists.

        male_test_data, male_train_data = NaiveBayesClassifierNameGenderPrediction.split_random(male_data, 0.2)
        female_test_data, female_train_data = NaiveBayesClassifierNameGenderPrediction.split_random(female_data, 0.2)

        return male_test_data, male_train_data, female_test_data, female_train_data

    @staticmethod
    def split_random(data_set, sample_ratio):
        """
        Using random reservoir sampling to split data sets
        into two sets with sizes in a certain ratio
        """
        k = int(len(data_set) * sample_ratio)
        sample = []
        rest = []
        i = 0
        for elem in data_set[:k]:
            sample.append(elem)
            i += 1

        for elem in data_set[k:]:
            j = random.randint(0, i)
            if j < k:
                rest.append(sample[j])
                sample[j] = elem
            else:
                rest.append(elem)
            i += 1

        return sample, rest

    def main(self):
        male_data = self.extract_data(self.male_file)
        female_data = self.extract_data(self.female_file)

        male_train_data, male_test_data, female_train_data, female_test_data = \
            self.get_train_and_test_data(male_data, female_data)

        # get the training and test set for the classifier and the evaluation
        train_set, test_set = self.get_training_and_test_labeled_features(
            female_train_data, male_train_data, female_test_data,
            male_test_data)

        # create classifier with the training set
        classifier = NaiveBayesClassifier.train(train_set)

        # print the evaluation with the precision, recall and f-measure
        self.evaluation(test_set, classifier)

        # print the 10 most informative features 
        classifier.show_most_informative_features(10)


if __name__ == '__main__':
    NaiveBayesClassifierNameGenderPrediction('female.txt',
                                             'male.txt')
