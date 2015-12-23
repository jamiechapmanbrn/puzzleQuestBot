import ImageGrab
import os
import time


top_left = (7,30)
bottom_right = (807,630)
box = ( top_left[0],top_left[1],bottom_right[0],bottom_right[1])
def screenGrab():
    time.sleep(5)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')
    #return im
    

def main():
    screenGrab()
 
if __name__ == '__main__':
    main()