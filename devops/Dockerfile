FROM python:latest
RUN apt-get --yes update
RUN apt-get --yes install ca-certificates curl gnupg lsb-release
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt-get --yes update
RUN apt-get --yes install docker-ce docker-ce-cli containerd.io docker-compose-plugin
RUN pip3 install flask
RUN apt-get --yes install jq
WORKDIR /server

ENTRYPOINT [ "python3", "flaskApp.py"]
 

