"""

IMAGE DOWNSIZING LOOP


Author: Ben Morrison


Description: This program takes a single image as input and outputs copies of
that image in a loop, downsizing the image by half each time. The loop ends when
an image is less than 20 in either row size or column size. Each downsized image
is centered vertically with the previous image, and the output image fills the
remaining space with black.

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys

#FUNCTIONS

"""
This recursive function takes in the original image and calculates how many times
the image will be downsized before row size < 20 or column size < 20.

It then preallocates an array of the correct size and fills the array with 0s.

The reason for doing this before the actual downsizing occurs is to ensure a more
efficient way of filling in the output image array. We can use indexing to set
the boundaries that we would like to fill, then fill those boundaries with the
downsized image. This prevents unneccesary copying of the image each time we
downsize.

"""
def getOutputImgSize(img, rows, cols, pic_counter):

    #State the base case

    if(img.shape[0] < 20 or img.shape[1] < 20):

        pic_counter-=1      #not including this pic, so subtract from counter
        cols-=img.shape[1]  #subtract this image from the column total

        #return the counter variable and the empty output image array
        return pic_counter, np.zeros((rows, cols,3))

    #Recursive loop

    #create downsized image by dividing each dimension by 2
    downsized_img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2),
    interpolation=cv2.INTER_AREA)
    cols+=downsized_img.shape[1] #add width of image to column total
    pic_counter+=1  #add to counter

    #call function again with downsized image as the input image
    return getOutputImgSize(downsized_img,rows,cols,pic_counter)

"""
This function takes in the current image and places it properly into the pre-made
array through the use of indexing. It returns the updated array at the end of
the function.

"""

def placeInArray(img, arr, col_current):
    #calculate upper and lower distances
    upper_bound = (arr.shape[0] - img.shape[0])//2
    lower_bound = upper_bound+img.shape[0]
    col_right_bound = col_current+img.shape[1]

    arr[upper_bound:lower_bound, col_current:col_right_bound] = img
    print("Copy starts at (", upper_bound, ", ",col_current,") image shape (",
    img.shape[0], ", ", img.shape[1], ", ", img.shape[2],")",sep="")

    return arr

#MAIN
if __name__ == '__main__':
    #Check for correct number of arguments
    if len(sys.argv) != 3:
        print("Invalid number of arguments!")
        sys.exit()

    #if correct, we must make sure each argument is valid. If not, exit program
    else:
        img_in = sys.argv[1]
        if img_in is None:
            print("Failed to open image", sys.argv[1])
            sys.exit()

        img_out = sys.argv[2]


    #READ IN IMAGE

    working_dir = os.getcwd()
    #path = working_dir + "/hw2_data_and_examples/" + img_in
    img = cv2.imread(img_in)
    rows = img.shape[0]
    cols = img.shape[1]
    pic_counter=1
    col = 0

    ##output image will be rowsxtotal_cols

    pic_counter, img_outline = getOutputImgSize(img, rows, cols, pic_counter)

    #looping through columns
    for i in range(0,pic_counter):
        img_outline = placeInArray(img, img_outline, col)
        col += img.shape[1]
        img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2),
        interpolation=cv2.INTER_AREA)

    print("Final shape (",img_outline.shape[0],", ",img_outline.shape[1],", ",
    img_outline.shape[2],")",sep="")

##    OUTPUT IMAGE

    #change the directory back to the original working directory
    #os.chdir(working_dir)
    #output the image under the name given in the command line argument
    cv2.imwrite(img_out, img_outline)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
