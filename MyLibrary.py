from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification
from sklearn.svm import LinearSVC
from sklearn.neighbors import NearestCentroid
import xlrd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from enum import Enum


def determine_clf_type(clf):
    """Determines type of classifier

    :param clf:
    :return: clfType: ClfType
    """
    try:
        clf.coef_
        return ClfType.LINEAR
    except:
        # print('No coef_ attribute')
        pass
    try:
        clf.centroids_
        return ClfType.MEAN
    except:
        # print('No centroids_ attribute')
        print('No attribute found')
    raise Exception('Classifier not defined')


def initialize_classifiers(number_of_classifiers, type_of_classifier):
    """Generates list of classifiers for analysis

    :param number_of_classifiers: Number of classifiers
    :param type_of_classifier: type of Sklearn classifier
    :return: List of classifiers: [clf, ..., clf]
    """
    clfs = []
    if type_of_classifier == ClfType.LINEAR:
        for i in range(number_of_classifiers):
            clfs.append(LinearSVC(max_iter = 1e8, tol = 1e-10))
    elif type_of_classifier == ClfType.MEAN:
        for i in range(number_of_classifiers):
            clfs.append(NearestCentroid())
    else:
        raise Exception('Classifier type not defined')
    return clfs


def prepare_raw_data(are_samples_generated = True, number_of_samples_if_generated = 100, number_of_dataset_if_not_generated = 12, number_of_classifiers = 3,
                     number_of_space_parts = 5):
    """Prepares raw data for classification

    :param are_samples_generated: boolean
    :param number_of_samples_if_generated: int
    :param number_of_dataset_if_not_generated: int
    :return: X, y: np.array, np.array
    """
    if are_samples_generated:
        X, y = make_classification(n_features = 2, n_redundant = 0, n_informative = 1, n_clusters_per_class = 1, n_samples = number_of_samples_if_generated,
                                   class_sep = 2.7, hypercube = False, random_state = 2)
        X0, X1 = divide_generated_samples(X, y)
        X0, X1 = sort_attributes(X0), sort_attributes(X1)
        length0, length1 = len(X0), len(X1)
        while True:
            X0, X1 = assert_distribution(X0, X1, number_of_classifiers, number_of_space_parts)
            if len(X0) == length0 and len(X1) == length1:
                break
            length0, length1 = len(X0), len(X1)
        return compose_sorted_parts(X0, X1)
    else:
        return load_samples_from_datasets(number_of_dataset_if_not_generated, number_of_classifiers, number_of_space_parts)


def load_samples_from_file(filename):
    """Loads data from file

    Warning: method does not sort data
    Missing sorting and composing
    :param filename: Name of file
    :return: X, y: np.array, np.array - samples for classification
    """
    file = xlrd.open_workbook(filename)
    sheet = file.sheet_by_index(0)
    line_number = 0
    line = sheet.row(line_number)
    number_of_columns = len(line)
    X, y = np.zeros((sheet.nrows, 2)), np.zeros(sheet.nrows, dtype = np.int)
    while line_number < sheet.nrows - 1:
        line_number += 1
        line = sheet.row(line_number)
        row = []
        for i in range(2):  # range(number_of_columns - 1):
            row.append(float(line[i].value))
        X[line_number - 1, :] = row
        y[line_number - 1] = int(line[number_of_columns - 1].value)
    X = SelectKBest(k = 2).fit_transform(X, y)
    return X, y


def load_samples_from_datasets(number = 12, number_of_classifiers = 3, number_of_space_parts = 5):
    """Loads data from dataset (xlsx file with data)

    :param number: int, number of sheet
    :param number_of_space_parts: int
    :param number_of_classifiers: int
    :return: X, y: np.array, np.array - samples for classification
    """
    file = xlrd.open_workbook('datasets.xlsx')
    sheet = file.sheet_by_index(number)
    line_number = 0
    line = sheet.row(line_number)
    number_of_columns = len(line)
    X0, X1 = [], []
    while line_number < sheet.nrows:
        line = sheet.row(line_number)
        row = []
        for i in range(2):  # range(number_of_columns - 1):
            row.append(float(line[i].value))
        if int(line[number_of_columns - 1].value) == 0:
            X0.append(row)
        else:
            X1.append(row)
        line_number += 1
    # X = SelectKBest(k = 2).fit_transform(X, y)
    print('Ratio (0:1): {}:{}'.format(len(X0), len(X1)))
    X0, X1 = sort_attributes(X0), sort_attributes(X1)
    length0, length1 = len(X0), len(X1)
    while True:
        X0, X1 = assert_distribution(X0, X1, number_of_classifiers, number_of_space_parts)
        if len(X0) == length0 and len(X1) == length1:
            break
        length0, length1 = len(X0), len(X1)
    X, y = compose_sorted_parts(X0, X1)
    return X, y


