import time

import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

cap=cv.VideoCapture(0)

cap.set(3,1280)
cap.set(4,720)
#maxHand
detect=HandDetector(detectionCon=0.9,maxHands=1)

class button:
    def __init__(self,pos,width,height,value):

        self.pos=pos
        self.width=width
        self.height=height
        self.value=value
    def draw(self,frame):

        cv.rectangle(frame, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),
                     (202, 150, 225), cv.FILLED)
        cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                     (50, 50, 225), 4  )
        #cv.rectangle(frame, (100, 100), (300, 300), (50, 50, 225), 4)

        cv.putText(frame, self.value, (self.pos[0]+28 , self.pos[1]+74),
                   cv.FONT_HERSHEY_PLAIN, 5, (220, 0, 50), 6)
        cv.putText(frame, "Press 'd' To End", (810,500), cv.FONT_HERSHEY_PLAIN,2, (0, 0, 0), 3)

    def clickCheck(self, x, y):

        # x1 < x < x1+width
        if self.pos[0] < x < self.pos[0] + self.width:
            if self.pos[1] < y < self.pos[1] + self.height:

                cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                             (255, 255, 73), cv.FILLED)
                cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height),
                             (0, 0, 50), 4)
                # cv.rectangle(frame, (100, 100), (300, 300), (50, 50, 225), 4)

                cv.putText(frame, self.value, (self.pos[0] + 28, self.pos[1] + 74),
                           cv.FONT_HERSHEY_PLAIN, 5, (50, 50, 25), 6)
                return True
            else:
                return False

win=0

def check_win():
    if( ( (ListVal[0][0]==ListVal[0][1]==ListVal[0][2]=='X' or ListVal[1][0]==ListVal[1][1]==ListVal[1][2]=='X' or ListVal[2][0]==ListVal[2][1]==ListVal[2][2]=='X' or ListVal[0][0]==ListVal[1][0]==ListVal[2][0]=='X' or  ListVal[0][1]==ListVal[1][1]==ListVal[2][1]=='X' or  ListVal[0][2]==ListVal[1][2]==ListVal[2][2]=='X' or  ListVal[0][0]==ListVal[1][1]==ListVal[2][2]=='X' or  ListVal[0][2]==ListVal[1][1]==ListVal[2][0]=='X')) or(ListVal[0][0]==ListVal[0][1]==ListVal[0][2]=='O' or ListVal[1][0]==ListVal[1][1]==ListVal[1][2]=='O' or ListVal[2][0]==ListVal[2][1]==ListVal[2][2]=='O' or ListVal[0][0]==ListVal[1][0]==ListVal[2][0]=='O' or  ListVal[0][1]==ListVal[1][1]==ListVal[2][1]=='O' or  ListVal[0][2]==ListVal[1][2]==ListVal[2][2]=='O' or  ListVal[0][0]==ListVal[1][1]==ListVal[2][2]=='O' or  ListVal[0][2]==ListVal[1][1]==ListVal[2][0]=='O')):
        if(flag==0):
            print("Player 1 Won!!")
            #cv.putText(frame, "Congo Player 1 Won !!!", (350, 360), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


        if(flag==1):
            print("Player 2 Won!!")
            #cv.putText(frame, "Congo Player 2 Won !!!", (350, 360), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        return 1

    else:
        if(len(count)>9):
            return 2
        return 0

ListVal=[[' ',' ',' '],
         [' ',' ',' '],
         [' ',' ',' ']]
count=[1]
butList=[]
for x in range(3):
    for y in range(3):

        xpos=x*100 +800
        ypos =y*100 +150
        butList.append(button((xpos,ypos),100,100,ListVal[y][x]))

delayCounter =0
flag = 0

while(True):
    #print(ListVal)
    #print('value=',butList[0].value)
    isTrue , frame = cap.read()

    frame=cv.flip(frame,1)

    hand , frame = detect.findHands(frame , flipType=False)

    #drawing bg
    cv.rectangle(frame,(750,20),(1150,550), (255, 255, 255), cv.FILLED)
    cv.putText(frame,"*Tic Tac Toe*",(830,80),cv.FONT_HERSHEY_TRIPLEX ,1,(122,25,255),3)


    if(flag==0):
        cv.putText(frame,"Player 1 Turn",(842,140),cv.FONT_HERSHEY_PLAIN, 2,(255,0,255),3)
    if(flag == 1):
        cv.putText(frame, "Player 2 Turn", (842, 140), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
    #cv.rectangle(frame, (300, 50), (600 , 300),
                 #(225, 255, 225), cv.FILLED)
    for button in butList:
        button.draw(frame)



   # for 0 and 1 for x
    if hand:
        lmList = hand[0]['lmList']
        # lank mark list , has all the points of out fingers

        length, info, frame = detect.findDistance(lmList[8][:2], lmList[12][:2], frame)
        # 8 is index and 12 is middle
        #print(length)if cv.waitKey(2) & 0xFF == ord('d'):
        x, y = lmList[8][:2]

        if length < 30:
            for i, button in enumerate(butList):
                if button.clickCheck(x, y) and delayCounter == 0:

                    #myVal = (ListVal[int(i % 3)][int(i / 3)])
                    if (flag==0 ):
                        ListVal[int(i % 3)][int(i / 3)]='O'
                        delayCounter = 1
                        button.value='O'
                    if(flag == 1):
                        ListVal[int(i % 3)][int(i / 3)]='X'
                        delayCounter = 1
                        button.value='X'
                    count.append(1)
                    win=check_win()
                    #print("win=",win)


    if(len(count)%2==0):
        flag=1
    else:
        flag=0





        # Avoid Duplicates
    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 14:
            delayCounter = 0

    if (win == 1 or win == 2):
        for button in butList:
            button.draw(frame)
        cv.imshow("LiveImage", frame)
        break

    cv.imshow("LiveImage",frame)

    if cv.waitKey(2) & 0xFF == ord('d'):
        for button in butList:
            button.draw(frame)
        break

cap.release()
cv.destroyAllWindows


#win=1
#print(win)

while(True):
    if(len(count)<9 and win==0):
        break
    #print(ListVal)
    #print('value=',butList[0].value)
    if(win==1):
        if(flag==1):
            image=cv.imread('download.png')
            cv.imshow('WON_Player_1',image)
        if (flag==0):
            image = cv.imread('download (1).png')
            cv.imshow('WON_Player_2', image)


    if(win==2):
        if(len(count)==9):
            break
        image = cv.imread("download (2).png")
        cv.imshow('TIE', image)
    #cv.waitKey(0)
    #time.sleep(5.5)

    if cv.waitKey(2) & 0xFF == ord('d'):
        break
cap.release()
cv.destroyAllWindows


