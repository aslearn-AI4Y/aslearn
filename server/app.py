from flask import Flask, render_template, request
import pickle
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import base64
import os

from PIL import Image
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})


AI_PATH = os.path.dirname(__file__) + '/aslearn.ai'

def load_ai():
    with open(AI_PATH, "rb") as f:
        return pickle.load(f)

KNN = load_ai()

labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'space', 'nothing']

detector = HandDetector(detectionCon=0.8, maxHands=1)  # Create a hand detector


@app.route('/logo.ico', methods=['GET'])
def get_favicon():
    return app.send_static_file('favicon.png')

@app.route('/', methods=['GET'])
def index() -> str:
    """Homepage of the application
    Returns:
        str: HTML page with the camera stream and asl classification result
    """
    return render_template('index.html')


@app.route('/drawhand', methods=['POST'])
def draw_hand():
    try:
        decodedBase64 = base64.b64decode(request.json['frame'].split(',')[1]) # decode the base64 string

        img = Image.open(BytesIO(decodedBase64)) # PIL image
        pixels = np.asarray(img, dtype='uint8')
        frame = pixels[:, :, ::-1].copy() # Convert to opencv format
        frame_copy = frame.copy()

        hands = detector.findHands(frame, draw=False) # detect the hand

        if (hands and hands[0]):
            # If it is left hand
            if (hands[0]['type'] == 'Left'):
                frame = cv2.flip(frame, 1) # mirror the frame
                hands = detector.findHands(frame, draw=False) # detect the hand

        detector.findHands(frame_copy, draw=True)

        retval, buffer = cv2.imencode('.png', frame_copy) # encode the frame to png and get buffer
        data = base64.b64encode(buffer).decode('utf-8') # encode the buffer to base64 and get string

        if not (hands and hands[0]):  # if no hands found
            return {'predection': 'nothing: 100%', 'frame': data}

        x, y, w, h = hands[0]['bbox']  # Get the bounding box

        x -= 20  # Move the bounding box to the center of the hand
        y -= 20  # Move the bounding box to the center of the hand
        w += 40  # Expand the bounding box
        h += 40  # Expand the bounding box

        if (w > h):  # if the width is greater than the height
            h = w  # Make the height the same as the width
        if (h > w):  # if the height is greater than the width
            w = h  # Make the width the same as the height

        hand_img = frame[y:y+h, x:x+w]  # Crop the hand out of the frame

        insertData = hands[0]['lmList']  # Get the landmarks

        for ins_data in insertData:  # move each landmark according to the bbox of the hand
            ins_data[0] -= x
            ins_data[1] -= y

        insertData = np.asarray(insertData).reshape(1, -1)  # reshape the landmarks to a 1D numpy array

        x1, y1, w1, h1 = hands[0]['bbox']  # Get the bounding box
        x1 -= x  # Move the bounding box according to the bbox of the hand
        y1 -= y  # Move the bounding box according to the bbox of the hand
        insertData = np.append(insertData, (x1, y1, w1, h1))  # Append the bounding box to the landmarks
        insertData = np.asarray(insertData).reshape(1, -1)  # reshape the bounding box to a 1D numpy array

        cx1, cy1 = hands[0]['center']  # Get the center
        cx1 -= x  # Move the center according to the bbox of the hand
        cy1 -= y  # Move the center according to the bbox of the hand
        insertData = np.append(insertData, (cx1, cy1))  # Append the center to the landmarks
        insertData = np.asarray(insertData).reshape(1, -1)  # reshape the center to a 1D numpy array

        insertData = np.append(insertData, hands[0]['type'] == 'Right')  # insert 1 if the hand is right, 0 if the hand is left

        predict = KNN.predict_proba([insertData])  # Predict the probability of each label

        predict = [int(i*100) for i in predict[0]]  # Convert the probabilities to integers
        precentageDict = {}
        for i, percentage in enumerate(predict):  # For each percentage
            if (percentage > 0.):
                precentageDict[labels[i]] = int(percentage)  # Add the label and the percentage to the dictionary
        precentageDict = {k: v for k, v in sorted(precentageDict.items(), key=lambda item: item[1], reverse=True)}  # Sort the dictionary by the percentage
        prediction = '\n'.join([key + ': ' + str(value) + '%' for key, value in precentageDict.items()])

        return {'predection': prediction, 'frame': data} # send the frame back to the client

    except cv2.error as e:
        print(e)
        return 'nothing 100%'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')