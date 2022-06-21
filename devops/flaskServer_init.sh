#/bin/bash
docker stop flask-server
docker build -t flask-server:v1 . && \
docker run --rm -d --name flask-server -p 8090:5000 -v $(pwd)/../billing:/tests -v /var/run/docker.sock:/var/run/docker.sock  -v $(pwd)/server-config-files:/server flask-server:v1
