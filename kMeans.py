'''
Author: Vaibhavi Awghate
Email: vna4493@rit.edu
'''

import csv
import matplotlib.pyplot as plt
import random
import math
import numpy
import copy


def do_kMeans_clustering(input_file):
    '''
    This function performs k-means clustering.
    :param input_file: Input data
    :return:None
    '''

    #array for sum of squared error
    sse_list = []

    # for number of clusters 2 to 10
    for k in range(2,11):
        random_points = []
        new_centroids = []
        clusters = []
        index = 0
        #selecting initial seed points
        while(index != k):
            temp_random = random.choice(input_file)
            random_points.append(temp_random)
            clusters.append([])
            new_centroids.append([0,0,0])
            index = index + 1

        #stopping criteria
        while (random_points != new_centroids):

            #calculating euclidean distance for every record from seed points
            for outer_row in range(len(input_file)):
                a = input_file[outer_row]
                temp = float(999999)
                for inner_row in range(len(random_points)):
                    b = random_points[inner_row]
                    dist = [(x - y)**2 for x, y in zip(a, b)]
                    dist = math.sqrt(sum(dist))

                    #selecting the minimum one
                    if(dist <= temp):
                        temp = dist
                        temp_b = inner_row

                #forming clusters
                clusters[temp_b].append(outer_row)

            #copying new centroids to older ones
            random_points = copy.deepcopy(new_centroids)

            # computing new centroids
            new_centroids = []
            for row in clusters:
                temp_array = []
                for element in row:
                    temp_array.append(input_file[element])
                new_centroids.append(calculate_centre_of_mass(temp_array))

            #rounding off to 2 decimals
            for index_i in range(0,k):
                for index_j in range(3):
                    new_centroids[index_i][index_j] = round(new_centroids[index_i][index_j],2)

        #calculating SSE for k clusters
        sse = calculate_SSE(input_file, clusters, random_points)
        sse_list.append(sse)

        #plotting each cluster with different colors
        colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'black', 'gray', 'brown', 'orange', 'pink', 'cyan']
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        index = 0
        for row in clusters:
            c = colors[index]
            for element in row:
                xs = input_file[element][0]
                ys = input_file[element][1]
                zs = input_file[element][2]
                ax.scatter(xs, ys, zs, color=c )
            index = index +1
        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()

    #plotting k versus SSE
    plt.plot(range(2,11),sse_list)
    plt.show()




def calculate_SSE(input_file, clusters, random_points):
    '''
    This funtion calculates sum of squared error
    :param input_file: input data
    :param clusters: clusters list
    :param random_points: centroids
    :return: euclidean_distance: sum of squared error
    '''
    index = 0
    euclidean_distance = 0
    for row in clusters:
        temp_array = []
        for element in row:
            temp_array.append(input_file[element])
        for row_element in temp_array:
            dist = [(x - y)**2 for x, y in zip(row_element, random_points[index])]
            dist = (sum(dist))
            euclidean_distance = euclidean_distance + dist
        index = index + 1
    return euclidean_distance


def calculate_centre_of_mass(temp_array):
    '''
    This function computes the new centroids for given cluster.
    :param temp_array: input data
    :return: new centroids
    '''
    return ((numpy.mean(temp_array, axis=0)).tolist())

def main():
    '''
    The main function
    :return: None
    '''
    input_file = []
    #reads the csv file
    with open('HW08_KMEANS_DATA_v300.csv') as csvfile:
        attributes = csv.reader(csvfile)
        for element in attributes:
            input_file.append(','.join(element))

    # converts it into 2D array
    for index in range( len(input_file)):
        input_file[index] = input_file[index].split(',')

    #converts into float
    for row in range(1, len(input_file)):
        for col in range(0,3):
            input_file[row][col] = float(input_file[row][col])

    #replaces values less than 0 by 0
    for row in range(1, len(input_file)):
        for col in range(0,3):
            if input_file[row][col] < 0:
                input_file[row][col] = 0

    input_file.pop(0)

    do_kMeans_clustering(input_file)



main()
