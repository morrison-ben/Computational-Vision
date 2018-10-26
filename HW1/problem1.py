"""

FORM A BLOCK IMAGE IN TWO STAGES


Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys
import math

##FUNCTIONS

"""
This function is used to find the average intensity within a certain
#boundary, with the boundary representing one pixel in the downsized image
"""
def findBlockVal(i,j,row_scale,col_scale,img):

    #get upper and lower bounds
    i_lb = math.floor(i*sm)
    i_ub = math.floor((i+1)*sm)     #+1 for inclusive, cancels out -1
    j_lb = math.floor(j*sn)
    j_ub = math.floor((j+1)*sn)     #+1 for inclusive, cancels out -1

    #create a temporary array by indexing part of the image
    temp = img[i_lb:i_ub, j_lb:j_ub]

    #return average intensity of the indexed section
    return np.average(temp)


##MAIN

if __name__ == "__main__":

    #Check for correct number of arguments
    if len(sys.argv) != 5:
        print("Incorrect number of arguments!")
        sys.exit()

    #if correct, we must make sure each argument is valid. If not, exit program
    else:
        img_name = sys.argv[1]
        if img_name is None:
            print("Failed to open image", sys.argv[1])
            sys.exit()

        rows = int(sys.argv[2])
        if not isinstance(rows, int):
            print("Number of rows needs to be an integer, ",
            sys.argv[2], " is not an integer.")
            sys.exit()

        columns = int(sys.argv[3])
        if not isinstance(columns, int):
            print("Number of columns needs to be an integer, ",
            sys.argv[3], " is not an integer.")
            sys.exit()

        blck_size = int(sys.argv[4])
        if not isinstance(blck_size, int):
            print("Block size needs to be an integer, ",
            sys.argv[4], " is not an integer.")
            sys.exit()


    #load in as grayscale image
    img = cv2.imread(img_name, 0)

    print("Downsized images are (", rows, ", ", columns, ")", sep="")
    print("Block images are (", rows*blck_size, ", ", columns*blck_size, ")", sep="")

    #create scale factors --> sm = M/m, sn = N/n
    sm = img.shape[0]/rows
    sn = img.shape[1]/columns


    ##GRAYSCALE IMAGE


    #setting up variables for while loop
    i=0
    j=0
    avg_blocks = np.zeros((rows,columns))

    while (i < rows):
        while (j < columns):
            avg_int = findBlockVal(i, j, sm, sn, img)
            avg_blocks[i,j] = avg_int
            j+=1

        i+=1
        j=0       #reset column to 0 when a new row is reached


    #compute and print average intensities at downsized pixels
    print("Average intensity at (",rows//4, ", ",columns//4,") is {0:.2f}".
    format(avg_blocks[rows//4, columns//4]), sep="")
    print("Average intensity at (",rows//4, ", ",3*columns//4,") is {0:.2f}".
    format(avg_blocks[rows//4, 3*columns//4]), sep="")
    print("Average intensity at (",3*rows//4, ", ",columns//4,") is {0:.2f}".
    format(avg_blocks[3*rows//4, columns//4]), sep="")
    print("Average intensity at (",3*rows//4, ", ",3*columns//4,") is {0:.2f}".
    format(avg_blocks[3*rows//4, 3*columns//4]), sep="")



    ##BINARY IMAGE


    #find the median of the numpy array, set as threshold
    thresh = np.median(avg_blocks)
    print("Binary threshold: {0:.2f}".format(thresh), sep="")

    #make a copy of the array, setting val to 0 where val < thresh
    #and otherwise setting val to 255
    avg_binary = avg_blocks.copy()
    avg_binary[avg_binary < thresh] = 0
    avg_binary[avg_binary > thresh] = 255

    #convert avg_blocks vals to ints by rounding
    avg_blocks_int = avg_blocks.astype(int)


    #OUTPUT THE IMAGES

    img_title, img_ext = os.path.splitext(img_name)
    gray_name = img_title + '_g' + img_ext
    cv2.imwrite(gray_name, avg_blocks_int)
    print("Wrote image", gray_name)
    bin_name = img_title + '_b' + img_ext
    cv2.imwrite(bin_name, avg_binary)
    print("Wrote image", bin_name)
