from flask import Flask, Response, render_template
from turbo_flask import Turbo
import threading
import pickle, cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import time

AI_PATH = '../aslkeys.ai'

def load_ai():
    with open(AI_PATH, "rb") as f:
        return pickle.load(f)

labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'del', 'space', 'nothing']
KNN = load_ai()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # Open the webcam #! CHANGE THE CAMERA INDEX IF DOESN'T WORK
detector = HandDetector(detectionCon=0.8, maxHands=1)  # Create a hand detector


def gen_frames() -> bytes:
    """Reads every frame from the camera and yields it

    Yields:
        bytes: Image from the camera with html stuff to display camera frame properly
    """
    while True:
        _, frame = cap.read()  # read the camera frame
        detector.findHands(frame, draw=True)
        ret, buffer = cv2.imencode('.jpg', frame) # encode the frame to jpeg
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
app = Flask(__name__)

@app.route('/video', methods=['GET'])
def video() -> Response:
    """Responses with the camera frame stream

    Returns:
        flask.wrappers.Response: Stream of camera frames
    """
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['GET'])
def index() -> str:
    """Homepage of the application

    Returns:
        str: HTML page with the camera stream and asl classification result
    """
    return render_template('index.html')

@app.route('/clasify_hand', methods=['GET'])
def clasify_hand() -> str:
    """Reads frame from the camera and uses aslkeys.ai to classify the sign language character

    Returns:
        str: Labels of the sign language character from the camera with their probabilities separated one from each other by new lines
    """
    ret, frame = cap.read()  # Read camera frame
    try:
        hands = detector.findHands(frame, draw=False)  # Find a hand
        # if it is left hand
        if (hands and hands[0] and hands[0]['type'] == 'Left'):
            mirror_frame = cv2.flip(frame, 1)
            hands = detector.findHands(mirror_frame, draw=False)  # Find a hand
    except cv2.error as e:
        print(e)
        return 'nothing 100%'

    if not (hands and hands[0]):  # if no hands found
        return 'nothing 100%'

    x, y, w, h = hands[0]['bbox']  # Get the bounding box
    # cx, cy = hands[0]['center']

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
    return prediction

if __name__ == '__main__':
    app.run(debug=True)