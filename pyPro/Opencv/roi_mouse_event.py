import cv2
print(cv2.__version__)
 

def mouse_click(event,x,y,flags,params):
    global x1,y1,x2,y2
    global goFlag
    if event == cv2.EVENT_LBUTTONDOWN:
        x1 = x
        y1 = y
        goFlag =0 
    if event == cv2.EVENT_LBUTTONUP:
        x2 = x
        y2 = y
        goFlag =1

cv2.namedWindow('nanoCam')
goFlag = 0
cv2.setMouseCallback('nanoCam',mouse_click)
dispW=1280
dispH=720
flip=2


#Uncomment These next Two Line for Pi Camera
# camSet='nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 !  appsink'
# cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
cam=cv2.VideoCapture(0,cv2.CAP_V4L2)
while True:
    ret, frame = cam.read()
    # cv2.imshow('nanoCam',frame)
    if goFlag == 1:
        frame = cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,0),2)
        roi = frame[y1:y2,x1:x2]
        cv2.imshow('Copy ROI', roi)
        cv2.moveWindow('Copy ROI',750,0)
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()