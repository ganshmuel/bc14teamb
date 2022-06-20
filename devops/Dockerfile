FROM python:latest
RUN pip3 install flask
WORKDIR /server
ENV FLASK_APP="/server/flaskApp.py"
ENTRYPOINT [ "python3", "flaskApp.py"]


