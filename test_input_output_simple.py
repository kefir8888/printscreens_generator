import cv2
import time
import os
import math
import sys

sys.path.append("/Users/elijah/Dropbox/Programming/detectors/modules/")

import input_output

def main ():    
    source = input_output.Source ("/Users/elijah/Dropbox/Programming/deblur/data/1/images/")
    
    while (True):
        frame = source.get_frame ()
        
        cv2.imshow ("frame", frame)

        time.sleep (0.02)

        keyb = cv2.waitKey (1) & 0xFF
        
        if (keyb == ord('q')):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main ()