def assert_distribution(X0, X1, number_of_classifiers = 3, number_of_space_parts = 5):
    """Asserts that samples can be divided into subspaces with the same amount of data

    :param X0: np.array, data with class 0
    :param X1: np.array, data with class 1
    :param number_of_classifiers: int
    :param number_of_space_parts: int
    :return: X0, X1: np.array, np.array, data prepared to be divided into number_of_classifiers + 2 parts of same length
    """
    print('len0: {}, len1: {}'.format(len(X0), len(X1)))
    x0_min, x0_max = get_subdata_limits(X0)
    x1_min, x1_max = get_subdata_limits(X1)
    x_min, x_max = min(x0_min, x1_min), max(x0_max, x1_max)
    for i in range(number_of_space_parts):
        counter0, counter1, index0, index1 = 0, 0, 0, 0
        while True:
            if index0 == len(X0):
                break
            if x_min + i * (x_max - x_min) / number_of_space_parts <= X0[index0][0] <= x_min + (i + 1) * (x_max - x_min) / number_of_space_parts:
                counter0 += 1
                index0 += 1
                continue
            if counter0 > 0:
                break
            index0 += 1
        while True:
            if index1 == len(X1):
                break
            if x_min + i * (x_max - x_min) / number_of_space_parts <= X1[index1][0] <= x_min + (i + 1) * (x_max - x_min) / number_of_space_parts:
                counter1 += 1
                index1 += 1
                continue
            if counter1 > 0:
                break
            index1 += 1
        if counter0 + counter1 < number_of_classifiers + 2:
            print('Only {} samples in {}. subspace'.format(counter0 + counter1, i + 1))
            # raise Exception('Not enough samples')
        remainder = (counter0 + counter1) % (number_of_classifiers + 2)
        if remainder != 0:
            if i == 0:
                if len(X0) > len(X1):
                    return assert_distribution(X0[1:], X1, number_of_classifiers, number_of_space_parts)
                return assert_distribution(X0, X1[1:], number_of_classifiers, number_of_space_parts)
            if i == number_of_space_parts - 1:
                if len(X0) > len(X1):
                    return assert_distribution(X0[:-1], X1, number_of_classifiers, number_of_space_parts)
                return assert_distribution(X0, X1[:-1], number_of_classifiers, number_of_space_parts)
            if len(X0) > len(X1):
                if counter0 < remainder:
                    subtraction, rest = counter0, remainder - counter0
                else:
                    subtraction, rest = remainder, 0
                X0 = np.vstack((X0[:index0 - subtraction], X0[index0:]))
                X1 = np.vstack((X1[:index1 - rest], X1[index1:]))
            else:
                if counter1 < remainder:
                    subtraction, rest = counter1, remainder - counter1
                else:
                    subtraction, rest = remainder, 0
                X0 = np.vstack((X0[:index0 - rest], X0[index0:]))
                X1 = np.vstack((X1[:index1 - subtraction], X1[index1:]))
    print('len0: {}, len1: {}'.format(len(X0), len(X1)))
    return X0, X1


