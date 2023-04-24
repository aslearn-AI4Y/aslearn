FROM python:3.9

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

WORKDIR /server

COPY ./server /server

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]
