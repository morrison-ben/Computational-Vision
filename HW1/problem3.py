"""

CHECKERBOARD


Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys

#FUNCTIONS

"""
Calculates the magnitude of a 3D vector
"""
def magnitude(i_list):
    return (i_list[0]**2 + i_list[1]**2 + i_list[2]**2) ** 0.5

"""
Calculates the distance between two 3D vectors
"""
def distance(i_list_one, i_list_two):
    return ((i_list_one[0]-i_list_two[0])**2 + (i_list_one[1]-i_list_two[1])**2
     + (i_list_one[2]-i_list_two[2])**2) ** 0.5

"""
This function is used to find the mean intensity values for each color in
an image. It does this by separating the colors into 3 arrays, then using
the built-in numpy mean function to find the mean intensity of each color
"""
def getVec(img_name):
    img = cv2.imread(img_name)
    red = img[:,:,2]
    green = img[:,:,1]      #account for BGR
    blue = img[:,:,0]

    red_mean = np.mean(red)
    green_mean = np.mean(green)     #find the mean value for each color
    blue_mean = np.mean(blue)

    #return mean values as a list in RGB order
    return [red_mean, green_mean, blue_mean]

"""
This function is used to determine how many images are in the given directory.
It returns img1 and img2, which are needed for the checkerboard function so
we know what images to use for the output.

"""
def getImages(dir, square_size):
    #change the directory to the one given in the command line input
    os.chdir(dir)
    #produce a sorted list of images
    img_list = sorted(os.listdir('./'))
    img_list = [name for name in img_list if 'jpg' in name.lower()]

    #CASE 1: NO IMAGES

    if(len(img_list) == 0):
        print("No images. Creating an ordinary checkerboard.")
        img1 = np.empty((square_size, square_size,1))
        img1.fill(255)  #all white
        img2 = np.zeros((square_size,square_size,1))    #all black

        return img1, img2

    #CASE 2: ONE IMAGE

    elif(len(img_list) == 1):
        img1 = cv2.imread(img_list[0])  #image in folder
        img2 = np.zeros((square_size, square_size,3))   #all black
        print("One image: ",img_list[0],". It will form the white square.", sep="")
        return img1, img2


    #CASE 3: TWO IMAGES

    elif(len(img_list) == 2):
        img1 = cv2.imread(img_list[0])  #first image in folder
        img2 = cv2.imread(img_list[1])  #second image in folder
        print("Exactly two images: ",img_list[0]," and ", img_list[1],
        ". Creating checkerboard from these.", sep="")
        return img1, img2

    #CASE 4: MORE THAN TWO IMAGES

    else:
        #loop through image list, get the mean intensity vectors for each image
        vec_list = []
        for img in img_list:
            i_list = getVec(img)
            print(img, " ({0:.1f}".format(i_list[0]), ", {0:.1f}".format(i_list[1]),
            ", {0:.1f}".format(i_list[2]),")",sep="")
            #push vector to list
            vec_list.append(i_list)

        #max_dist originally gets set to dist(vec_list[0], vec_list[1])
        #img1 and img2 are the first 2 images, by default

        max_dist = distance(vec_list[0], vec_list[1])
        img1_name = img_list[0]
        img2_name = img_list[1]

        #set original variables - j is always 1 greater than i
        i=0
        j=1
        while i < len(vec_list)-1:
            while j < len(vec_list):
                current_dist = distance(vec_list[i], vec_list[j])
                #if current distance is larger than the previous max, set new
                #variables
                if current_dist > max_dist:
                    max_dist = current_dist
                    #setting img1 and img2 based on magnitude
                    img1_name = img_list[i]
                    img2_name = img_list[j]
                    if magnitude(vec_list[j]) > magnitude(vec_list[i]):
                        img1_name = img_list[j]
                        img2_name = img_list[i]
                    else:
                        img1_name = img_list[i]
                        img2_name = img_list[j]
                #increment j until end of while loop
                j+=1
            #move i to next image, set j to image after that one
            i+=1
            j=i+1

        print("Checkerboard from ",img1_name," and ",img2_name,
        ". Distance between them is {0:.1f}".format(max_dist),sep="")
        img1 = cv2.imread(img1_name)
        img2 = cv2.imread(img2_name)
        return img1, img2


"""
This function takes in an image and returns a new one with square dimensions.