def assert_distribution_simplified(X0, X1, number_of_classifiers = 3, number_of_space_parts = 5):
    """Asserts that samples can be divided into subspaces with the same amount of data

    :param X0: np.array, data with class 0
    :param X1: np.array, data with class 1
    :param number_of_classifiers: int
    :param number_of_space_parts: int
    :return: X0, X1: np.array, np.array, data prepared to be divided into number_of_classifiers + 2 parts of same length
    """
    x_min, x_max = get_extrema_for_subspaces(X0, X1)
    previous_index0, previous_index1 = 0, 0
    for i in range(number_of_space_parts):
        print('Before assertion: len0: {}, len1: {}'.format(len(X0), len(X1)))
        counter0, index0 = get_count_of_samples_in_subspace_and_beginning_index_of_next_subspace(X0, x_min, x_max, i, number_of_space_parts)
        counter1, index1 = get_count_of_samples_in_subspace_and_beginning_index_of_next_subspace(X1, x_min, x_max, i, number_of_space_parts)
        if counter0 + counter1 < number_of_classifiers + 2:
            print('Only {} samples in {}. subspace'.format(counter0 + counter1, i + 1))
            # raise Exception('Not enough samples')
        remainder = (counter0 + counter1) % (number_of_classifiers + 2)
        if remainder != 0:
            if i != number_of_space_parts - 1:
                relative_index0, relative_index1, is_last = index0, index1, False
            else:
                relative_index0, relative_index1, is_last = previous_index0, previous_index1, True
            if counter0 > counter1:
                counter, is_first_bigger = counter0, True
            else:
                counter, is_first_bigger = counter1, False
            X0, X1 = limit_datasets(X0, X1, counter, remainder, relative_index0, relative_index1, is_first_bigger, is_last)
        previous_index0, previous_index1 = index0, index1
    print('After assertion: len0: {}, len1: {}'.format(len(X0), len(X1)))
    return X0, X1


def get_extrema_for_subspaces(X0, X1):
    """Returns minimum and maximum bor both datasets

    :param X0: np.array
    :param X1: np.array
    :return: minimum, maximum: float, float
    """
    x0_min, x0_max = get_subdata_limits(X0)
    x1_min, x1_max = get_subdata_limits(X1)
    return min(x0_min, x1_min), max(x0_max, x1_max)


def get_count_of_samples_in_subspace_and_beginning_index_of_next_subspace(X0, x_min, x_max, i, number_of_space_parts = 5):
    """Returns of count of data in subspace as well as index of the first element of next subspace

    :param X0: np.array
    :param x_min: float
    :param x_max: float
    :param i: int, number of subspace - 1
    :param number_of_space_parts: int
    :return: counter, index: int, int
    """
    counter, index = 0, 0
    while True:
        if index == len(X0):
            break
        if x_min + i * (x_max - x_min) / number_of_space_parts <= X0[index][0] <= x_min + (i + 1) * (x_max - x_min) / number_of_space_parts:
            counter += 1
            index += 1
            continue
        if counter > 0:
            break
        index += 1
    return counter, index


def set_subtraction_and_rest(counter, remainder):
    """Calculates substracion and rest for limiting datasets

    :param counter: int
    :param remainder: int
    :return: substraction, rest: int, int
    """
    if counter < remainder:
        return counter, remainder - counter
    else:
        return remainder, 0


def limit_datasets_for_every_subspace_but_last(X0, X1, counter, remainder, index0, index1, is_first_bigger):
    """Returns limited datasets for every subspace but last one

    :param X0: np.array
    :param X1: np.array
    :param counter: int
    :param remainder: int
    :param index0: int
    :param index1: int
    :param is_first_bigger: boolean, true if there is more data in analysiert subspace in the first dataset
    :return: X0, X1: np.array, np.array
    """
    subtraction, rest = set_subtraction_and_rest(counter, remainder)
    if is_first_bigger:
        first_subtraction, second_subtraction = subtraction, rest
    else:
        first_subtraction, second_subtraction = rest, subtraction
    X0 = np.vstack((X0[:index0 - first_subtraction], X0[index0:]))
    X1 = np.vstack((X1[:index1 - second_subtraction], X1[index1:]))
    return X0, X1


def limit_datasets_for_last_subspace(X0, X1, counter, remainder, previous_index0, previous_index1, is_first_bigger):
    """Returns limited datasets for last subspace

    :param X0: np.array
    :param X1: np.array
    :param counter: int
    :param remainder: int
    :param previous_index0: int
    :param previous_index1: int
    :param is_first_bigger: boolean, true if there is more data in analysiert subspace in the first dataset
    :return: X0, X1: np.array, np.array
    """
    subtraction, rest = set_subtraction_and_rest(counter, remainder)
    if is_first_bigger:
        first_subtraction, second_subtraction = subtraction, rest
    else:
        first_subtraction, second_subtraction = rest, subtraction
    X0 = np.vstack((X0[:previous_index0], X0[previous_index0 + first_subtraction:]))
    X1 = np.vstack((X1[:previous_index1], X1[previous_index1 + second_subtraction:]))
    return X0, X1


