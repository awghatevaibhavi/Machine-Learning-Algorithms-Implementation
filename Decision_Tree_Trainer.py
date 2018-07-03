'''
Author: Vaibhavi Awghate
Email: vna4493@rit.edu
'''
import csv
import numpy


def build_decision_tree(input_file, height, writer):
    '''
    This function builds the decision tree based on minimum entropy.
    :param input_file: Training data on which decision tree is built
    :param height: height of resultant decision tree
    :param writer: Object to write in another python file
    :return: writes class 0 or 1
    '''
    height = height + 1

    #calculates mixed entropy for every attribute and returns the attribute with minimum
    #entropy and its threshold
    min_entropy, column_index, threshold = calculate_mixed_entropy(input_file)

    #splits the data into two subsets and returns them
    gte_data, lt_data = split_the_data(input_file, column_index, threshold)

    #counts for leaf nodes
    count_for_0_for_gte = 0
    count_for_1_for_gte = 0
    count_for_0_for_lt = 0
    count_for_1_for_lt = 0

    #counting the number of zeros and ones for leaf nodes
    for col in range(4,5):
        for row in range(len(gte_data)):
            if gte_data[row][col] == 0:
                count_for_0_for_gte = count_for_0_for_gte + 1
            if gte_data[row][col] == 1:
                count_for_1_for_gte = count_for_1_for_gte + 1
        for row in range(len(lt_data)):
            if lt_data[row][col] == 0:
                count_for_0_for_lt = count_for_0_for_lt + 1
            if lt_data[row][col] == 1:
                count_for_1_for_lt = count_for_1_for_lt + 1

    #writing to output file
    writer.write("\n")
    writer.write("\t"*height)
    writer.write("if input_file[row][%d]  > %f :" %(column_index, threshold))

    #stopping criteria for recursion
    #if 95% of elements belong to class 0 then it is assigned as leaf node
    if float(count_for_0_for_gte) >= 0.95 * len(gte_data):
        writer.write("\n")
        writer.write("\t"*(height+1))
        writer.write("csvwriter.writerow('0')")

    #if 95% of elements belong to class 1 then it is assigned as leaf node
    elif float(count_for_1_for_gte) >= 0.95 * len(gte_data):
        writer.write("\n")
        writer.write("\t"*(height+1))
        writer.write("csvwriter.writerow('1')")

    #else recursively building the left subtree
    else:
        build_decision_tree(gte_data, height, writer)
    writer.write("\n")
    writer.write("\t"*(height))
    writer.write("else:")

    #if 95% of elements belong to class 0 then it is assigned as leaf node
    if float(count_for_0_for_lt) >= 0.95 * len(lt_data):
        writer.write("\n")
        writer.write("\t"*(height+1))
        writer.write("csvwriter.writerow('0')")

    #if 95% of elements belong to class 1 then it is assigned as leaf node
    elif float(count_for_1_for_lt) >= 0.95 * len(lt_data):
        writer.write("\n")
        writer.write("\t"*(height+1))
        writer.write("csvwriter.writerow('1')")

    else:
        #else recursively building the right subtree
        build_decision_tree(lt_data, height, writer)
    height = height - 1





def split_the_data(input_file, column_index, threshold):
    '''
    This function splits the attribute with minimum entropy
    according to threshold.
    :param input_file: training data on which decision tree is to be built
    :param column_index: the attribute with minimum entropy
    :param threshold: threshold of attribute with minimum entropy
    :return: left and right subsets
    '''
    gte_data = []
    lt_data = []

    #for every row, checking the value if it is greater than or less than
    #equal to threshold
    for row in range(len(input_file)):
        if input_file[row][column_index] > threshold:
            gte_data.append(input_file[row])
        if input_file[row][column_index] <= threshold:
            lt_data.append(input_file[row])
    return gte_data, lt_data


