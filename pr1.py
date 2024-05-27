import cv2
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self , pos , width , height , value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self , img):
        cv2.rectangle(img , self.pos, (self.width + self.pos[0] , self.height + self.pos[1]) , (255,255,255) , cv2.FILLED)
        cv2.rectangle(img , self.pos , (self.width + self.pos[0] , self.height + self.pos[1]) , (55,55,55) , 3)
        cv2.putText(img , self.value , (self.pos[0]+20 , self.pos[1]+80) , cv2.FONT_HERSHEY_PLAIN, 3 , (55,55,55) , 3)

    def click(self , x , y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.width:
            cv2.rectangle(img , self.pos, (self.width + self.pos[0] , self.height + self.pos[1]) , (255,255,255) , cv2.FILLED)
            cv2.rectangle(img , self.pos , (self.width + self.pos[0] , self.height + self.pos[1]) , (55,55,55) , 3)
            cv2.putText(img , self.value , (self.pos[0]+20 , self.pos[1]+80) , cv2.FONT_HERSHEY_PLAIN, 5 , (0,0,0) , 5)

            return True
        else:
            return False
        
cap = cv2.VideoCapture(1)
cap.set(3 , 1280)
cap.set(4 , 720)
detector = HandDetector(detectionCon=0.8 , maxHands=1)


#Creating button
buttonvalues = [['7','8','9','*'],
                ['4','5','6','-'],
                ['1','2','3','+'],
                ['.','0','/','=']]
buttonlist = []
for x in range(4):
    for y in range(4):
        xpos = x*100 +700
        ypos = y*100+150
        buttonlist.append(Button((xpos, ypos) , 100 , 100 , buttonvalues[y][x]))

#Variables

myeq = ''
delaycounter = 0

while True:
    #IMage from webcam
    success , img = cap.read()
    img = cv2.flip(img , 1)

    #Hands detection
    hands , img = detector.findHands(img , flipType=False)

    #Draw the button 
    cv2.rectangle(img ,(700 , 50), (800+300 , 100+70) , (255,255,255) , cv2.FILLED)
    cv2.rectangle(img , (700 , 50), (800+300 , 100+70) , (55,55,55) , 3)

    for button in buttonlist:
        button.draw(img)


    #Check for hand
    if hands:
        lmlist = hands[0]['lmList']
        
        length , _ , img = detector.findDistance(lmlist[8][:2] , lmlist[12][:2] , img)
        if length < 35:
            x,y = lmlist[8][:2]
            for i , button in enumerate(buttonlist):
                if button.click(x,y) and delaycounter==0:
                    val = (buttonvalues[int(i%4)][int(i/4)])
                    if val == "=":
                        myeq = str(eval(myeq))
                    else:
                        myeq += val
                    delaycounter=1
    #Avoid Duplicate
    if delaycounter!=0:
        delaycounter+=1
        if delaycounter>10:
            delaycounter=0

    #Display the result/equation
    cv2.putText(img , myeq , (710 , 120) , cv2.FONT_HERSHEY_PLAIN, 3 , (55,55,55) , 3)

    cv2.imshow("Image" , img)

    key = cv2.waitKey(1)
    if key == ord('x'):
        break