"""

def crop(img):
    #total difference between dimension vals
    total = max(img.shape[0], img.shape[1]) - min(img.shape[0], img.shape[1])

    #CASE 1: ALREADY SQUARE

    if total==0:
        print("Image does not require cropping")
        cropped_img = img

    #CASE 2: ROW VALUE IS GREATER THAN COLUMN VALUE

    elif(img.shape[0]>img.shape[1]):
        if total % 2 == 0:
            cropped_img = img[total//2:img.shape[0]-total//2, :]
            print("Image cropped at (",total//2,",0) and (",
            (img.shape[0]-(total//2))-1,",",img.shape[1]-1,")",sep="")
        else:
            cropped_img = img[total//2:img.shape[0]-total//2-1, :]
            print("Image cropped at (",total//2,",0) and (",
            (img.shape[0]-(total//2))-2,",",img.shape[1]-1,")",sep="")

    #CASE 3: COLUMN VALUE IS GREATER THAN ROW VALUE

    else:
        if total % 2 == 0:
            cropped_img = img[:, total//2:img.shape[1]-total//2]
            print("Image cropped at (0,",total//2,") and (",
            img.shape[0]-1,",",img.shape[1]-total//2-1,")",sep="")
        else:
            cropped_img = img[:, total//2:img.shape[1]-total//2-1]
            print("Image cropped at (0,",total//2,") and (",
            img.shape[0]-1,",",img.shape[1]-total//2-2,")",sep="")

    return cropped_img

"""
This function takes in an image and a command line argument that determines
what size the images will be resized to. It returns a resized image of those
dimensions.

"""
def resize(img, square_size):

    #CASE 1: IMAGE IS ALREADY SQUARE SIZE X SQUARE SIZE

    if img.shape[0]==square_size and img.shape[1]==square_size:
        print("No resizing needed")
        resized_img = img

    #CASE 2: IMAGE NEEDS TO BE RESIZED

    else:
        resized_img = cv2.resize(img, (square_size, square_size),
         interpolation=cv2.INTER_AREA)
        print("Resized from ",img.shape," to ",resized_img.shape)

    return resized_img

"""
This function calls the crop and resize functions to format the two images that
get passed in as parameters. It then makes use of the concatenate and tile
functions to put together a checkerboard of these two images. It returns this
checkerboard as the final image.

"""
def checkerboard(img1, img2, rows, cols, square_size):

    img1 = crop(img1)
    img1 = resize(img1, square_size)

    img2 = crop(img2)
    img2 = resize(img2, square_size)

    top_row = np.concatenate((img1,img2), axis=1)
    top_row = np.tile(top_row, (cols//2, 1))

    second_row = np.concatenate((img2, img1), axis=1)
    second_row = np.tile(second_row, (cols//2, 1))

    top_two = np.concatenate((top_row, second_row), axis=0)
    final_img = np.tile(top_two, (rows//2, 1, 1))

    return final_img


#MAIN

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Incorrect number of arguments!")
        sys.exit()

    output_img = sys.argv[2]
    rows = int(sys.argv[3])
    cols = int(sys.argv[4])
    square_size = int(sys.argv[5])

    #save working directory as variable, used when outputting image
    working_dir = os.getcwd()

    if os.path.isdir(sys.argv[1]):
        image_dir = sys.argv[1]
        img1, img2 = getImages(image_dir, square_size)
    else:
        print(image_dir, "is an invalid directory.")
        sys.exit()

    #the checkerboard image is saved as a numpy array
    final_image = checkerboard(img1, img2, rows, cols, square_size)


    #OUTPUT IMAGE

    #change the directory back to the original working directory
    os.chdir(working_dir)
    #output the image under the name given in the command line argument
    cv2.imwrite(output_img, final_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
