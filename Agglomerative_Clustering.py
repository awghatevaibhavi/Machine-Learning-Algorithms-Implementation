'''
Author: Vaibhavi Awghate
Email: vna4493@rit.edu
'''
import csv
import math
def do_agglomerative_clustering(file):
    '''
    This function implements agglomerative clustering.
    :param file: Input file
    :return: None
    '''
    input_file = file

    #2D array to keep track of cluster IDs
    clusters = []

    #Initially, there are 100 clusters each containing its own cluster ID
    temp_array = [ [(row[ci]) for ci in range(0, 1)] for row in input_file ]
    for element in temp_array:
        clusters.append(element)

    #labeles are removed
    clusters.pop(0)
    input_file.pop(0)

    #loop till one big cluster is formed
    while(len(input_file)>1):
        temp = float(9999999)

        #euclidean distance is calculated between each and every record.
        for outer_row in input_file:
            a = outer_row[1:]
            for inner_row in input_file:
                if outer_row[0] != inner_row[0]:
                    b = inner_row[1:]

                    #formula for euclidean distance
                    dist = [(x - y)**2 for x, y in zip(a, b)]
                    dist = math.sqrt(sum(dist))

                    #retrieving the minimum one and IDs of two records
                    if(dist < temp):
                        temp = dist
                        min_element = outer_row[0]
                        max_element = inner_row[0]

        #function call to build clusters and to calculate centre of mass
        input_file, clusters = build_clusters_and_calculate_centre_of_mass(input_file, clusters, min_element, max_element)


def build_clusters_and_calculate_centre_of_mass(input_file, clusters, min_element, max_element):
    '''
    This function builds clusters and calculates centre of mass.
    :param input_file: Input file
    :param clusters: 2D cluster ID array
    :param min_element: ID which is smaller between two IDs of records with shortest distance.
    :param max_element: ID which is larger between two IDs of records with shortest distance.
    :return: input_file: transformed input file
    :return: clusters: transformed 2D cluster array
    '''
    centre_of_mass = input_file

    #Retrieved ID are searched in clusters array and its index is returned
    for outer_row in range(len(clusters)):
        for element in clusters[outer_row]:
            if min_element == element:
                index1 = outer_row
            if max_element == element:
                index2 = outer_row

    #Calculating weighted average for centre of mass and changing the record with smaller ID with center of mass and
    #deleting the record with bigger ID
    for index in range(1, len(input_file[0])):
        centre_of_mass[index1][index] = len(clusters[index1])* centre_of_mass[index1][index]
        centre_of_mass[index2][index] = len(clusters[index2])* centre_of_mass[index2][index]

    for index in range(1, len(input_file[0])):
        centre_of_mass[index1][index] = float((centre_of_mass[index1][index]+centre_of_mass[index2][index])/(len(clusters[index1])+len(clusters[index2])))

    #the clusters are merged here
    for element in clusters[index2]:
        clusters[index1].append(element)

    #the records with bigger ID are deleted
    clusters.pop(index2)
    centre_of_mass.pop(index2)

    print("clusters when length of cluster ID array is: ", len(clusters) )
    print(clusters)

    #changed input file and clusters array are returned
    return centre_of_mass, clusters

def main():
    '''
    The main function
    :return: None
    '''
    input_file = []
    #reads the csv file
    with open('HW_07_SHOPPING_CART_v137.csv') as csvfile:
        attributes = csv.reader(csvfile)
        for element in attributes:
            input_file.append(','.join(element))

    # converts it into 2D array
    for index in range( len(input_file)):
        input_file[index] = input_file[index].split(',')

    #converts into int
    for row in range(1, len(input_file)):
        for col in range(0,13):
            input_file[row][col] = int(input_file[row][col])

    #function call to agglomerative clustering
    do_agglomerative_clustering(input_file)

#call to main function
main()