#/bin/bash

docker stop ci-server
docker build -t flask-server:v1 . && \
docker run  --rm -d --name ci-server -p 8090:5000 \
-v /var/run/docker.sock:/var/run/docker.sock  \
-v $(pwd)/exec-files/:/test-env/exec-files \
-v $(pwd)/key:/root/.ssh \
-v $(pwd)/server-config-files:/server flask-server:v1
