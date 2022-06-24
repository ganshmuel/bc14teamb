FROM python:3-alpine3.16

ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV USER=app_user
ENV HOME /home/$USER

RUN adduser -D $USER

WORKDIR $HOME

# The EXPOSE instruction indicates the ports on which a container 
# will listen for connections

EXPOSE 8080

# Update Python

RUN python3 -m pip install --upgrade pip setuptools wheel; \
    apk add --no-cache curl

# Install any needed packages specified in requirements.txt

COPY --chown=$USER ./app/requirements.txt ./app/requirements.txt

RUN pip install --no-cache-dir -r ./app/requirements.txt

COPY --chown=$USER ./app/app.py ./app/app.py

# the INTERNAL port of the app, inside the container

ENV INTERNAL_APP_PORT=8080
ENV WEIGHT_HOST=3.68.253.241

HEALTHCHECK --timeout=2s CMD curl --fail http://localhost:${INTERNAL_APP_PORT}/health || exit 1

USER $USER

ENTRYPOINT [ "python3", "./app/app.py" ]