def limit_datasets(X0, X1, counter, remainder, relative_index0, relative_index1, is_first_bigger, is_last):
    """Returns limited datasets

    :param X0: np.array
    :param X1: np.array
    :param counter: int
    :param remainder: int
    :param relative_index0: int
    :param relative_index1: int
    :param is_first_bigger: boolean
    :param is_last: boolean, true if it is last subspace
    :return: X0, X1: np.array, np.array
    """
    if is_last:
        return limit_datasets_for_last_subspace(X0, X1, counter, remainder, relative_index0, relative_index1, is_first_bigger)
    else:
        return limit_datasets_for_every_subspace_but_last(X0, X1, counter, remainder, relative_index0, relative_index1, is_first_bigger)


def compose_sorted_parts(X0, X1):
    """Composes classification data from 1 and 0 parts, datasets must be sorted

    :param X0: [], data, where y = 0
    :param X1: [], data, where y = 1
    :return: X, y: np.array, np.array - samples for classification
    """
    X, y = np.zeros((len(X0) + len(X1), 2)), np.zeros(len(X0) + len(X1), dtype = np.int)
    for i in range(len(X0)):
        X[i, :], y[i] = X0[i], 0
    for i in range(len(X1)):
        X[len(X0) + i, :], y[len(X0) + i] = X1[i], 1
    return X, y


def sort_attributes(X):
    """Sorts attribute array

    :param X: []
    :return: X: np.array
    """
    length, X_result_array = len(X), []
    for input_index in range(length):
        output_index = 0
        while output_index < input_index:
            if X_result_array[output_index][0] > X[input_index][0]:
                break
            output_index += 1
        X_result_array.insert(output_index, X[input_index])
    X_result = np.zeros((length, 2))
    for i in range(length):
        X_result[i, :] = X_result_array[i]
    return X_result


def sort_results(X, y):
    """Sorts attribute and class arrays

    Warning: does not sort by classes (y is not taken into consideration)
    :param X: np.array
    :param y: np.array
    :return: X, y: np.array, np.array
    """
    length = len(y)
    X_result_array, y_result_array = [], []
    for input_index in range(length):
        output_index = 0
        while output_index < input_index:
            if X_result_array[output_index][0] > X[input_index, 0]:
                break
            output_index += 1
        X_result_array.insert(output_index, X[input_index, :])
        y_result_array.insert(output_index, y[input_index])
    X_result, y_result = np.zeros((length, 2)), np.zeros(length, dtype = np.int)
    for i in range(length):
        X_result[i, :] = X_result_array[i]
        y_result[i] = y_result_array[i]
    return X_result, y_result


def divide_generated_samples(X, y):
    """Divide samples into arrays X0 (with y = 0) and X1 (y = 1)

    :param X: np.array
    :param y: np.array
    :return: X0, X1: [], []
    """
    X0, X1 = [], []
    for i in range(len(y)):
        if y[i] == 0:
            X0.append(X[i, :])
        else:
            X1.append(X[i, :])
    return X0, X1


def divide_samples_between_classifiers(X, y, number_of_classifiers = 3):
    """Divides sample into parts for every classifier

    Warning: does not take sorting into consideration
    Prepares n = number_of_classifiers + 1 parts X(k) and y(k) with the same count
    and returns [X(1), X(2), ..., X(n - 1)], [y(1), y(2), ..., y(n - 1)], X(n), y(n)
    :param X: np.array, raw data
    :param y: np.array, raw data
    :param number_of_classifiers: total number of classifiers (excluding composite)
    :return: [X(1), X(2), ..., X(n - 1)], [y(1), y(2), ..., y(n - 1)], X(n), y(n)
    """
    number_of_samples = len(X)
    X_whole, y_whole, X_rest, y_rest = [], [], [], []
    X_final_test, X_rest, y_final_test, y_rest = \
        train_test_split(X, y, train_size = int(number_of_samples / (number_of_classifiers + 1)))
    for i in range(number_of_classifiers - 1):
        X_part, X_rest, y_part, y_rest = \
            train_test_split(X_rest, y_rest, train_size = int(number_of_samples / (number_of_classifiers + 1)))
        X_whole.append(X_part)
        y_whole.append(y_part)
    X_whole.append(X_rest)
    y_whole.append(y_rest)
    return X_whole, y_whole, X_final_test, y_final_test


