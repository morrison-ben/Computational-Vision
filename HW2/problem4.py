"""

LINEAR ALGEBRA GIVEN A SET OF POINTS

Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys

#FUNCTIONS

def ransac(kmax, theta, rho, sx, sy, tau):


#MAIN
if __name__ == '__main__':
    ##COMMAND LINE ARGS
    if (len(sys.argv) != 4 and len(sys.argv) != 5):
        print("Invalid number of arguments!")
        sys.exit()

    if (len(sys.argv) == 5):
        #seed is true
        np.random.seed(sys.argv[4])
    else:
        pnt_file = sys.argv[1]
        if pnt_file is None:
            print("Failed to open text file:", sys.argv[1])
            sys.exit()

        samples = int(sys.argv[2])
        if not isinstance(samples, int):
            print("Tau needs to be an int value, ",
            sys.argv[2], " is not an int value.")
            sys.exit()

        tau = float(sys.argv[3])
        if not isinstance(tau, float):
            print("Tau needs to be a float value, ",
            sys.argv[3], " is not a float value.")
            sys.exit()


    #do stuff

    #read in text file, save as numpy array
    # working_dir = os.getcwd()
    # path = working_dir + "/hw2_data_and_examples/" + pnt_file

    x_vals = []
    y_vals = []

    for line in open(pnt_file, 'r'):
        coord = line.split()
        x,y = float(coord[0]), float(coord[1])
        if (len(x_vals) == 0):
            sample_x = x

        x_vals.append(x)
        if (len(y_vals)==0):
            sample_y = y
        y_vals.append(y)

    x_arr = np.array(x_vals)
    y_arr = np.array(y_vals)

    a = np.matrix([x_vals, y_vals]).transpose()
    kmax = 0
    for (x in range(0,samples)):
        s_x, s_y = np.random.randint(0, a.shape[0], 2)
        if (s_x != s_y):
            #generate line
            slope = (sample_y - s_y) / (sample_x - s_x)

            #find a, b, c using ax+by+c = 0
            a = sample_x - s_x
            b = sample_y - s_y

            c = (a*sample_x + b*sample_y)*-1

            #convert to polar

            theta = arccos(a)
            rho = c*-1

            #run ransac
            k = ransac(kmax, theta, rho, s_x, s_y, tau)
            if (k > kmax):
                kmax = k
                print("Sample ",x,":")
                print("indices (",s_x,", ",s_y,")",sep="")
                print("line ({0:.3f}".format(a),",{0:.3f}".format(b),
                ",{0:.3f}".format(c),")",sep="")
                #print ("inliers ",inliers)
