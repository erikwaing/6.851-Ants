import math
from FKLS import *
import matplotlib as mpl
import pylab as pl
import Image,ImageDraw

def showStatus(ant):
    print "Ant"
    print "Location: ", ant.getLocation()
    #print "i: ", ant.i
    #print "(j, i)", (ant.j, ant.i)
    #print "u = ", ant.u
    #print "Spiral step: ", ant.step
    #print "Spiral limit: ", ant.t_max()
    #if ant.step == 'spiral':
    #    print "Spiral current:", ant.t


def drawBoard(ants, xrange, yrange, placesVisitedDuringSpiral):
    img = Image.new("RGB", (xrange, yrange), "#FFFFFF")
    draw = ImageDraw.Draw(img)
    for i in range(xrange):
        for j in range(yrange):
            if i == xrange/2 and  j == yrange/2:
                r, g, b = 255, 0, 0
            else:
                r, g, b = 0, 0, 0
            for ant in ants:
                (x0, y0) = ant.getLocation()
                if x0 + xrange/2 == i and y0 + yrange/2 == j:
                    r, g, b = 0, 255, 0
            if (i,j) in placesVisitedDuringSpiral:
                r, g, b = 255, 255, 255
            draw.point((i,yrange - j - 1), fill=(int(r),int(g),int(b)))
    return img

def showImage(ants, xrange, yrange):
    img = drawBoard(ants, xrange, yrange, [])
    img = pl.imshow(img)
    pl.draw()
    pl.show()
    option = raw_input()
    while option != 'q':
        for ant in ants:
            ant.act()
            showStatus(ant)
            if ant.step != 'spiral':
                placesVisitedDuringSpiral = []
            else:
                (i, j) = ant.location
                placesVisitedDuringSpiral.append((i+xrange/2, j+yrange/2))
        print placesVisitedDuringSpiral
        img = drawBoard(ants, xrange, yrange, placesVisitedDuringSpiral)
        pl.imshow(img)
        pl.draw()
        pl.pause(0.2)
        option = raw_input()

ant = FKLS2((0,0), lambda x: x*x + 1)

