#/bin/bash

docker stop ci-test-server
docker build -t flask-server:v1 . && \
docker run  --rm -d --name ci-test-server -p 8089:5000 \
-v /var/run/docker.sock:/var/run/docker.sock  \
-v $(pwd)/exec-files/:/test-env/exec-files \
-v /home/ubuntu/.ssh/:/root/.ssh \
-v $(pwd)/compose-config-files/:/test-env/compose-config-files \
-v $(pwd)/server-config-files:/server flask-server:v1
