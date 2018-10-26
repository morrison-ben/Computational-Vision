"""

HW 3 PROBLEM 1

Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys
import math



#MAIN
if __name__ == '__main__':

    ##COMMAND LINE ARGS
    if len(sys.argv) != 3:
        print("Invalid number of arguments!")
        sys.exit()

    #if correct, we must make sure each argument is valid. If not, exit program
    else:
        param_file = sys.argv[1]
        if param_file is None:
            print("Failed to open text file:", sys.argv[1])
            sys.exit()

        pnt_file = sys.argv[2]
        if pnt_file is None:
            print("Failed to open text file:", sys.argv[2])
            sys.exit()



    #PARSE THE PARAM FILE, SET VARIABLES

    x=0
    for line in open(param_file, 'r'):
        coord = line.split()
        if (x==0):
            rx, ry, rz = float(coord[0]),float(coord[1]), float(coord[2])
        if (x==1):
            tx, ty, tz = float(coord[0]),float(coord[1]), float(coord[2])
        if (x==2):
            f = float(coord[0])
            d = float(coord[1])
            ic = float(coord[2])
            jc = float(coord[3])

        x+=1


    #can be used to disable scientific notation printing style
    #for numpy arrays:

    # np.set_printoptions(suppress=True,
    # formatter={'float_kind':'{:0.2f}'.format})


    #FINDING R



    #Create the three rotational matrices

    #Rx matrix
    rx = np.radians(rx)
    rx_matrix = np.array([1,0,0,0,math.cos(rx),-1*(math.sin(rx)),
    0,math.sin(rx),math.cos(rx)]).reshape(3,3)


    #Ry matrix
    ry = np.radians(ry)
    ry_matrix = np.array([math.cos(ry),0,math.sin(ry),0,1,0,-1*(math.sin(ry)),
    0,math.cos(ry)]).reshape(3,3)


    #Rz matrix
    rz = np.radians(rz)
    rz_matrix = np.array([math.cos(rz),-1*(math.sin(rz)),0,math.sin(rz),
    math.cos(rz),0,0,0,1]).reshape(3,3)


    #multiply the three matrices together to find R
    rx_ry_matrix = np.dot(rx_matrix,ry_matrix)
    r_matrix = np.dot(rx_ry_matrix, rz_matrix)



    #FINDING K

    #take the equation sx = sy = f/d --> convert d from microns to mm
    sx = f / float(d/1000)
    sy = sx
    k_matrix = np.array([sx,0,ic,0,sy,jc,0,0,1]).reshape(3,3)


    #SOLVE FOR CAMERA MATRIX M


    #Create column array t

    t = np.array([tx,ty,tz])
    t_matrix = t.reshape(3,1)

    #set a variable for R^T
    r_matrix_t = np.transpose(r_matrix)

    #multiply transposed r by the column vector t
    col_four = np.dot(r_matrix_t, -1*t_matrix)

    #concatenate onto matrix
    r_mat_transpose = np.concatenate((r_matrix_t,col_four),axis=1)

    #calculate 3*4 matrix
    m = np.dot(k_matrix,r_mat_transpose)
    # m = np.round(m, 2)
    # print(m)

    #print matrix M
    print("Matrix M:")
    col_ctr = 0
    for val in np.nditer(m):
        print("{0:.2f}".format(val), end=" ")
        col_ctr+=1
        #if last column reached, start a new line, reset columns to 0
        if (col_ctr==m.shape[1]):
            print()
            col_ctr = 0


    #PARSING POINT FILE

    i = 0
    visible = []
    hidden = []
    for line in open(pnt_file, 'r'):
        coord = line.split()

        x, y, z = float(coord[0]),float(coord[1]),float(coord[2])
        p = np.array([x,y,z,1]).reshape(4,1)

        i+=1
