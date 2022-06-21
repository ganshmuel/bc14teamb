FROM python:3-alpine3.16

ENV FLASK_APP=app
ENV FLASK_ENV=development

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections
# Since Flask apps listen to port 5000  by default, we expose it

EXPOSE 8081

# Sets the working directory for following COPY and CMD instructions
# Notice we haven’t created a directory by this name - this instruction 
# creates a directory with this name if it doesn’t exist

WORKDIR /app

# Update Python

RUN python3 -m pip install --upgrade pip setuptools wheel

# Install any needed packages specified in requirements.txt

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app

ENTRYPOINT [ "python3", "app.py" ]
