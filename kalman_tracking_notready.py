import numpy as np
import cv2
import time
import matplotlib.pyplot as plt
from numpy.linalg import inv

#from imutils.video import VideoStream

#picam = VideoStream(usePiCamera=True).start()

time.sleep(2.0)

 

def on_hue_changed(_=None):

    global mask
    global centroid_1
    global centroid_2
    #ower_r = cv2.getTrackbarPos('Lower r','mask')
    #lower_g = cv2.getTrackbarPos('Lower g','mask')
    #lower_b = cv2.getTrackbarPos('Lower b','mask')

 
    #upper_hue = cv2.getTrackbarPos('Upper Hue','mask')
    #lowerb = (lower_r,lower_g,lower_b)

    lowerb = (100,100,110)
    upperb = (255,255,255)

 

    mask = cv2.inRange(frame,lowerb,upperb)
    mask = ~mask
    mask = cv2.erode(mask,None)

    contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    for pts in contours:

        if cv2.contourArea(pts)<400:
            continue

        approx = cv2.approxPolyDP(pts,cv2.arcLength(pts,True)*0.02,True)
        vtc = len(approx)

        if vtc ==4:
            Label(frame,pts,'window detect')

            
    

 

 

def Label(img,pts,label):
    
    (x,y,w,h) = cv2.boundingRect(pts)
    pt1 = (x,y)
    pt2 = (x+w,y+h)
    cv2.rectangle(img,pt1,pt2,(255,0,0),1)
    centroid_1= int((x+x+w)/2)
    centroid_2 = int((y+y+h)/2)
    centroid = (centroid_1,centroid_2)
    cv2.circle(img,centroid,5,(255,255,255),2)
    cv2.putText(img,label,pt1,cv2.FONT_HERSHEY_PLAIN,1,(0,0,255))
    #estimate_loc = kalman_filter(centroid_1,centroid_2)
    """plt.subplot(2,2,1)
    plt.plot(t,estimate_loc[0])
    plt.title('estimate_x')
    plt.subplot(2,2,2)
    plt.plot(t,estimate_loc[2])
    plt.title('estimate_y')
    plt.subplot(2,2,3)
    plt.plot(t,centroid_1)
    plt.title('centroid_x')
    plt.subplot(2,2,4)
    plt.plot(t,centroid_2)
    plt.title('centorid_y')"""
    #picture = img[x:x+w,y:y+h]
    #cv2.imwrite("picture",picture)
    x.append(centroid_1)
    y.append(centroid_2)
    

 

 

def main():
    global frame
    global centroid_1
    global centroid_2
    global x
    global y
    x= []
    y = []
    cap = cv2.VideoCapture(0)
    #cap = picam.read()
    if not cap.isOpened():
        print("frame load failed")
        return

    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        #frame = picam.read()

        #frame = cv2.imread("frame.jpg")
        on_hue_changed(0)
        
        #cv2.createTrackbar('Lower r','mask',lower_r,255,on_hue_changed)
        #cv2.createTrackbar('Lower g','mask',lower_g,255,on_hue_changed)
        #cv2.createTrackbar('Lower b','mask',lower_b,255,on_hue_changed)

 

        #on_hue_changed(0)

 
        
        
        cv2.imshow("frame",frame)
        cv2.imshow("mask",mask)
        #cv2.imwrite("frame.jpg",frame)

    
        
        
        if cv2.waitKey(10) ==27:
            break

 

    cv2.destroyAllWindows()

 

"""def kalman_filter(xm,ym):
    dt = 0.1
    A = np.array([[1,dt,0,0], [0,1,0,0] ,[0,0,1,dt] ,[0,0,0,1]])
    H = np.array([[1,0,0,0], [0,0,1,0]])
    Q = 1.0 * np.eye(4)  #eye는 대각행렬
    R = np.array([[50,0], [0,50]])
    x= np.array([0,0,0,0]).transpose()
    P = 100 * np.eye(4)
    xp = np.dot(A,x)
    Pp = np.dot(np.dot(A,P), A.transpose()) + Q
    K = np.dot(Pp,H.transpose()),inv(np.dot(np.dot(H,Pp),H.transpose())+R)
    z = np.array([xm,ym])
    q = z-np.dot(H,xp)
    x = xp + np.dot(K,q)
    P = Pp - np.dot(np.dot(K,H),Pp)
    xh = x[0]
    yh = x[2]
    result = np.array([xh,yh])
    return result"""



 

if __name__ =='__main__':
    main()