def split_sorted_samples_between_classifiers(X, y, number_of_classifiers = 3):
    """Splits sorted samples between classifiers

    :param X: np.array
    :param y: np.array
    :param number_of_classifiers: int
    :return: X_whole, y_whole, X_final_test, y_final_test: [np.array(1), np.array(2), ..., np.array(number_of_classifiers)],
    [np.array(1), np.array(2), ..., np.array(number_of_classifiers)], np.array, np.array
    """
    length = int(len(X) / (number_of_classifiers + 1))
    X_whole, y_whole, X_final_test, y_final_test = [], [], np.zeros((length, 2)), np.zeros(length, dtype = np.int)
    for i in range(number_of_classifiers):
        X_temp, y_temp = np.zeros((length, 2)), np.zeros(length, dtype = np.int)
        for j in range(length):
            X_temp[j, :] = (X[j * (number_of_classifiers + 1) + i, :])
            y_temp[j] = (y[j * (number_of_classifiers + 1) + i])
        X_whole.append(X_temp)
        y_whole.append(y_temp)
    for i in range(length):
        X_final_test[i, :] = (X[(i + 1) * number_of_classifiers + i, :])
        y_final_test[i] = (y[(i + 1) * number_of_classifiers + i])
    return X_whole, y_whole, X_final_test, y_final_test


def divide_samples_between_training_and_testing(X_unsplitted, y_unsplitted, quotient = 2 / 3):
    """Divides sample into parts for ttaining and testing

    Warning: does not take sorting into consideration
    :param X_unsplitted: [np.array(1), np.array(2), ..., np.array(n - 1)]
    :param y_unsplitted: [np.array(1), np.array(2), ..., np.array(n - 1)]
    :param quotient: float
    :return: X_train, X_test, y_train, y_test: [np.array(1), np.array(2), ..., np.array(n - 1)], [np.array(1), np.array(2), ..., np.array(n - 1)],
    [np.array(1), np.array(2), ..., np.array(n - 1)], [np.array(1), np.array(2), ..., np.array(n - 1)]
    """
    X_train, X_test, y_train, y_test = [], [], [], []
    for X_one, y_one in zip(X_unsplitted, y_unsplitted):
        X_train_part, X_test_part, y_train_part, y_test_part = train_test_split(X_one, y_one, train_size = int(len(X_one) * quotient))
        X_train.append(X_train_part)
        X_test.append(X_test_part)
        y_train.append(y_train_part)
        y_test.append(y_test_part)
    return X_train, X_test, y_train, y_test


def split_sorted_samples_between_training_and_testing(X_unsplitted, y_unsplitted, quotient = 2 / 3):
    """Splits sorted samples for testing and training

    :param X_unsplitted: [np.array(1), np.array(2), ..., np.array(n - 1)]
    :param y_unsplitted: [np.array(1), np.array(2), ..., np.array(n - 1)]
    :param quotient: float
    :return: X_train, X_test, y_train, y_test: [np.array(1), np.array(2), ..., np.array(n - 1)], [np.array(1), np.array(2), ..., np.array(n - 1)],
    [np.array(1), np.array(2), ..., np.array(n - 1)], [np.array(1), np.array(2), ..., np.array(n - 1)]
    """
    X_train, X_test, y_train, y_test = [], [], [], []
    for X_one, y_one in zip(X_unsplitted, y_unsplitted):
        X_train_part, X_test_part, y_train_part, y_test_part = train_test_sorted_split(X_one, y_one, quotient)
        X_train.append(X_train_part)
        X_test.append(X_test_part)
        y_train.append(y_train_part)
        y_test.append(y_test_part)
    return X_train, X_test, y_train, y_test


