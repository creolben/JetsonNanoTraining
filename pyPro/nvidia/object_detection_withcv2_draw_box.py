
import cv2
import jetson_inference
import jetson_utils
import time
import numpy as np 
timeStamp = time.time()
dwidth = 640
dheight = 480
fpsFilter = 0
# get detection model
net= jetson_inference.detectNet('ssd-mobilenet-v2',threshold =.5)
# create cam object
cam = cv2.VideoCapture('/dev/video0')
# set window size
cam.set(cv2.CAP_PROP_FRAME_WIDTH,dwidth)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,dheight)
font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    # grab frame
    _,img = cam.read()
    width = img.shape[0]
    height = img.shape[1]
    # convert opencv BGR to RGBA from detect net
    frame = cv2.cvtColor(img,cv2.COLOR_BGR2RGBA).astype(np.float32)
    frame = jetson_utils.cudaFromNumpy(frame)

    # detect and analyze using nvidia utils
    detections = net.Detect(frame,width, height)
    for detect in detections:
        # get detected object info
        id = detect.ClassID
        item = net.GetClassDesc(id)
        top = int(detect.Top)
        left = int(detect.Left)
        right = int(detect.Right)
        bottom = int(detect.Bottom)
        width  = int(detect.Width)
        # create box around objects
        cv2.rectangle(img,(left,top),(right,bottom),(255,0,0),1)
        # add object name on top of box
        cv2.putText(img,item,(round(width/2),top-20),font,.75,(0,0,255),2)
    dt = time.time() - timeStamp
    timeStamp = time.time()
    fps = 1/dt
    fpsFilter = .9*fpsFilter + .1*fps
    # add text to screen
    cv2.putText(img,str(round(fpsFilter,1))+ ' fps',(0,30),font,1,(0,0,255),2)
    # create window with coordinate 0,0
    cv2.imshow('detCam',img)
    # put window at coordinate 0,0
    cv2.moveWindow('detCam',0,0)
    if cv2.waitKey(1)== ord('q'):
        break
    # clean up
cam.release()
cv2.destroyAllWindows()