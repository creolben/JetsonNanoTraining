import cv2
print(cv2.__version__)
# dispW=1280
# dispH=720
flip=2
#Uncomment These next Two Line for Pi Camera
# camSet='nvarguscamerasrc wbmode=3 tnr-mode=2 tnr-strength=1 ee-mode=2 ee-strength=1 !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! videobalance contrast=1.5 brightness=-.2 saturation=1.2 !  appsink'
# cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
cam=cv2.VideoCapture(0,cv2.CAP_V4L2)
dispW = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
dispH = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
BW = int(.25*dispW)
BH = int(.25*dispH)
posX = 10
posY = 100
dx = 5
dy = 5

while True:
    ret, frame = cam.read()
    frame = cv2.rectangle(frame,(posX,posY),(posX+BW,posY+BH),(255,0,0),-1)
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    posX = posX+dx
    posY = posY+dy
    if (posX + BW >= dispW) or (posX  <= 0) :
        dx = dx *(-1)
    if (posY + BH >= dispH - BH) or (posY  <= 0) :
        dy = dy *(-1)
       
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()