def split_sorted_samples(X, y, number_of_classifiers = 3, number_of_space_parts = 5):
    """Splits raw data into number_of_classifiers + 2 parts of same length

    :param X: np.array, array with sorted data
    :param y: np.array
    :param number_of_classifiers: int
    :param number_of_space_parts: int
    :return: X_whole_train, y_whole_train, X_validation, y_validation, X_test, y_test: [np.array(1), np.array(2), ..., np.array(number_of_classifiers)],
    [np.array(1), np.array(2), ..., np.array(number_of_classifiers)], np.array, np.array, np.array, np.array
    """
    print('Splitting samples')
    if len(X) < (number_of_classifiers + 2) * number_of_space_parts:
        print('Not enough samples')
        raise Exception('Not enough samples')
    length = int(len(X) / (number_of_classifiers + 2))
    X_whole_train, y_whole_train, X_validation, y_validation, X_test, y_test = \
        [], [], np.zeros((length, 2)), np.zeros(length, dtype = np.int), np.zeros((length, 2)), np.zeros(length, dtype = np.int)
    for i in range(number_of_classifiers):
        X_temp, y_temp = np.zeros((length, 2)), np.zeros(length, dtype = np.int)
        for j in range(length):
            X_temp[j, :] = (X[j * (number_of_classifiers + 1) + i, :])
            y_temp[j] = (y[j * (number_of_classifiers + 1) + i])
        X_whole_train.append(X_temp)
        y_whole_train.append(y_temp)
    for i in range(length):
        X_validation[i, :] = (X[(i + 1) * number_of_classifiers - 2, :])
        y_validation[i] = (y[(i + 1) * number_of_classifiers - 2])
    for i in range(length):
        X_test[i, :] = (X[(i + 1) * number_of_classifiers - 1, :])
        y_test[i] = (y[(i + 1) * number_of_classifiers - 1])
    return X_whole_train, y_whole_train, X_validation, y_validation, X_test, y_test


def train_test_sorted_split(X_one, y_one, quotient = 2 / 3):
    """Splits dataset into training and testing

    :param X_one: np.array
    :param y_one: np.array
    :param quotient: float
    :return: X_train, X_test, y_train, y_test: np.array, np.array, np.array, np.array
    """
    quotient_freq = 1 / (1 - quotient)
    if quotient_freq - int(quotient_freq) - 1 < 1e-3:
        quotient_freq = int(quotient_freq) + 1
    else:
        quotient_freq = int(quotient_freq)
    length = int(len(y_one) / quotient_freq)
    X_train, X_test, y_train, y_test = np.zeros((length * (quotient_freq - 1), 2)), np.zeros((length, 2)), \
                                       np.zeros(length * (quotient_freq - 1), dtype = np.int), np.zeros(length, dtype = np.int)
    counter = 0
    for i in range(length):
        for j in range(quotient_freq - 1):
            X_train[counter, :] = X_one[i * quotient_freq + j, :]
            y_train[counter] = y_one[i * quotient_freq + j]
            counter += 1
        X_test[i, :] = X_one[(i + 1) * quotient_freq - 1]
        y_test[i] = y_one[(i + 1) * quotient_freq - 1]
    return X_train, X_test, y_train, y_test


def prepare_samples_for_subspace(X_test, y_test, X, j, partitioning = 5):
    """Preparing sample for testing in j-th subspace

    :param X_test: np.array
    :param y_test: np.array
    :param X: np.array
    :param j: int
    :param partitioning: int
    :return: X_part, y_part: [], []
    """
    x_samp_max, x_samp_min = get_subspace_limits(X, j, partitioning)
    X_part = [row for row in X_test if x_samp_min < row[0] < x_samp_max]
    y_part = [y_test[k] for k in range(len(y_test)) if x_samp_min < X_test[k][0] < x_samp_max]
    return X_part, y_part


def get_samples_limits(X):
    """Gets limits of j-th subspace

    :param X: np.array
    :return: X_0_min, X_0_max, X_1_min, X_1_max: float, float, float, float
    """
    return X[:, 0].min(), X[:, 0].max(), X[:, 1].min(), X[:, 1].max()


def get_subdata_limits(X):
    """Gets limits of one dimensional dataset

    :param X: np.array
    :return: minimum, maximum: float, float
    """
    minimum, maximum = X[0][0], X[0][0]
    for i in range(len(X)):
        if X[i][0] < minimum:
            minimum = X[i][0]
        if X[i][0] > maximum:
            maximum = X[i][0]
    return minimum, maximum


def get_plot_data(X, plot_mesh_step_size = .2):
    """Prepares data for plot generation

    :param X: np.array
    :param plot_mesh_step_size: float
    :return: xx, yy, x_min_plot, x_max_plot: dnarray, dnarray, float, float
    """
    print('Getting data for plot')
    x_min, x_max, y_min, y_max = get_samples_limits(X)
    x_shift = 0.1 * (x_max - x_min)
    y_shift = 0.1 * (y_max - y_min)
    x_min_plot, x_max_plot, y_min_plot, y_max_plot = x_min - x_shift, x_max + x_shift, y_min - y_shift, y_max + y_shift
    xx, yy = np.meshgrid(np.arange(x_min_plot, x_max_plot, plot_mesh_step_size), np.arange(y_min_plot, y_max_plot, plot_mesh_step_size))
    return xx, yy, x_min_plot, x_max_plot


