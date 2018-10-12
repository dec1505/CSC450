#author: Devan Corcoran

import random
import math
from PIL import Image
import pygame
import sys
from pygame.locals import*
'''
This program takes an image file and reads the pixel values in order to
create a color palette. The palette has a number of colors that the user
decides upon.
'''


def main():
    
    user_image = input("Enter the file name: ")

    pixel_list = read_pixels(user_image)

    palette_num = int(input("How many colors would you like on the palette? "))

    xmeans, ymeans, zmeans = create_palette(palette_num, pixel_list)

    colorlist = []

    for i in range(len(xmeans)):
        r = xmeans[i]
        g = ymeans[i]
        b = zmeans[i]

        colorlist.append([r,g,b])

    print(colorlist)

    pygame.init()

##    screen = pygame.display.set_mode((1020, 100))
##
##    xcoord = -200
##
##    pattern = False
##    clock = pygame.time.Clock()
##    while not pattern:
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT:
##                pattern = True
##        for color in colorlist:
##
##            pygame.draw.rect(screen,color, (xcoord,0,100,100), 0)
##            xcoord+=100
##
##        pygame.display.flip()
##        clock.tick(60)
##
##    pygame.quit()



    
def read_pixels(imagename):
    '''
    This function uses the pillow package. It creates a list of the rgb values
    of every pixel in an image.
    '''

    im = Image.open(imagename, 'r')

    pix_val = list(im.getdata())

    return pix_val


def create_palette(palette_num, pixel_list):

    '''
    This function does all the work for creating the palette, using other functions in
    the program. first, it seperates the rgb values into separate lists for r (in the xlist),
    g (in the ylist), and b (im the zlist). Then it uses a function to generate random rgb start
    points for the categories. A function is used to separate the pixels into different
    categories, if there are 3 categories, the values indicating each would be 0,1, and 2.
    Until the category points stop changing, the mean of each assigned pixel values for each
    category are calculated, and the means are updated. Then the process is repeated: Categorize
    pixels, then refine the mean.
    '''
    
    xlist = []
    ylist = []
    zlist = []
    
    for each in pixel_list:

        xlist.append(each[0])
        ylist.append(each[1])
        zlist.append(each[2])

    xmeans, ymeans, zmeans = generatestartpoints(palette_num) 

    change = 1

    catlist = categorize(xlist, ylist, zlist, xmeans, ymeans, zmeans)

    while change > 0.00001:

        catlist = categorize(xlist, ylist, zlist, xmeans, ymeans, zmeans)

        xmeans, ymeans, zmeans, change = refinemean(palette_num, catlist,
                                                 xlist, ylist, zlist, xmeans, ymeans, zmeans)

    return(xmeans, ymeans, zmeans)

        
def generatestartpoints(num):

    '''
    A simple random pick of values from 0 to 255 is done to create start points for
    the palette color mean.
    '''

    xmeans = []
    ymeans = []
    zmeans = []
    
    for i in range(num):
        
        xmeans.append(random.randint(0, 255))
        ymeans.append(random.randint(0, 255))
        zmeans.append(random.randint(0, 255))

    return xmeans, ymeans, zmeans

def categorize(x, y, z, xmeans, ymeans, zmeans):
    '''
    For each pixel point, the distance from the current category mean points are calculated,
    and the pixels are assigned to the category of the pixel that it is closest to. A category
    list is returned that would look something like [0,2,1,2,1,0,0,0....] if there were 3 categories.
    '''

    catlist = []

    category = 0
    
    for i in range(len(x)):

        xpoint = x[i]
        ypoint = y[i]
        zpoint = z[i]

        bestdistance = 10000000000000

        for j in range(len(xmeans)):

            xm = xmeans[j]
            ym = ymeans[j]
            zm = zmeans[j]

            distance = math.sqrt(((xm-xpoint)**2)+((ym-ypoint)**2)+((zm-zpoint)**2))

            if distance  < bestdistance:

                bestdistance = distance
                category = j

        catlist.append(category)

    return catlist

def refinemean(palette_num, catlist, xlist, ylist, zlist, xmeans, ymeans, zmeans):

    '''
    This function updated the category rgb values by taking the mean of all the rgb pixel points
    that are assigned to it. Thes then become the new points.
    '''

    newxmeans = []
    newymeans = []
    newzmeans = []

    change = 0

    for j in range(palette_num):

        xsum = 0
        ysum = 0
        zsum = 0

        catcount = 0

        count = 0

        for cat in catlist:

            if cat == j:

                x = xlist[count]
                y = ylist[count]
                z = zlist[count]
                
                xsum += x
                ysum += y
                zsum += z

                catcount += 1

            count += 1

        if count != 0:

            meanx = xsum//catcount
            meany = ysum//catcount
            meanz = zsum//catcount

            change += abs(meanx-xmeans[j])

            newxmeans.append(meanx)
            newymeans.append(meany)
            newzmeans.append(meanz)

        else:

            newxmeans.append(xmeans[j])
            newymeans.append(ymeans[j])
            newzmeans.append(zmeans[j])

    return newxmeans, newymeans, newzmeans, change
            

main()
