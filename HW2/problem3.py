"""

LINEAR ALGEBRA GIVEN A SET OF POINTS

Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys
from numpy.linalg import svd
import numpy.linalg as lin
import math

#FUNCTIONS

def findMinAndMax(min, max, point):
    if (point > max):
        max = point
    if (min == 0):
        min = point
    elif (point < min):
        min = point

    return min, max


def findCOM(x_vals, y_vals):
    x_com = np.sum(x_vals)/x_vals.size
    y_com = np.sum(y_vals)/y_vals.size

    return x_com, y_com


#MAIN
if __name__ == '__main__':

    ##COMMAND LINE ARGS
    if len(sys.argv) != 4:
        print("Invalid number of arguments!")
        sys.exit()

    #if correct, we must make sure each argument is valid. If not, exit program
    else:
        pnt_file = sys.argv[1]
        if pnt_file is None:
            print("Failed to open text file:", sys.argv[1])
            sys.exit()

        tau = float(sys.argv[2])
        if not isinstance(tau, float):
            print("Tau needs to be a float value, ",
            sys.argv[2], " is not a float value.")
            sys.exit()

        plot_out = sys.argv[3]


    #working_dir = os.getcwd()
    #path = working_dir + "/hw2_data_and_examples/" + pnt_file

    x_min_val = 0.0
    x_max_val = 0.0
    y_min_val = 0.0
    y_max_val = 0.0
    x_vals = []
    y_vals = []
    #parse text file
    for line in open(pnt_file, 'r'):
        coord = line.split()
        x,y = float(coord[0]), float(coord[1])
        x_min_val, x_max_val = findMinAndMax(x_min_val, x_max_val, x)
        y_min_val, y_max_val = findMinAndMax(y_min_val, y_max_val, y)

        x_vals.append(x)
        y_vals.append(y)

    print("min: ({0:.3f}".format(x_min_val),", {0:.3f}".format(y_min_val),")",sep="")
    print("max: ({0:.3f}".format(x_max_val),", {0:.3f}".format(y_max_val),")",sep="")

    x_arr = np.array(x_vals)
    y_arr = np.array(y_vals)
    com_x, com_y = findCOM(x_arr,y_arr)
    print("com: ({0:.3f}".format(com_x),", {0:.3f}".format(com_y),")",sep="")

    x_vals = [x - com_x for x in x_vals]

    y_vals = [y - com_y for y in y_vals]

    new_x_arr = np.array(x_vals)
    new_y_arr = np.array(y_vals)

    a = np.matrix([x_vals, y_vals]).transpose()
    u, s, vh = np.linalg.svd(a, full_matrices=True)

    min_x, min_y = -1*(vh[1,0]), -1*(vh[1,1])
    max_x, max_y = vh[0,0], vh[0,1]

    print("min axis: ({0:.3f}".format(min_x),",{0:.3f}".format(min_y),")",sep="")
    print("max axis: ({0:.3f}".format(max_x),",{0:.3f}".format(max_y),")",sep="")

    w, v = lin.eigh(vh)

    #multiply bottom row * w[0], that's min axis point
    #multiply top row * w[1], that's max axis point

    theta = np.arctan2(max_x, min_x)

    rho = com_x*math.cos(theta) + com_y*math.sin(theta)

    print("closest point: rho {0:.3f}".format(rho),", theta {0:.3f}".format(theta), sep="")

    print("implicit: a {0:.3f}".format(min_x),", b {0:.3f}".format(max_x),
     ", c {0:.3f}".format(-1*rho), sep="")

    # print(np.std(new_x_arr))
    # print(np.std(new_y_arr))
