import ImageGrab
import os
import time
import ImageOps
from numpy import *
import win32api, win32con
import msvcrt
import Image, ImageDraw, ImageFont
from copy import deepcopy

from gems import *
from gemtypes import gemTypes
from puzzlelearner import *


gemDict= {  }

def initDict():
    for gem in gem_type_list:
        gemDict[gem.symbol[0]] = gem
  
  
top_left = (7,30)
bottom_right = (807,630)

box = ( top_left[0],top_left[1],bottom_right[0],bottom_right[1])

top_left = (7,30)
bottom_right = (807,630)

grid_top = (169,100)

gem_offset_loc = (20,25)

cell_width = 56
cell_length = 56
divider_width = 2

dburg = (254,328)
Lysea = (180,437)

buttonThreshold = 8

ReadyRunLoc=(268,429)
ReadyRun = (4,48,79)

rebellionButton = (375,431)
OKRebellion = (4,47,79)

def getValue(matchList):
    value =0
    for matchSet in matchList:
        for match in matchSet:
            temp_value = 0
            multList = []
            for physgem in match:
                if physgem.gem.symbol[0].isdigit():
                    multList.append( int(physgem.gem.symbol[0]) )
                else:
                    temp_value += physgem.gem.value
            for multiplier in multList:
                temp_value *= multiplier
            numGem = len(match)
            if numGem == 4:
                temp_value *= 6
            if numGem > 5:
                temp_value *= 10
            value+=temp_value
    return value

#wrapper of gem class for physical gems on the board    
class physGem:
    def __init__ (self, gem , loc  ):
        self.gem = gem
        self.loc = loc
    def __str__(self):
        return str(self.symbol + " :" + str(self.loc))
        
class board:
    def __init__(self):
        self.board = [ [' ',' ',' ',' ',' ',' ',' ',' '] , [' ',' ',' ',' ',' ',' ',' ',' '] , [' ',' ',' ',' ',' ',' ',' ',' '] , [' ',' ',' ',' ',' ',' ',' ',' '] , [' ',' ',' ',' ',' ',' ',' ',' '] , [' ',' ',' ',' ',' ',' ',' ',' '] , [' ',' ',' ',' ',' ',' ',' ',' '] ,[' ',' ',' ',' ',' ',' ',' ',' '] ]
    def copy(self):
        return deepcopy(self)
    def printBoard(self ):
        for i in range( 0,8 ):
            str = ''
            for j in range ( 0, 8 ):
                str = str +  self.getGem((i,j))
            print str
    #swaps gems starting at loc in direction dir. only 'D' and 'R' supported
    #dowsn't bound check or cool stuff like that
    def swapGems(self , loc, dir ):
        holder = self.getGem(loc)
        if dir == 'R':
            self.setGem( loc , self.getGem( (loc[0],loc[1]+1) ) )
            self.setGem( (loc[0],loc[1]+1), holder )
        if dir == 'D':
            self.setGem( loc , self.getGem( (loc[0]+1,loc[1]) ) )
            self.setGem( (loc[0]+1,loc[1]), holder )
    def getMatches( self ):
        
        match = [];
        matches = []
        rowCount = 1
        #checkRows
        for i in range(0,8):
            last = None
            match = [];
            for j in range(0,8):
            
                
                if self.getGem( (i,j) ) == ' ':
                    last = None
                elif gemDict[self.getGem( (i,j) )].matchGem( last):
                    rowCount +=1
                    #add it to the current sequence
                    match.append( physGem( gemDict[self.getGem( (i,j) )] , (i,j) ) )
                    #have 3 gems it's an official match
                    if rowCount > 2:
                        if rowCount > 3:
                            matches.pop()
                        matches.append(match)
                        #have more than 3, need to remove last match (it was counted earlier)
                else :
                    #create a new gem sequence
                    match = []
                    last = gemDict[self.getGem( (i,j) )]
                    
                    match.append( physGem( last , (i,j) ) )
                    rowCount = 1
                    
        # check columns
        for j in range(0,8):
            last = None
            match = [];
            for i in range(0,8):
            
                if self.getGem( (i,j) ) == ' ':
                    last = None
                elif gemDict[self.getGem( (i,j) )].matchGem( last):
                    rowCount +=1
                    #add it to the current sequence
                    match.append( physGem( gemDict[self.getGem( (i,j) )] , (i,j) ) )
                    #have 3 gems it's an official match
                    if rowCount > 2:
                        if rowCount > 3:
                            matches.pop()
                        matches.append(match)
                        #have more than 3, need to remove last match (it was counted earlier)
                else :
                    #create a new gem sequence
                    match = []
                    last = gemDict[self.getGem( (i,j) )]
                    
                    match.append( physGem( last , (i,j) ) )
                    rowCount = 1
        return matches
    def getGem( self , loc):
        return self.board[loc[1]][loc[0]]
        
    def setGem( self, loc, type ):
        self.board[loc[1]][loc[0]] = type
        
    def colapseBoard( self ):
        for n in xrange(7):
            for i in range(0,7) :
                for j in range( 0,8):
                    if self.getGem((i+1,j)) == ' ':
                        self.swapGems( ((i , j)) , 'D')
    
    def runBoard( self ):
        matchStack = []
        while( self.getMatches() ):
            matches = self.getMatches()
            matchStack.append( matches )
            for match in matches:
                for physGem in match:
                    self.setGem( physGem.loc , ' ' )
            self.colapseBoard()

                
   
            
        return matchStack
    
