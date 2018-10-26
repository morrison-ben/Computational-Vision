"""

IMAGE MANIPULATION


Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys

##FUNCTIONS

"""
This function is used to create the distance arrays for the
left, right, top, and bottom shading directions.
"""

def createDistanceArrays(dir, rows, cols, img):
    if (dir == "left"):
        row_array = np.arange(cols)
        two_d = np.tile(row_array, (rows, 1))
        return two_d

    if (dir == "right"):
        temp = np.arange(cols)
        row_array = np.flip(temp,0)
        two_d = np.tile(row_array, (rows, 1))
        return two_d

    if (dir == "top"):
        col_array = np.arange(rows).reshape(rows, 1)
        two_d = np.tile(col_array, cols)
        return two_d

    if (dir == "bottom"):
        temp = np.arange(rows).reshape(rows, 1)
        col_array = np.flip(temp,0)
        two_d = np.tile(col_array, cols)
        return two_d

"""
This function is used to create the distance array for the
center shading direction.
"""

def createCenterArray(rows, cols, img):

    #creating x array

    #if even number of columns, set up so that there is only one 0 value
    #that represents the starting point of center shading
    if cols % 2 == 0:
        xtemp_left = np.arange(cols//2+1)
        xtemp_left = np.flip(xtemp_left, 0)
        xtemp_right = np.arange(cols//2)
        xtemp_right = xtemp_right[1:]

    #if odd number of columns, set up accordingly
    else:
        xtemp_right = np.arange((cols//2)+1)
        xtemp_left = np.flip(xtemp_left, 0)
        xtemp_right = xtemp_right[1:]

    #merge the left and right arrays
    xtemp = np.concatenate((xtemp_left, xtemp_right))

    #tile down for each row to create a 2d array
    x_two_d = np.tile(xtemp, (rows, 1))


    #creating y array

    #same procedure as x array
    if rows % 2 == 0:
        ytemp_top = np.arange(rows//2+1).reshape(rows//2+1,1)
        ytemp_top = np.flip(ytemp_top, 0) #540 items, (540-0)
        ytemp_bottom = np.arange(rows//2).reshape(rows//2,1)
        ytemp_bottom = ytemp_bottom[1:]
    else:
        ytemp_bottom = np.arange((rows//2)+1).reshape((rows//2)+1, 1)
        ytemp_top = np.flip(ytemp_top, 0)
        ytemp_bottom = ytemp_bottom[1:]

    #merge the two arrays
    ytemp = np.concatenate((ytemp_top, ytemp_bottom), axis=0)

    #tile across to make 2d array
    y_two_d = np.tile(ytemp, cols)

    #calculate distance at each point using sqrt(x^2 + y^2)
    #store these values in a new array
    two_d = np.sqrt(np.add(np.square(x_two_d), np.square(y_two_d)))


    return two_d


#MAIN

if __name__ == '__main__':

    #Check for correct number of arguments
    if len(sys.argv) != 4:
        print("Invalid number of arguments!")
        sys.exit()

    #if correct, we must make sure each argument is valid. If not, exit program
    else:
        img_name = sys.argv[1]
        if img_name is None:
            print("Failed to open image", sys.argv[1])
            sys.exit()

        output_img = sys.argv[2]

        dir = sys.argv[3]
        if dir not in ['left', 'right', 'top', 'bottom', 'center']:
            print(sys.argv[3], "is an invalid direction.")
            sys.exit()


    #READ IN IMAGE

    img = cv2.imread(img_name)
    rows = img.shape[0]
    cols = img.shape[1]

    if dir == "center":
        two_d = createCenterArray(rows, cols, img)

    else:
        two_d = createDistanceArrays(dir, rows, cols, img)

    #normalize array
    two_d_max, two_d_min = two_d.max(), two_d.min()
    two_d = (two_d - two_d_min)/(two_d_max - two_d_min)

    #subtract values from 1 to get multiplier array
    two_d = np.subtract(1,two_d)

    #reshape the array into 3 dimensions
    two_d = two_d.reshape(rows, cols, 1)


    #multiply the 3d multiplier array by the 3d image array to produce
    #a new array representing the shaded image
    arr = np.multiply(img, two_d)


    #print the 9 multiplier values
    print("(0,0) {0:.3f}".format(two_d[0,0][0]),sep="")
    print("(0,",cols//2,") {0:.3f}".format(two_d[0,cols//2][0]),sep="")
    print("(0,",cols-1,") {0:.3f}".format(two_d[0,cols-1][0]), sep="")
    print("(",rows//2,",0) {0:.3f}".format(two_d[rows//2,0][0]), sep="")
    print("(",rows//2,",",cols//2,") {0:.3f}".format(two_d[rows//2,cols//2][0]), sep="")
    print("(",rows//2,",",cols-1,") {0:.3f}".format(two_d[rows//2,cols-1][0]), sep="")
    print("(",rows-1,",0) {0:.3f}".format(two_d[rows-1,0][0]), sep="")
    print("(",rows-1,",",cols//2,") {0:.3f}".format(two_d[rows-1,cols//2][0]), sep="")
    print("(",rows-1,",",cols-1,") {0:.3f}".format(two_d[rows-1, cols-1][0]), sep="")


    #OUTPUT IMAGE

    cv2.imwrite(output_img, arr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
