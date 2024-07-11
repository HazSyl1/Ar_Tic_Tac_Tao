import time
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value
    
    def draw(self, frame):
        cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (202, 150, 225), cv.FILLED)
        cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 225), 4)
        cv.putText(frame, self.value, (self.pos[0] + 28, self.pos[1] + 74), cv.FONT_HERSHEY_PLAIN, 5, (220, 0, 50), 6)

    def clickCheck(self, frame, x, y):
        if self.pos[0] < x < self.pos[0] + self.width and self.pos[1] < y < self.pos[1] + self.height:
            cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 73), cv.FILLED)
            cv.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (0, 0, 50), 4)
            cv.putText(frame, self.value, (self.pos[0] + 28, self.pos[1] + 74), cv.FONT_HERSHEY_PLAIN, 5, (50, 50, 25), 6)
            return True
        return False

def check_win(ListVal, flag):
    if ((ListVal[0][0] == ListVal[0][1] == ListVal[0][2] != ' ' or 
         ListVal[1][0] == ListVal[1][1] == ListVal[1][2] != ' ' or 
         ListVal[2][0] == ListVal[2][1] == ListVal[2][2] != ' ' or 
         ListVal[0][0] == ListVal[1][0] == ListVal[2][0] != ' ' or 
         ListVal[0][1] == ListVal[1][1] == ListVal[2][1] != ' ' or 
         ListVal[0][2] == ListVal[1][2] == ListVal[2][2] != ' ' or 
         ListVal[0][0] == ListVal[1][1] == ListVal[2][2] != ' ' or 
         ListVal[0][2] == ListVal[1][1] == ListVal[2][0] != ' ')):
        if flag == 0:
            return 1, "Player 1 Won!!"
        if flag == 1:
            return 2, "Player 2 Won!!"
    elif all(cell != ' ' for row in ListVal for cell in row):
        return 3, "It's a Tie!!"
    return 0, ""

def serve(frame, detect, butList, count, flag, ListVal, win, delayCounter):
    frame = cv.flip(frame, 1)
    hand, frame = detect.findHands(frame, flipType=False)

    # Drawing background
    cv.rectangle(frame, (750, 20), (1150, 550), (255, 255, 255), cv.FILLED)
    cv.putText(frame, "*Tic Tac Toe*", (830, 80), cv.FONT_HERSHEY_TRIPLEX, 1, (122, 25, 255), 3)

    if flag == 0:
        cv.putText(frame, "Player 1 Turn", (842, 140), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)
    if flag == 1:
        cv.putText(frame, "Player 2 Turn", (842, 140), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)

    for button in butList:
        button.draw(frame)

    if hand:
        lmList = hand[0]['lmList']
        length, info, frame = detect.findDistance(lmList[8][:2], lmList[12][:2], frame)
        x, y = lmList[8][:2]

        if length < 30:
            for i, button in enumerate(butList):
                if button.clickCheck(frame, x, y) and delayCounter == 0:
                    if flag == 0:
                        ListVal[int(i % 3)][int(i / 3)] = 'O'
                        delayCounter = 1
                        button.value = 'O'
                    if flag == 1:
                        ListVal[int(i % 3)][int(i / 3)] = 'X'
                        delayCounter = 1
                        button.value = 'X'
                    count.append(1)
                    win, msg = check_win(ListVal, flag)
                    if win != 0:
                        cv.putText(frame, msg, (810, 500), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    flag = 1 if len(count) % 2 == 0 else 0

    if delayCounter != 0:
        delayCounter += 1
        if delayCounter > 14:
            delayCounter = 0

    return frame, win, flag, delayCounter