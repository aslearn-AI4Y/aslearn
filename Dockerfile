FROM python:3.9

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 openssh-server -y
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication/PasswordAuthentication/' /etc/ssh/sshd_config
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd


ADD ./server/ ./server/ 
WORKDIR /server

RUN pip install -r requirements.txt


EXPOSE 80
EXPOSE 22