def determine_number_of_subplots(draw_color_plot = False, number_of_classifiers = 3):
    """Checks number of subplots to draw
    
    :param draw_color_plot: boolean, if true - draws plots generated by scikit
    :param number_of_classifiers: int
    :return: int, number of subplots to draw
    """
    if draw_color_plot:
        return number_of_classifiers * 2 + 1
    return number_of_classifiers + 1


def train_classifiers(clfs, X_whole_train, y_whole_train, type_of_classifier, number_of_subplots, X, plot_mesh_step_size = .2, draw_color_plot = False):
    """Trains classifiers

    :param clfs: [], scikit classifiers
    :param X_whole_train: [np.array(1), np.array(2), ..., np.array(number_of_classifiers)]
    :param y_whole_train: [np.array(1), np.array(2), ..., np.array(number_of_classifiers)]
    :param type_of_classifier: ClfType
    :param number_of_subplots: int
    :param X: np.array
    :param plot_mesh_step_size: float
    :param draw_color_plot: boolean, if true - draws plots generated by scikit
    :return: trained_clfs, coefficients: [], []
    """
    print('Training classifiers')
    trained_clfs, coefficients, current_subplot = [], [], 1
    xx, yy, x_min_plot, x_max_plot = get_plot_data(X, plot_mesh_step_size)
    for clf, X_train, y_train in zip(clfs, X_whole_train, y_whole_train):
        clf.fit(X_train, y_train)
        print(clf.coef_)
        trained_clfs.append(clf)

        if type_of_classifier == ClfType.LINEAR:
            a, b = extract_coefficients_for_linear(clf)
        elif type_of_classifier == ClfType.MEAN:
            a, b = extract_coefficients_for_mean(clf)

        coefficients.append([a, b])

        # Prepare plot
        ax = plt.subplot(1, number_of_subplots, current_subplot)
        ax.scatter(X_train[:, 0], X_train[:, 1], c = y_train)
        x = np.linspace(x_min_plot, x_max_plot)
        y = a * x + b
        ax.plot(x, y)
        ax.set_xlim(xx.min(), xx.max())
        ax.set_ylim(yy.min(), yy.max())
        current_subplot += 1

        if draw_color_plot:
            # Draw color plot
            print('Drawing color plot')
            ax = plt.subplot(1, number_of_subplots, current_subplot)
            if hasattr(clf, 'decision_function'):
                Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
            elif hasattr(clf, 'predict_proba'):
                Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
            else:
                Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
            Z = Z.reshape(xx.shape)
            ax.contourf(xx, yy, Z, alpha = .8)
            current_subplot += 1
    return trained_clfs, coefficients


def extract_coefficients_for_linear(clf):
    """Gets a and b coefficients of the linear classifier

    :param clf: Clf
    :return: a, b: float, float
    """
    a, b = - clf.coef_[0][0] / clf.coef_[0][1], - clf.intercept_[0] / clf.coef_[0][1]
    return a, b


def extract_coefficients_for_mean(clf):
    """Extracts coefficients for mean classifier

    :param clf: Clf
    :return: a, b: float, float
    """
    x1, x2, y1, y2 = clf.centroids_[0][0], clf.centroids_[1][0], clf.centroids_[0][1], clf.centroids_[1][1]
    a_t = (y2 - y1) / (x2 - x1)
    a = -1 / a_t
    x3, y3 = (x1 + x2) / 2, (y1 + y2) / 2
    b = y3 - a * x3
    return a, b


def evaluate_average_coefficients_from_n_best(coefficients, number_of_classifiers,
                                              scores, j, number_of_best_classifiers):
    """Evaluates coefficients from n best classifiers in j-th subspace

    :param coefficients: []
    :param number_of_classifiers: int
    :param scores: []
    :param j: int
    :param number_of_best_classifiers: int
    :return: a, b: float, float
    """
    a, b, sumOfScores, params = 0, 0, 0, []
    for i in range(number_of_classifiers):
        params.append([scores[i][j], coefficients[i]])
    params.sort()
    for i in range(number_of_best_classifiers):
        sumOfScores += params[i][0]
        a += params[i][1][0]
        b += params[i][1][1]
    return a / number_of_best_classifiers, b / number_of_best_classifiers


