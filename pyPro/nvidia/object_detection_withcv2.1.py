
import cv2
import jetson_inference
import jetson_utils
import time
import numpy as np 
timeStamp = time.time()
width = 640
height = 480
fpsFilter = 0
# get detection model
net= jetson_inference.detectNet('ssd-mobilenet-v2',threshold =.5)
# create cam object
cam = cv2.VideoCapture('/dev/video0')
# set window size
cam.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
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
        id = detect.ClassID
        item = net.GetClassDesc(id)
        top = detect.Top
        left = detect.Left
        right = detect.Right
        width = detect.Width
        height = detect.Height 
        print(item,top,left,right,width,height)
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