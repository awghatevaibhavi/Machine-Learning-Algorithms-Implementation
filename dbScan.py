__author__ = 'Vaibhavi'
import math
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy

def generate_graph(input_file):
    for k in range(1,11):
        sorted_distance_list = []

        #for each star
        for outer_row in input_file:
            distance_list = []
            a = outer_row

            #to every other star
            for inner_row in input_file:
                b = inner_row

                #calculate euclidean distance
                dist = [(x - y)**2 for x, y in zip(a, b)]
                dist = math.sqrt(sum(dist))
                distance_list.append(dist)

            #distance list is sorted to get kth nearest neighbor
            distance_list.sort()
            sorted_distance_list.append(distance_list[k])

        #for every star, kth nearest neighbor distance is sorted
        # to generate the plot
        sorted_distance_list.sort()

        plt.plot(range(len(input_file)), sorted_distance_list)

    plt.show()

def dbscan(input_file, eps, minpts):
    '''
    This function performs dbScan algorithm.
    :param input_file: input file
    :param eps: epsilon distance
    :param minpts: minimum points in cluster
    :return:
    '''
    C=-1
    visited = []
    NOISE = []
    clusters = []

    #for every star, get the stars within eps
    for row in range(len(input_file)):

        #to make sure a star is not added twice
        if row not in visited:
            visited.append(row)

            #get points within eps
            neighbors = getClosePoints(input_file[row], input_file, eps)

            #if the length of neighbors is greater than or equal to minimum points
            if len(neighbors) >= minpts:

                #the neighbors are appended to next cluster
                clusters.append([])
                C += 1

                #to get all the connected stars
                getMoreCloserPoints (row, neighbors, clusters, C, eps, minpts, visited, input_file)


            else:
                # any cluster whose size is less than 6 are considered to be noise
                NOISE.append(row)
        else:

            #if the star is already visited, we ignore that star
            continue

    #calculating centre of mass for each cluster
    for index in range(len(clusters)):
        print(len(clusters[index]), " ", calculate_centre_of_mass(input_file, clusters[index]))

    print("Estimated number of noise datapoints: ", len(NOISE))
    #scatter plot of each cluster with different colors
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

def calculate_centre_of_mass(input_file, data):
    '''
    This function calculates centre of mass for each cluster
    :param input_file: input file
    :param data: cluster points
    :return: centre of mass for each cluster
    '''
    data_list =[]
    for element in data:
        data_list.append(input_file[element])
    return ((numpy.mean(data_list, axis=0)).tolist())

def getMoreCloserPoints (row, neighbors, clusters, C, eps, minpts, visited, input_file):
    '''
    This function collects all the connected components.
    :param row: current star
    :param neighbors: close stars to current
    :param clusters: clusters list
    :param C: cluster index
    :param eps: epsilon distance
    :param minpts: minimum points in the cluster
    :param visited: list of visited star
    :param input_file: input file
    :return: None
    '''

    #current star is added to current cluster
    clusters[C].append(row)

    #for every element in close stars list
    for neighbor in neighbors:

        #if that element is not already visted
        if neighbor not in visited:
            visited.append(neighbor)

            #get close points for the current element
            __neighbors = getClosePoints(input_file[neighbor], input_file, eps)

            #if the length of neighbors is greater than or equal to minimum points
            if len(__neighbors) >= minpts:
                for element in __neighbors:
                    if element not in neighbors:

                        #all the close points are added to neighbors list of current star
                        neighbors.append(element)

        #if current element is not in any cluster, we add to current cluster
        if neighbor not in (i for i in clusters):
            clusters[C].append(neighbor)



def getClosePoints(current_row, input_file, eps):
    '''
    This function gets all the points which are within eps to current star.
    :param current_row: current star
    :param input_file: input file
    :param eps: epsilon distance
    :return: close_points: all the close points
    '''
    close_points = []

    # for every other star
    for row in range(len(input_file)):

        #calculate euclidean distance
        dist = [(x - y)**2 for x, y in zip(current_row, input_file[row])]
        dist = math.sqrt(sum(dist))

        #if the computed distance is less than eps
        if dist < eps:

            #that point is added to close points list
            close_points.append(row)
    return close_points

def main():
    '''
    The main function
    :return: None
    '''
    input_file = []
    #reads the csv file
    with open('HW_08_DBScan_Data_NOISY_v300.csv') as csvfile:
        attributes = csv.reader(csvfile)
        for element in attributes:
            input_file.append(','.join(element))

    # converts it into 2D array
    for index in range( len(input_file)):
        input_file[index] = input_file[index].split(',')

    #converts into float
    for row in range(0, len(input_file)):
        for col in range(0,3):
            input_file[row][col] = float(input_file[row][col])

    #generates graph to get eps
    generate_graph(input_file)
    eps = 0.7
    minpts = 6

    #dbScan algorithm
    dbscan(input_file, eps, minpts)


main()