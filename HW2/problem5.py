"""

DETERMINING BEST IMAGE FOCUS


Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys
import math

#FUNCTIONS

def getImages(dir):
    #change the directory to the one given in the command line input
    os.chdir(dir)
    #produce a sorted list of images
    img_list = sorted(os.listdir('./'))
    img_list = [name for name in img_list if 'jpg' in name.lower()]
    return img_list


#MAIN
if __name__ == '__main__':

    #COMMAND LINE ARGS
    if len(sys.argv) != 2:
        print("Incorrect number of arguments!")
        sys.exit()

    #save working directory as variable, used when outputting image
    working_dir = os.getcwd()

    if os.path.isdir(sys.argv[1]):
        image_dir = sys.argv[1]
    else:
        print(sys.argv[1], "is an invalid directory.")
        sys.exit()

    list_of_images = getImages(image_dir)
    #sort image list
    list_of_images.sort()
    ##int ddepth = CV_16S;
    best_focused = 0
    ctr = 0
    best_focused_name=""
    for img in list_of_images:
        #load in as grayscale image
        img = cv2.imread(img, 0)
        grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, 3)
        grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, 3)


        #loop through grad_x and grad_y
        #at each pixel, add x_value^2 + y_value^2
        #when loop is done, divide by MN

        energy = (np.sum(grad_x**2) + np.sum(grad_y**2)) / (img.shape[0]*img.shape[1])

        if energy > best_focused:
            best_focused = energy
            best_focused_name = list_of_images[ctr]

        print(list_of_images[ctr], ": {0:.2f}".format(energy))

        ctr+=1


    print("Image ",best_focused_name, " is best focused.",sep="")
