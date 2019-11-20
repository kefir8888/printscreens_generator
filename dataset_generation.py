import numpy as np
import cv2
import time

#sys.path.append("../modules/")

class Window:
    def __init__ (self, x_sz_, y_sz_, x_pos_, y_pos_, min_x_pos_, max_x_pos_, min_y_pos_, max_y_pos_, x_step_, y_step_, text_, head_img_path):
        self.x_sz = x_sz_
        self.y_sz = y_sz_

        self.x_pos = x_pos_
        self.y_pos = y_pos_
        self.min_x_pos = min_x_pos_
        self.max_x_pos = max_x_pos_
        self.min_y_pos = min_y_pos_
        self.max_y_pos = max_y_pos_

        self.x_step = x_step_
        self.y_step = y_step_

        self.text = text_

        print (head_img_path)
        head_img_ = cv2.imread ("/Users/elijah/Dropbox/Programming/deblur/data/1/window_head.jpg")

        sh = head_img_.shape

        x_sz = sh [1]

        new_x_sz = self.x_sz
        self.new_y_sz = int (sh [0] / x_sz * self.x_sz)

        self.head_img = cv2.resize (head_img_, (new_x_sz, self.new_y_sz))
        print (self.head_img.shape)
        print ("shape")

    def draw (self, img):
        cv2.rectangle (img, (self.x_pos, self.y_pos),
            (self.x_pos + self.x_sz, self.y_pos + self.y_sz), (200, 200, 34), 5)

        img [self.y_pos: self.y_pos + self.new_y_sz, self.x_pos:self.x_pos + self.x_sz, :] = self.head_img

        #for line in self.text:
        cv2.putText (img, self.text, (self.x_pos + 10, self.y_pos + 160),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 250, 231), 2, cv2.LINE_AA)

    def make_step (self):
        self.x_pos += self.x_step

        if (self.x_pos < self.min_x_pos or self.x_pos > self.max_x_pos):
            self.x_step *= -1
            self.x_pos += self.x_step 

        self.y_pos += self.y_step

        if (self.y_pos < self.min_y_pos or self.y_pos > self.max_y_pos):
            self.y_step *= -1
            self.y_pos += self.y_step 

def read_num (config):
    string = config.readline ()

    if (string == ""):
        return 0, string

    return int (string [0:10]), string

def main ():
    #load config

    config = open ("data/1/config.txt")

    pict_num, _ = read_num (config)    
    IMAGE_X, _  = read_num (config)
    IMAGE_Y, _  = read_num (config)
        
    #create windows
    
    windows = []

    string = "heh"

    while (string != ""):
        print ("aaa")
        x_sz, string      = read_num (config)
        y_sz, string      = read_num (config)
        x_pos, string     = read_num (config)
        y_pos, string     = read_num (config)
        min_x_pos, string = read_num (config)
        max_x_pos, string = read_num (config)
        min_y_pos, string = read_num (config)
        max_y_pos, string = read_num (config)
        x_step, string    = read_num (config)
        y_step, string    = read_num (config)
        head_img_path     = config.readline ()
        string            = config.readline ()
        
        if (string != ""):
            windows.append (Window (x_sz, y_sz, x_pos, y_pos, min_x_pos, max_x_pos, min_y_pos, max_y_pos, x_step, y_step, string, head_img_path))

    for i in range (pict_num):
        image = np.zeros ((IMAGE_Y, IMAGE_X, 3), np.uint8)
        image [:, :, 0] = 141
        image [:, :, 1] = 141
        image [:, :, 1] = 111

        print (i)

        for window in windows:
            window.draw (image)
            window.make_step ()

        cv2.imwrite ("data/1/images/" + "{0:0=5d}".format (i) + ".jpg", image)

if __name__ == "__main__":
    main ()