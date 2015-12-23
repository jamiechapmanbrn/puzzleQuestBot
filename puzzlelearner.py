import ImageGrab
import os
import time
import ImageOps
from numpy import *
import win32api, win32con
import msvcrt
from PIL import Image, ImageDraw, ImageFont

from gems import *

from gemtypes import gemTypes

gem_type_list = [   gemTypes.blue_gem , 
                gemTypes.gold_gem , 
                gemTypes.red_gem, 
                gemTypes.exp_gem , 
                gemTypes.yellow_gem , 
                gemTypes.red_skull , 
                gemTypes.green_gem , 
                gemTypes.skull_gem ,
                gemTypes.double_gem,
                gemTypes.triple_gem,
                gemTypes.quadruple_gem,
                gemTypes.quintuple_gem,
                gemTypes.hextuple_gem,
                gemTypes.octuple_gem   
            ]

top_left = (7,30)
bottom_right = (807,630)

box = ( top_left[0],top_left[1],bottom_right[0],bottom_right[1])

top_left = (7,30)
bottom_right = (807,630)



gem_offset_loc = (20,25)



dburg = (254,328)
Lysea = (180,437)

buttonThreshold = 5

ReadyRunLoc=(268,429)
ReadyRun = (4,48,79)

rebellionButton = (375,431)
OKRebellion = (4,47,79)

def learnGem( pixel , type ):
    if type[0] != '?':
        for gem in gem_type_list:
            if type == gem.symbol[0]:
                min = [ gem.colorMin[0] , gem.colorMin[1] , gem.colorMin[2] ]
                for i in range(0,3):
                    if pixel[i] < gem.colorMin[i]:
                        min[i] = pixel[i]
                        print pixel[i]
                gem.colorMin = ( min[0] , min[1] , min[2] )
                max = [ gem.colorMax[0] , gem.colorMax[1] , gem.colorMax[2] ]
                for i in range(0,3):
                    if pixel[i] > gem.colorMax[i]:
                        max[i] = pixel[i]
                gem.colorMax = ( max[0] , max[1] , max[2] )
                print "for gem" + gem.symbol[0]
                print "newmax:"
                print gem.colorMax
                print "newmin:"
                print gem.colorMin
            

 

def printResult():
    f = open( "gemTypes.py" , 'w')
    f.write("from gems import gem\n")
    f.write("class gemTypes: \n")
    for gem in gem_type_list:
        f.write( "    " )
        f.write( gem.printTable() )
        f.write ( "\n")

color = [ "rgb(255,0,0)" , "rgb(0,255,0)" , "rgb(0,0,255)" ]
        
def plotSolution():

    #font = ImageFont.truetype("resources/HelveticaNeueLight.ttf", 12)
    
    Im = Image.new( "RGB" , (1024,1024), "white" )
    
    startX = 60
    startY = 30
    space = 40
    draw = ImageDraw.Draw(Im)
    
    h = startY
    for i in range(0,3):
        draw.rectangle( [(startX-10 , h ) , (startX+10 , h + 255)] , fill=color[i] )
        h = h + 256 + space
    x = startX + space
    for gem in gem_type_list:
        h = startY
        draw.text( (x , startY-15) , gem.symbol , fill=0 )
        for i in range (0,3):
            draw.rectangle( [(x , h + gem.colorMin[i]) , (x+10 , h + gem.colorMax[i])] , fill=color[i] )
            h = h + 256 + space
        x = x+ space
    del draw
    Im.save(os.getcwd() + '\\plot' +'.png', 'PNG')

learnSet = [ 1 , 2, 3 , 4 , 5 , 6 ]
    
def main():
    count = 0
    exitTime = False
    dir = "away"
    #printComButtons(im)
    #while ( True ):
    
    #getGem( im , (3,1) );
    gemString = ''
    for data in learnSet:
        
        file = open( 'solution' + str(data) + '.txt' , 'r' )
        im = Image.open('solution' + str(data) + '.png')
        loc = 0
        input = file.read()
        for j in range (0,8):
            for i in range (0,8):
                #thisGem = convertGem( getGem( im , ( i , j ) ) )
                
                inchar = input[loc]
                
                if inchar.isdigit():
                    cropped = cropGem( im , (i,j) )
                    cropped.crop(window).save(os.getcwd() + '\\cell' + str(loc) + inchar +'.png', 'PNG')
                '''
                this is what you need to change
                '''
                inGem = getGem( im , (i,j) )

                learnGem( inGem , inchar )
                #print thisGem
                '''For generating the board layout'''
                #gemString = gemString + thisGem
                loc= loc+1
                print inchar
            loc = loc+1
            print '\n'
            '''output the board layout'''
            #gemString = gemString + '\n'
    plotSolution()
    check = raw_input("keep solutions?: ")
    if check == 'y':
        printResult()
    
if __name__ == '__main__':
    main()