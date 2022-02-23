import cv2
import mediapipe as mp
import time
import serial

arduino=serial.Serial("/dev/cu.usbmodem143301",9600)
#ensure that the port matches arduino
#second argument is setting baud rate

print(arduino.name)


class handDetector():
    def __init__(self,mode=False,maxHands=3,detectionCon=0.5,trackCon=0.5):
        self.mode=mode
        self.maxHands=maxHands
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        #variable
        #general parameters of the hands class. see the documations of Hands
        self.mpHands = mp.solutions.hands  # taking the hands model from the google mediapipe
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)  # write parameters inside the brackets
        # write nothing because using the default parameters (see what those are)
        self.mpDraw = mp.solutions.drawing_utils
        # provided that draws points on your hand
        #^ just initializing the class

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:  # if multiple hands are detected
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    #only draw if true
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)  # wont draw on RGB
                    # extract information from each hand
        return img

    def findPosition(self,img,handNo=0,draw=True):

        lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]

            for id, lm in enumerate(myHand.landmark):
                # gets info from each hand
                # each hand has numbered landmarks and its x,y,z coodinates are printed
                # for example the tip of your thumb has a landmark and so on
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                 # position of the centre landmark x*w landmark y*h
                # height width and channel

                lmList.append([id,cx,cy])
                # basically gives the x and y coordinates of each landmark
                # will print for all 20 landmarks
                 # therefore print id as well
                 # then you can use certain IDs for certain tasks
                if draw:
                    cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)
        return lmList





    #dummy code to showcase what the module can do
    #basically you can copy the code below to run in a different project
def main():

    pTime = 0  # previous time
    cTime = 0  # current time
    # used to track the FPS
    cap = cv2.VideoCapture(0)
    detector=handDetector() #default parameters already set

    while True:
        success, img = cap.read()
        img=detector.findHands(img,draw=False)
        lmList=detector.findPosition(img,draw=False)
        #find position method returns a list of hand positions
        if len(lmList) !=0:
            print(lmList[8])
            x='X'+str((lmList[8][1]))
            y='Y'+str((lmList[8][2]))
            print(x)
            print(y)
            arduino.write(bytes(x, 'utf-8'))
            arduino.write(bytes(y, 'utf-8'))
            #index 1 is x
            #index 2 is y
            #where land mark 4 is the tip of the thumb
            # 8 is the finger tip


        # for calculating fps
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime  # previoustime becomes current time
        img = detector.findHands(img)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                    (255, 0, 255), 3)
        # prints text on the image instead of the console
        # need to convert fps to a string and also round it
        # the rest is just the font, scale colour and thickness
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__=="__main__":
    main()