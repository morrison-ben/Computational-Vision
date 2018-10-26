"""

HW 3 PROBLEM 2

Author: Ben Morrison

"""

##IMPORTS

import cv2
import numpy as np
import os
import sys
import math

#FUNCTIONS


"""
minCost: This function calculates the minimum cost for each row; it is
used to form the cost array

It works by creating 2 slices of the previous row array (-1 shift, +1 shift)
and using the original prev_row array as the center slice. Infinite values fill
the empty spots in the array. It then forms a minimum array with the left and
right arrays and compares this to the center array to get all the correct
min values. The last step is to add the energy values for the current row and
return the array to the for loop found within the main.


"""

def minCost(current_row, prev_row):

    #account for edges
    # current_row = current_row[:,1:-1]
    # previous_row = previous_row[:,1:-1]

    #create 3 sliced arrays

    temp = np.array([np.inf]).reshape(1,1)
    prev_row = prev_row.reshape((1,img.shape[1]))
    slice_right = np.array(prev_row[:,1:])
    slice_right_full = np.append(slice_right,temp,axis=1)

    slice_left = np.array(prev_row[:,:-1])
    slice_left_full = np.append(temp,slice_left,axis=1)

    min_left_right = np.minimum(slice_right_full,slice_left_full)

    min_array = np.minimum(min_left_right, prev_row)

    updated_cost = min_array+current_row

    return updated_cost

"""
backtrackSeam: This function is called once the cost matrix is assembled. Its
purpose is to take in the current location and return the new location that
has the minimum cost value (out of the 3 options)

It does this by creating three location variables that represent the three
options of the next possible index. It then obtains the cost values of these
indices and returns the index with the lowest cost value. This repeats within
main until the edge of the image is reached, giving us a complete seam.


"""

def backtrackSeam(loc, cost):

    #create 3 potential indices

    left_index = loc[0]-1, loc[1]-1
    center_index = loc[0]-1, loc[1]
    right_index = loc[0]-1, loc[1]+1

    #create 3 slices with the 3 indices

    cost_left = cost[left_index[0]][left_index[1]]
    cost_center = cost[center_index[0]][center_index[1]]
    cost_right = cost[right_index[0]][right_index[1]]

    #find minimum and return

    if min(cost_left, cost_center, cost_right) == cost_left:
        return left_index
    if min(cost_left, cost_center, cost_right) == cost_right:
        return right_index
    else:
        return center_index



#MAIN
if __name__ == '__main__':

    ##COMMAND LINE ARGS
    if len(sys.argv) != 2:
        print("Invalid number of arguments!")
        sys.exit()

    #if correct, we must make sure each argument is valid. If not, exit program
    else:
        img_in = sys.argv[1]
        if img_in is None:
            print("Failed to open image:", sys.argv[1])
            sys.exit()

    #Read in image as grayscale

    img = cv2.imread(img_in,0)

    #Read in a colored version of image(needed for later)
    img_colored = cv2.imread(img_in)

    #if in portrait mode, transpose to get landscape mode
    horiz = False
    if(img.shape[0] > img.shape[1]):
        img = np.transpose(img)
        img_colored = np.transpose(img_colored)
        horiz = True


    #cols_total = img.shape[1]

    #LOOP UNTIL IMAGE IS SQUARE
    while (img.shape[1]>img.shape[0]):


        #BUILD THE ENERGY MATRIX


        #get x and y gradient matrices
        grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, 3)
        grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, 3)

        #combine to form energy matrix
        energy_matrix = np.sqrt(grad_x**2 + grad_y**2)


        #create an np array of np.inf values
        x = np.full((img.shape[0]),np.inf)

        #set columns 0 and N-1 to this array - ensures that the border of the image
        #will never be included in a seam path
        energy_matrix[:,0] = x
        energy_matrix[:,grad_y.shape[1]-1] = x




        #BUILD COST MATRIX


        #preallocate cost_matrix for efficiency
        cost_matrix = np.zeros((img.shape[0],img.shape[1]))

        #set first row of cost matrix equal to the first row of energy matrix
        cost_matrix[0,:] = energy_matrix[0,:]

        #counter variable
        x = 1

        #loop through rows to form cost matrix
        for row in range(1,cost_matrix.shape[0]):
            new_row = minCost(energy_matrix[x, :], cost_matrix[x-1, :])
            cost_matrix[x,:] = new_row
            x+=1



        #BACKTRACKING TO FIND SEAM


        #grab last line of cost matrix
        last_line = cost_matrix[-1]


        #find the index of the min value for the last line
        index_min = np.argmin(last_line)

        #convert to a 2d image point
        index_min = (cost_matrix.shape[0]-1, index_min)

        #set location variable to this point
        location = index_min


        #TRACK SEAM, DELETE PIXELS AS WE GO

        #start i at the bottom pixel of the image
        i = img_colored.shape[0]-1


        for row in img_colored:
            #set current row
            current_row = np.array(img_colored[i])

            #slice into left half and right half, excluding the
            #pixel that needs to be deleted
            left_half = current_row[:location[1]]
            right_half = current_row[location[1]+1:]

            #create a zero array of correct dimensions to append
            #onto the end of the row
            zero = np.array([0,0,0]).reshape(1,3)
            right_half = np.concatenate((right_half, zero))

            #put the row back together
            current_row = np.concatenate((left_half,right_half))

            #broadcast the updated row onto the colored image
            img_colored[i] = np.array(current_row)

            #get new location and update counter variable i
            location = backtrackSeam(location, cost_matrix)
            i-=1



        #slice the zero column off the end
        img_colored = img_colored[:,:-1]

        #reset to grayscale
        img = cv2.cvtColor(img_colored, cv2.COLOR_BGR2GRAY)



        ##DIDN'T GET TO PRINT STATEMENTS

        # x=0
        # print("Points on seam 0:")"
        # if(horiz):
        #     print("horizontal")
        # else:
        #     print("vertical")
        # for row in range(0,cost_matrix.shape[0]-1):
        #     if(x==0):
        #     #print end pixel
        #     if(x==cost_matrix.shape[0]//2):
        #     #print middle pixel
        #     if(x==cost_matrix.shape[0]-1):
        #     #print start pixel
        #     location = backtrackSeam(location, cost_matrix)
        #     #set pixel at location index to red
        #     img_colored[location[0]][location[1]] = [0,0,255]

        # if (img.shape[1]==cols_total):
        #     img_title, img_ext = os.path.splitext(img_in)
        #     img_seam_name = img_title + '_seam' + img_ext
        #     cv2.imwrite(img_seam_name, img_colored)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()



    if(horiz):
        img_colored = np.transpose(img_colored)



    #OUTPUT IMAGE

    img_title, img_ext = os.path.splitext(img_in)
    img_out_name = img_title + '_final' + img_ext
    cv2.imwrite(img_out_name, img_colored)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # img_title, img_ext = os.path.splitext(img_in)
    # img_seam_name = img_title + '_seam' + img_ext
    # cv2.imwrite(img_seam_name, img_colored)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
