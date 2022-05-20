@echo off

echo "Installing python libs..."
pip install flask flask_cors opencv-python numpy cvzone pillow mediapipe scikit-learn

echo "Running app.py"
cd flask_server
python app.py