@echo off

cd server

echo "Running bat for aslearn installation is deprecated, please use dockerfile"

echo "Installing python libs..."
pip install -r requirements.txt

echo "Running app.py"
python app.py

pause