def calculate_mixed_entropy(input_file):
    '''
    This function calculates mixed entropy for every attribute and returns
    the one with minimum entropy along with its threshold.
    :param input_file: training data on which decision tree is to be built
    :return: the attribute with minimum entropy, its threshold and column number
    '''

    #initializing the entropy, column number and threshold
    min_entropy = float(999999999)
    min_index = 0
    threshold = 0

    #for every attribute
    for col_index in range(4):

        # getting a particular column and storing in a array
        temp_array = [ [(row[ci]) for ci in range(col_index, col_index+1)] for row in input_file ]

        # finding the unique values(thresholds) in retreived column to avoid excessive computations
        unique_array = numpy.unique(temp_array)

        # for every unique value in unique array
        for unique_index in range(len(unique_array)):
            #count of zeros and ones for the value which is less than equal to and greater than
            #the selected threshold
            count_of_0_for_gte = 0
            count_of_1_for_gte = 0
            count_of_0_for_lt = 0
            count_of_1_for_lt = 0

            # for every row in that column
            for row in range(0, len(input_file)):

                # checking if value in that row greater than the unique element in unique array
                if float(unique_array[unique_index]) > input_file[row][col_index]:

                    # checking the target variable i.e. 0 or 1 for that unique element and
                    # increasing the appropriate counter
                    if input_file[row][4] == float(0):
                        count_of_0_for_gte = count_of_0_for_gte + 1
                    if input_file[row][4] == float(1):
                        count_of_1_for_gte = count_of_1_for_gte + 1

                # checking if value in that row less than equal to the unique element in unique array
                if float(unique_array[unique_index]) <= input_file[row][col_index]:

                    # checking the target variable i.e. 0 or 1 for that unique element and
                    # increasing the appropriate counter
                    if input_file[row][4] == float(0):
                        count_of_0_for_lt = count_of_0_for_lt + 1
                    if input_file[row][4] == float(1):
                        count_of_1_for_lt = count_of_1_for_lt + 1

            #calculating weighted entropy
            if count_of_0_for_gte == 0 or count_of_1_for_gte == 0:
                gte_entropy = 0
            else:
                gte_entropy = (-((count_of_0_for_gte/(count_of_0_for_gte+count_of_1_for_gte)) * numpy.log2(count_of_0_for_gte/(count_of_0_for_gte+count_of_1_for_gte)))-\
                      ((count_of_1_for_gte/(count_of_0_for_gte+count_of_1_for_gte)) * numpy.log2(count_of_1_for_gte/(count_of_0_for_gte+count_of_1_for_gte))))
            weighted_gte_entropy = ((count_of_0_for_gte+count_of_1_for_gte)/(len(input_file)))* gte_entropy

            if count_of_0_for_lt == 0 or count_of_1_for_lt == 0:
                lte_entropy = 0
            else:
                lte_entropy = (-((count_of_0_for_lt/(count_of_0_for_lt+count_of_1_for_lt)) * numpy.log2(count_of_0_for_lt/(count_of_0_for_lt+count_of_1_for_lt)))-\
                      ((count_of_1_for_lt/(count_of_0_for_lt+count_of_1_for_lt)) * numpy.log2(count_of_1_for_lt/(count_of_0_for_lt+count_of_1_for_lt))))
            weighted_lte_entropy = ((count_of_0_for_lt+count_of_1_for_lt)/(len(input_file)))*lte_entropy

            weighted_entropy = weighted_gte_entropy + weighted_lte_entropy

            #finding out the element with minimum entropy, its column number and
            #setting that element as threshold
            if weighted_entropy <= min_entropy:
                min_entropy = weighted_entropy
                min_index = col_index
                threshold = float(unique_array[unique_index])

    return min_entropy, min_index, threshold

def emit_prologue(writer):
    '''
    This function writes header in output file
    :param writer: Object to write in file
    :return: None
    '''
    writer.write("import csv\n")

def emit_body(writer):
    '''
    This function writes the body of output file
    :param writer: Object to write in file
    :return: None
    '''

    #writing the main function and its contents
    writer.write("def main():\n")
    writer.write("\tinput_file = []\n")
    writer.write("\t#reading the validation file\n")
    writer.write("\twith open('HW_05B_DecTree_validation_data___v200.csv') as csvfile:\n")
    writer.write("\t\tattributes = csv.reader(csvfile)\n")
    writer.write("\t\tfor element in attributes:\n")
    writer.write("\t\t\tinput_file.append(','.join(element))\n")
    writer.write("\tfor index in range( len(input_file)):\n")
    writer.write("\t\tinput_file[index] = input_file[index].split(',')\n")
    writer.write("\tfor row in range(1, len(input_file)):\n")
    writer.write("\t\tfor col in range(0,4):\n")
    writer.write("\t\t\tinput_file[row][col] = float(input_file[row][col])\n")
    writer.write("\tinput_file.pop(0)\n")
    writer.write("\t#writing the classifications to output file as per the decision tree\n")
    writer.write("\twith open('HW_05B_Awghate_Vaibhavi_MyClassifications.csv','w',newline='') as csvfile1:\n")
    writer.write("\t\tcsvwriter = csv.writer(csvfile1)\n")
    writer.write("\t\tfor row in range(0, len(input_file)):")

    input_file = []
    #reads the csv file
    with open('HW_05BB_DecTree_Training__v200.csv') as csvfile:
        attributes = csv.reader(csvfile)
        for element in attributes:
            input_file.append(','.join(element))

    # converts it into 2D array
    for index in range( len(input_file)):
        input_file[index] = input_file[index].split(',')

    #converts into float
    for row in range(1, len(input_file)):
        for col in range(0,5):
            input_file[row][col] = float(input_file[row][col])

    input_file.pop(0)
    height = 2

    #function call to build decision tree
    build_decision_tree(input_file, height,writer)

def emit_epilogue(writer):
    '''
    This function calls the main function in output file
    :param writer: Object to write in file
    :return: None
    '''
    writer.write("\nmain()")


def main():
    '''
    this function makes all the function to write the output file
    :return:
    '''
    writer = open("HW_05B_Awghate_Vaibhavi_Classifier.py","w")
    emit_prologue(writer)
    emit_body(writer)
    emit_epilogue(writer)


main()