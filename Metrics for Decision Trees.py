'''
Author: Vaibhavi Awghate
Email: vna4493@rit.edu
'''
import csv
import numpy
import math

def main():
    '''
    This function reads the csv file, converts it into 2D integer array and
    calls three functions to compute all three mixed splitting criteria.
    :return:None
    '''
    attributes_array = []
    #reads the csv file
    with open('VHCLS_speeders_by_attributes_v042.csv') as csvfile:
        attributes = csv.reader(csvfile)
        for element in attributes:
            attributes_array.append(','.join(element))

    # converts it into 2D array
    for index in range( len(attributes_array)):
        attributes_array[index] = attributes_array[index].split(',')

    #converts into integer
    for row in range(1, len(attributes_array)):
        for col in range(0,11):
            attributes_array[row][col] = int(attributes_array[row][col])

    # function call to compute weighted Gini index
    getWeightedGiniIndex(attributes_array)
    print("\n")

    # function call to compute weighted Entropy
    getWeightedEntropy(attributes_array)
    print("\n")

    #function call to compute weighted misclassification error
    getWeightedMisclassificationError(attributes_array)

def getWeightedGiniIndex(attributes_array):
    '''
    This function computes the weighted gini index for attributes 4 to 10.
    :param attributes_array: the input 2D array
    :return: None
    '''
    for col_index in range(3,10):

        # getting a particular column and storing in a array
        temp_array = [ [(row[ci]) for ci in range(col_index, col_index+1)] for row in attributes_array ]

        # finding the unique values in retreived column and its count
        unique_array, unique_counts = numpy.unique(temp_array, return_counts=True)
        weighted_gini_index = 0

        # for every unique value in unique array
        for unique_index in range(len(unique_array)-1):
            count_of_0 = 0
            count_of_1 = 0

            # for every row in that column
            for row in range(1, len(attributes_array)):

                # checking if value in that row matches the unique element in unique array
                if int(unique_array[unique_index]) == attributes_array[row][col_index]:

                    # checking the target variable i.e. 0 or 1 for that unique element and
                    # increasing the appropriate counter
                    if attributes_array[row][10] == 0:
                        count_of_0 = count_of_0 + 1
                    if attributes_array[row][10] == 1:
                        count_of_1 = count_of_1 + 1

            # calculating gini for every unique element
            gini = float(1 - math.pow((count_of_0/unique_counts[unique_index]),2)- math.pow((count_of_1/unique_counts[unique_index]),2))

            # calculating weighted gini index
            weighted_gini_index = weighted_gini_index + ((unique_counts[unique_index]/(len(attributes_array)-1))*gini)


        print("weighted gini index for ", attributes_array[0][col_index]," is ", round(weighted_gini_index,3))


def getWeightedEntropy(attributes_array):
    '''
    This function computes the weighted entropy for attributes 4 to 10.
    :param attributes_array: the input 2D array
    :return: None
    '''
    for col_index in range(3,10):

        # getting a particular column and storing in a array
        temp_array = [ [(row[ci]) for ci in range(col_index, col_index+1)] for row in attributes_array ]

        # finding the unique values in retreived column and its count
        unique_array, unique_counts = numpy.unique(temp_array, return_counts=True)
        weighted_entropy = 0

        # for every unique value in unique array
        for unique_index in range(len(unique_array)-1):
            count_of_0 = 0
            count_of_1 = 0

            # for every row in that column
            for row in range(1, len(attributes_array)):

                # checking if value in that row matches the unique element in unique array
                if int(unique_array[unique_index]) == attributes_array[row][col_index]:

                    # checking the target variable i.e. 0 or 1 for that unique element and
                    # increasing the appropriate counter
                    if attributes_array[row][10] == 0:
                        count_of_0 = count_of_0 + 1
                    if attributes_array[row][10] == 1:
                        count_of_1 = count_of_1 + 1

            # calculating entropy for every unique element
            entropy = -((count_of_0/unique_counts[unique_index]) * numpy.log2(count_of_0/unique_counts[unique_index]))-\
                      ((count_of_1/unique_counts[unique_index]) * numpy.log2(count_of_1/unique_counts[unique_index]))

            # calculating weighted entropy
            weighted_entropy = weighted_entropy + ((unique_counts[unique_index]/(len(attributes_array)-1))*entropy)

        print("weighted entropy for ", attributes_array[0][col_index]," is ", round(weighted_entropy,3))

def getWeightedMisclassificationError(attributes_array):
    '''
    This function computes the weighted misclassification error for attributes 4 to 10.
    :param attributes_array: the input 2D array
    :return: None
    '''
    for col_index in range(3,10):

        # getting a particular column and storing in a array
        temp_array = [ [(row[ci]) for ci in range(col_index, col_index+1)] for row in attributes_array ]

        # finding the unique values in retreived column and its count
        unique_array, unique_counts = numpy.unique(temp_array, return_counts=True)
        weighted_misclassification_error = 0

        # for every unique value in unique array
        for unique_index in range(len(unique_array)-1):
            count_of_0 = 0
            count_of_1 = 0

            # for every row in that column
            for row in range(1, len(attributes_array)):

                # checking if value in that row matches the unique element in unique array
                if int(unique_array[unique_index]) == attributes_array[row][col_index]:

                    # checking the target variable i.e. 0 or 1 for that unique element and
                    # increasing the appropriate counter
                    if attributes_array[row][10] == 0:
                        count_of_0 = count_of_0 + 1
                    if attributes_array[row][10] == 1:
                        count_of_1 = count_of_1 + 1

            # calculating misclassification error for every unique element
            misclassification_error = 1 - max((count_of_0/unique_counts[unique_index]), (count_of_1/unique_counts[unique_index]))

            # calculating weighted misclassification error
            weighted_misclassification_error = weighted_misclassification_error + \
                                               ((unique_counts[unique_index]/(len(attributes_array)-1))*misclassification_error)

        print("weighted misclassification for ", attributes_array[0][col_index]," is ", round(weighted_misclassification_error,3))
main()