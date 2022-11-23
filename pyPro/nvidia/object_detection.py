
import cv2
import jetson.inference
import jetson.utils
import time
import numpy as np 
timeStamp = time.time()
width = 640
height = 480
fpsFilter = 0
# get detection model
net= jetson.inference.detectNet('ssd-mobilenet-v2',threshold =.5)
# create cam object
cam =jetson.utils.gstCamera(640,480,'/dev/video0')
display = jetson.utils.glDisplay()
font = jetson.utils.cudaFont()

while display.IsOpen():
    # grab frame
    img, width, height = cam.CaptureRGBA()
    # detect and analyze
    detection = net.Detect(img,width, height)
    # show result
    display.RenderOnce(img,width,height)
    dt = time.time() - timeStamp
    timeStamp = time.time()
    fps = 1/dt
    fpsFilter = .9*fpsFilter + .1*fps
    print(str(round(fps,1)) +' fps')