def screenGrab():
    im = ImageGrab.grab(box)
    return im

    
def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    
def rightClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,0,0)

def get_cords():
    x,y = win32api.GetCursorPos()

def mousePos(cord):
    win32api.SetCursorPos((cord[0]+top_left[0] , cord[1]+top_left[1]))


def minMaxCompare( max , min , pixel ):
    compareCount = 0
    for i in range(0,3):
        if ( pixel[i]-buttonThreshold <= max[i] ):
            compareCount +=1 
        if ( pixel[i]+buttonThreshold >= min[i] ):
            compareCount +=1
    if (compareCount == 6):
        return True
    else:
        return False

def convertGem( pixel ):
    for gem in gem_type_list:
        if minMaxCompare( gem.colorMax, gem.colorMin , pixel ):
            return gem.symbol
    return '?'
 

def getMoves(gameBoard):
    moves = []
    for i in range(0,8):
        for j in range(0,7):            
            testBoard = gameBoard.copy()
            testBoard.swapGems( (i,j) , 'R' )
            if testBoard.getMatches():
                matches = testBoard.runBoard()
                moves.append( ( testBoard ,  getValue(matches) , (i,j) , 'R' ) ) 
    
    for i in range(0,7):
        for j in range(0,7):          
            testBoard = gameBoard.copy()
            testBoard.swapGems( (i,j) , 'D' )
            if testBoard.getMatches():
                matches = testBoard.runBoard()
                moves.append( ( testBoard ,  getValue(matches) , (i,j) , 'D' ) )
    return moves

def getMaxValue( moves ):
    moveValue = 0
    for move in moves:
        if move[1] > moveValue:
            moveValue = move[1]
    return moveValue
    
def main():
    count = 0
    exitTime = False
    dir = "away"
    initDict()
    #printComButtons(im)
    #while ( True ):
    
    #getGem( im , (3,1) );

    im = screenGrab()
    
    gameBoard = board()
    #build the board
    for j in range (0,8):
        for i in range (0,8):
            thisGem = convertGem( getGem( im , ( i , j ) ) )
            if thisGem[0] == '?':
                print 'help with gem :' + str( (i,j) )
            gameBoard.setGem( (j,i) , thisGem[0])
    gameBoard.printBoard()
    print '\n'

    
    
    for move in getMoves(gameBoard):
        print 'move:'
        print move[2]
        print move[3]
        
        print 'value'
        
        print float(move[1]) / getMaxValue( getMoves( move[0] ) )
        
    
if __name__ == '__main__':
    main()