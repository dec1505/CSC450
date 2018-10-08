import random
import math
import matplotlib.pyplot as plt

#K-Means Clustering


#This program takes set Data Points, and classifies the points into the amount of clusters the user desires


def main():

    # read in txt file with data points

    with open('xyz.txt') as fp:
        lines = fp.read().replace("\t","\n").split("\n")

    variable1 = lines[0]
    variable2 = lines[2]

    lines.pop(0)
    lines.pop(0)
    lines.pop(0)

    xlist = []
    ylist = []

    count = 1

    for e in lines:
        if count%2 == 0:
            ylist.append(e)
        else:
            xlist.append(e)
        count+=1

    #generate random start points for cluster means

    xmeans, ymeans, numofcats = generatestartpoints()

    xmeans = list(map(float, xmeans))
    ymeans = list(map(float, ymeans))

    originalxmeans = xmeans
    originalymeans = ymeans

    xlist = list(map(float, xlist))
    ylist = list(map(float, ylist))

    change = 1

    itercount = 0

    catlist = categorize(xlist, ylist, xmeans, ymeans)
    print("Random Mean Starting points: ")

    print(xmeans, ymeans)

    while change > 0.00001:

        catlist = categorize(xlist, ylist, xmeans, ymeans)

        xmeans, ymeans, change = refinemean(numofcats, catlist, xlist, ylist, xmeans, ymeans)

        itercount += 1
    print("Final Mean points after ", itercount, " iterations: ")

    print(xmeans, ymeans)

    makescatterplot(xlist, ylist, xmeans, ymeans, catlist, originalxmeans, originalymeans)

def generatestartpoints():

    numofclusters = int(input("How many clusters would you like to create? (integer only): "))

    xmeans = []
    ymeans = []

    for i in range(numofclusters):

        xmeans.append(random.uniform(0.0, 1.0))
        ymeans.append(random.uniform(0.0, 1.0))

    return xmeans, ymeans, numofclusters


def categorize(x, y, xmean, ymean):

    ind = 0
    ind2 = 0

    catlist = []

    category = 0

    for p in range(len(x)):

        xpoint = x[ind]
        ypoint = y[ind]

        ind += 1

        bestdistance = 1000

        for i in range(len(xmean)):

            xm = xmean[i]
            ym = ymean[i]

            distance = math.sqrt(((xm-xpoint)**2)+((ym-ypoint)**2))

            if distance < bestdistance:

                bestdistance = distance
                category = i

            ind2 += 1

        catlist.append(category)

    return catlist


def refinemean(numofcats, cats, xlis, ylis, xmean, ymean):

    #add up the x's and y's in each category to get new xmean and ymean

    newxmeans = []
    newymeans = []

    change = 0

    for j in range(numofcats):

        xsum = 0
        ysum = 0

        catcount = 0

        count = 0

        for cat in cats:

            if cat == j:

                x = xlis[count]
                y = ylis[count]

                xsum += x
                ysum += y

                catcount += 1

            count += 1

        if count != 0:

            meanx = float(xsum/(catcount))
            meany = float(xsum/(catcount))

            change += abs(meanx-xmean[j])

            newxmeans.append(meanx)
            newymeans.append(meany)

        else:

            newxmeans.append(xmean[j])
            newymeans.append(xmean[j])

    return newxmeans, newymeans, change


def makescatterplot(xs, ys, xmean, ymean, cats, origx, origy):

    x = xs
    y = ys

    for mean in xmean:
        x.append(mean)

    for m in ymean:
        y.append(m)

    for ox in origx:
        x.append(ox)

    for oy in origy:
        y.append(oy)

    colors = []

    currentcat = -1

    catsdone = []

    catcolors = []

    for i in range(len(cats)):

        if currentcat != cats[i]:

            currentcat = cats[i]

            if currentcat in catsdone:

                color = catcolors[catsdone.index(currentcat)]

            else:
                color = random.uniform(.1, .9)
                catcolors.append(color)
                catsdone.append(currentcat)

        colors.append(color)

    for j in range(len(xmean)):

        colors.append(0)

    for z in range(len(origx)):
        colors.append(1.0)

    plt.scatter(x, y, c=colors, alpha=0.9)
    plt.show()

main()