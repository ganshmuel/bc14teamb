#/bin/bash

docker build -t flask-server:v1 . && \
docker run --rm -d --name test-server -p 8090:5000 -v $(pwd)/server-config-files:/server flask-server:v1