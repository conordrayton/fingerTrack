import cv2
import mediapipe as mp
import time

cap=cv2.VideoCapture(0)

mpHands = mp.solutions.hands #taking the hands model from the google mediapipe
hands = mpHands.Hands() #write parameters inside the brackets
#write nothing because using the default parameters (see what those are)

mpDraw=mp.solutions.drawing_utils
#provided that draws points on your hand

pTime=0 #previous time
cTime=0 #current time
#used to track the FPS

while True:
    success,img=cap.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    #hands class only uses RGB images so needs to be converted
    results= hands.process(imgRGB)
    #now just need to extract the info and use it
    #print(results.multi_hand_landmarks)
    #first print the results to see what we have (detect hands)
    #check for multiple hands

    if results.multi_hand_landmarks: #if multiple hands are detected
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                #gets info from each hand
                #each hand has numbered landmarks and its x,y,z coodinates are printed
                #for example the tip of your thumb has a landmark and so on
                #print(id,lm)
                h,w,c=img.shape
                cx,cy=int(lm.x*w), int(lm.y*h)
                #position of the centre landmark x*w landmark y*h
                #height width and channel
                print(id,cx,cy)
                #basically gives the x and y coordinates of each landmark
                #will print for all 20 landmarks
                #therefore print id as well
                #then you can use certain IDs for certain tasks
                if id==4:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)
                    #draws a purple circle around the first landmark (base of hand)



            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS) #wont draw on RGB

            #extract information from each hand

    #for calculating fps
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime #previoustime becomes current time

    cv2.putText(img,str(int(fps)),(10,70), cv2.FONT_HERSHEY_SIMPLEX,3,
        (255,0,255),3)
    #prints text on the image instead of the console
    #need to convert fps to a string and also round it
    #the rest is just the font, scale colour and thickness



    cv2.imshow("Image",img)
    cv2.waitKey(1)
    #basically run this code everytime to use a webcam


    #this will be converted into a module to be reused
    #take the data of each landmark which can be used to do whatever i want