def get_subspace_limits(X, j, number_of_subspaces = 5):
    """Gets limits of j-th subspace

    :param X: np.array
    :param j: int
    :param number_of_subspaces: int
    :return: x_subspace_max, x_subspace_min: float, float
    """
    x_subspace_min, x_subspace_max = \
        X[:, 0].min() + j * (X[:, 0].max() - X[:, 0].min()) / number_of_subspaces, \
        X[:, 0].min() + (j + 1) * (X[:, 0].max() - X[:, 0].min()) / number_of_subspaces
    return x_subspace_max, x_subspace_min


def test_classifiers(clfs, X_validation, y_validation, X, coefficients, number_of_space_parts = 5, write_computed_scores = False):
    """Tests classifiers

    :param clfs: clfs: [], scikit classifiers
    :param number_of_space_parts: int
    :param X_validation: np.array
    :param y_validation: np.array
    :param X: np.array
    :param coefficients: []
    :param write_computed_scores: boolean
    :return: scores: []
    """
    scores, i = [], 0
    for clf in clfs:
        score = []
        for j in range(number_of_space_parts):
            X_part, y_part = prepare_samples_for_subspace(X_validation, y_validation, X, j, number_of_space_parts)
            if len(X_part) > 0:
                score.append(clf.score(X_part, y_part))
            else:
                score.append(0)
        scores.append(score)

        a, b = coefficients[i]

        if write_computed_scores:
            # Computing scores manually
            print('Compute scores manually')
            for j in range(number_of_space_parts):
                X_part, y_part = prepare_samples_for_subspace(X_validation, y_validation, X, j, number_of_space_parts)
                propperly_classified, all_classified = 0, 0
                for k in range(len(X_part)):
                    if (a * X_part[k][0] + b > X_part[k][1]) ^ (y_part[k] == 1):
                        propperly_classified += 1
                    all_classified += 1
                if not (all_classified == 0):
                    print(propperly_classified / all_classified)
                else:
                    print('No samples')
        i += 1
    return scores


def prepare_composite_classifier(X_test, y_test, X, number_of_best_classifiers, coefficients, scores, number_of_subplots, number_of_space_parts = 5,
                                 number_of_classifiers = 3, plot_mesh_step_size = .2):
    """Prepares composite classifiers

    :param X_test: np.array
    :param y_test: np.array
    :param X: np.array
    :param number_of_space_parts: int
    :param number_of_classifiers: int
    :param number_of_best_classifiers: int
    :param coefficients: []
    :param scores: []
    :param plot_mesh_step_size: float
    :param number_of_subplots: int
    :return: scores: []
    """
    print('Preparing composite classifier')
    score, flip_index = [], 0
    ax = plt.subplot(1, number_of_subplots, number_of_subplots)
    ax.scatter(X_test[:, 0], X_test[:, 1], c = y_test)
    for j in range(number_of_space_parts):
        x_subspace_min, x_subspace_max = get_subspace_limits(X, j, number_of_space_parts)
        x = np.linspace(x_subspace_min, x_subspace_max)
        a, b = evaluate_average_coefficients_from_n_best(coefficients, number_of_classifiers, scores, j, number_of_best_classifiers)
        y = a * x + b
        ax.plot(x, y)
        X_part, y_part = prepare_samples_for_subspace(X_test, y_test, X, j, number_of_space_parts)
        # Checking if the orientation is correct and determining score
        if len(X_part) > 0:
            propperly_classified = 0
            all_classified = 0
            flip_index = 0
            for k in range(len(X_part)):
                if (a * X_part[k][0] + b > X_part[k][1]) ^ (y_part[k] == 1):
                    propperly_classified += 1
                all_classified += 1
            if propperly_classified / all_classified < 0.5:
                score.append(1 - propperly_classified / all_classified)
                flip_index += 1
            else:
                score.append(propperly_classified / all_classified)
                flip_index -= 1
        else:
            score.append(0)
    if flip_index > 0:
        for k in range(len(score)):
            score[k] = 1 - score[k]
    scores.append(score)
    xx, yy, x_min_plot, x_max_plot = get_plot_data(X, plot_mesh_step_size)
    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    return scores


def print_results(scores):
    """Prints final scores

    :param scores: []
    :return: void
    """
    i = 1
    for row in scores:
        print('Classifier ' + str(i))
        print(row)
        i += 1


class ClfType(Enum):
    """Defines the type of classifier


    """
    LINEAR = 0
    MEAN = 1
