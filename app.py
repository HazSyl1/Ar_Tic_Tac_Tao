from flask import Flask,render_template,Response, jsonify , request
import cv2 as cv 
from main import serve , Button
import numpy as np
import base64
from flask_cors import CORS
from cvzone.HandTrackingModule import HandDetector
app=Flask(__name__)
CORS(app)

global detect
detect= HandDetector(detectionCon=0.9, maxHands=1)
global ListVal
ListVal= [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
global count
count= [1]
global butList
butList= [Button((x * 100 + 800, y * 100 + 150), 100, 100, ListVal[y][x]) for x in range(3) for y in range(3)]
global delayCounter
delayCounter= 0
global flag
flag= 0
global win
win= 0
global end_frame
end_frame=None
@app.route('/process_frame',methods=['POST'])
def process_frame():
    global flag, win, count, butList, ListVal, delayCounter,end_frame 
    try:
        
        file=request.files['frame']
        file_byte=np.frombuffer(file.read(),np.uint8)
        frame=cv.imdecode(file_byte,cv.IMREAD_COLOR)
        
        if(win!=0):
            if(end_frame==None):
                frame, win, flag ,delayCounter= serve(frame, detect, butList, count, flag, ListVal, win, delayCounter)
                if(win!=3):
                    cv.putText(frame, "Player "+str(win)+" Won!!", (810, 500), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                else:
                    cv.putText(frame, "It's a Tie!!", (810, 500), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
                _,buffer=cv.imencode('.jpg',frame)
                processed_frame=base64.b64encode(buffer).decode('utf-8')
                end_frame=processed_frame
            return jsonify(success=True, frame =end_frame)
        
        frame, win, flag ,delayCounter= serve(frame, detect, butList, count, flag, ListVal, win, delayCounter)
        # print("GOT PROCESSED FILE")
        _,buffer=cv.imencode('.jpg',frame)
        processed_frame=base64.b64encode(buffer).decode('utf-8')
        
        
        return jsonify(success=True, frame =processed_frame),200
    except Exception as e:
        print(e)
        return jsonify(success=False,message=str(e)), 400
        

@app.route('/')
def index():
    # return "Starting"
    return render_template('index.html')


@app.route('/reset', methods=['POST'])
def reset():
    global ListVal, count, delayCounter, flag, win, end_frame,butList
    ListVal = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    count = [1]
    delayCounter = 0
    flag = 0
    win = 0
    end_frame = None
    butList= [Button((x * 100 + 800, y * 100 + 150), 100, 100, ListVal[y][x]) for x in range(3) for y in range(3)]
    return jsonify(success=True)


if __name__=="__main__":
    app.run(debug=True)