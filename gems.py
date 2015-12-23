
import string 

grid_top = (169,100)
cell_width = 56
cell_length = 56
divider_width = 2
class gem:            
    def __init__(self,colorMax,colorMin , value ,symbol , fullName):
        self.colorMax = colorMax
        self.colorMin = colorMin
        self.value = value
        self.symbol = symbol
        self.fullName = fullName
    def printTable(self):
        return self.fullName + " = gem(" + str( self.colorMax ) + ',' + str( self.colorMin) + ',' + str(self.value) + ", '" + self.symbol + "'" + ', "' + self.fullName + '"' + ")"  
    def matchGem( self , other ):
        if other == None:
            return False
        for char in list( other.symbol) :
            if char in self.symbol:
                return True
        return False
    
    
def cropGem( im , loc ):
    bound = ( grid_top[0] + loc[0] * (cell_width + divider_width ) , \
    grid_top[1] + loc[1] * (cell_width + divider_width ) , \
    grid_top[0] + (loc[0]) * (cell_width + divider_width) + cell_width, \
    grid_top[1] + (loc[1]) * (cell_width + divider_width) + cell_width )
    return im.crop( bound )

    
window = ( 30 , 22 , 45 , 35 )  
sum = (window[2] - window[0]) * ( window[3] - window[1])
def getGem( im ,  loc ):
    cropped = cropGem( im , loc )
    avg = [0.0,0.0,0.0]
    for i in range( window[0], window[2] ):
        for j in range( window[1], window[3] ):
            for color in range (0,3):
                avg[color] += cropped.getpixel( (i,j) )[color]
    output = ( round(avg[0]/sum) , round(avg[1]/sum) , round(avg[2]/sum))
    return output

        
def showGem( loc ):
    mousePos( (grid_top[0]+ gem_offset_loc[0] + cell_width*loc[0] + loc[0]* divider_width , grid_top[1] + gem_offset_loc[1] + cell_length*loc[1]+ loc[1]* divider_width ) )

