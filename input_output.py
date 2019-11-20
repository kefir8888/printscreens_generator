import cv2
from pathlib import Path
import math
import numpy as np

def get_available_cameras (upper_bound = 10, lower_bound = 0):
    available = []
    
    for i in range (lower_bound, upper_bound):
        cap = cv2.VideoCapture (i)
    
        if (cap.isOpened ()):
            available.append (i)
    
        cap.release ()
    
    return available

def folder_files (path):
    files_png = sorted (Path (path).glob('*.png'))
    files_jpg = sorted (Path (path).glob('*.jpg'))
    files_bmp = sorted (Path (path).glob('*.bmp'))

    files = files_png + files_jpg + files_bmp

    return files

#Incapsulates reading frames from the following types of sources:
#photo (single image), photos series, video, camera, ROS node (?)

#If an input file or camera number is given, desired input type
#can be omitted. Numeric value given in initialization is considered
#as a number of camera desired to be opened. Value "-1" opens camera
#with minimal available id, "-2" - with maximal.

#TODO: semi-automatic source type detection
#TODO: implementation of reading from all the sources (except for ROS) [later]
#TODO: output [later]

class Source:
    #type = ""
    #path = ""

    #Taking sample image requires reading, in case of non-constant
    #sources like camera or video it can lead to a loss of a single
    #frame. These is the fix :)
    sample_image_obtained          = False
    sample_image_incoherency_fixed = False

    def __init__ (self, path_, type_ = "", instant_init = True):
        self.path = path_
        
        if (type_ == ""):
            if (self.path.endswith ("jpg") or
                self.path.endswith ("png") or
                self.path.endswith ("bmp")):
                self.type = "photo"

            elif (self.path.endswith (".webm") or
                self.path.endswith (".mp4") or
                self.path.endswith (".avi")):
                self.type = "video"

            elif (self.path.endswith ("/")):
                self.type = "photo series"

            elif (self.path.isnumeric      () == True or
                  self.path [1:].isnumeric () == True):
                self.type = "camera"

                num = int (self.path)

                if (num < 0):
                    cameras = get_available_cameras ()

                    if (num == -1):
                        self.cam_num = min (cameras)

                    else:
                        self.cam_num = max (cameras)

                else:
                    self.cam_num = num                    

            else:
                self.type = "ros flex"

        else:
            self.type = type_

        if (instant_init == True):
            self.init_source ()

    def shape (self):
        return self.sample_image ().shape

    def sample_image (self):
        if (self.sample_image_obtained == False):
            self.sample_image = self.get_frame ()

            self.sample_image_obtained = True

        return self.sample_image

    def init_source (self):
        self.sources = {}

        self.sources.update ({"photo"        : (self.init_photo,        self.get_frame_photo)})
        self.sources.update ({"photo series" : (self.init_photo_series, self.get_frame_photo_series)})
        self.sources.update ({"video"        : (self.init_video,        self.get_frame_video)})
        self.sources.update ({"camera"       : (self.init_camera,       self.get_frame_camera)})
        #self.sources.update ({"ros flex"     : (self.init_ros_flex,     self.get_frame_ros_flex)})

        self.sources [self.type] [0] ()

    def init_photo (self):
        self.img = cv2.imread (self.path)

    def init_photo_series (self):
        self.file_num = 0
        self.files = folder_files (self.path)

        #print (self.files)

        #print (len (self.files), " files")

    def init_video (self):
        self.video = cv2.VideoCapture (self.path)

    def init_camera (self):
        self.camera = cv2.VideoCapture (self.cam_num)

    #def init_photo (self):
    #    self.img = cv2.imread (self.path)

    def get_frame (self):
        if (self.sample_image_obtained          == True and
            self.sample_image_incoherency_fixed == False):
            self.sample_image_incoherency_fixed = True
            
            return self.sample_image

        return self.sources [self.type] [1] ()

    def get_frame_photo (self):
        return self.img.copy ()
        
    def get_frame_photo_series (self):
        filename = str (self.files [self.file_num])

        #print (filename)

        img = cv2.imread (filename)

        self.file_num += 1

        if (self.file_num == len (self.files)):
            self.file_num = 0

        return img

    def get_frame_video (self):
        reading_success, frame = self.video.read ()

        if (reading_success == False):
            self.video.release ()
            self.init_video ()

            reading_success, frame = self.video.read ()

        return reading_success, frame

    def get_frame_camera (self):
        reading_success, frame = self.camera.read ()

        return frame

    def get_frame_photo (self):
        return self.img.copy ()

#output (stream to video file)

#generalize to the desired a by b cells grid (?)
#generalize to the desired acpect ratio (?)

def form_grid (images_, window_x_sz = -1, one_img_x_sz = -1, square_like = True):
    images = []

    sh = images_ [0].shape
    scaling = 4

    szx = int (sh [0] / scaling)
    szy = int (sh [1] / scaling)

    for img_ in images_:
        img = cv2.resize (img_, (szx, szy))
        images.append (img)

    if (square_like == True):
        images_num = len (images)
        row_len = math.ceil (math.sqrt (images_num))
        print ("row len", row_len)

        #form rows
        rows = []

        for i in range (row_len):
            #new_row_ = images [i * row_len : min (i * row_len + row_len, images_num)]]

            print ("len", len (new_row_))

            if (len (new_row_) != row_len):
                while (len (new_row_) != row_len):
                    new_row_.append (new_row_ [-1])

            new_row = np.concatenate (tuple (new_row_), axis = 0)

            rows.append (new_row)

        for row in rows:
            print (row.shape)

        result = np.concatenate (tuple (rows), axis = 1)

    return result






