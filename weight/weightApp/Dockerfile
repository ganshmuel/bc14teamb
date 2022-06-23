FROM python:3.6

EXPOSE 8081

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY weightApp.py /app
CMD python weightApp.py
