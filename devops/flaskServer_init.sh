#/bin/bash
docker stop ci-server
docker build -t ci-server:v2 . && \
docker run --rm -d --name ci-test-server -p ci-server 8080:5000 \
-v /var/run/docker.sock:/var/run/docker.sock  \
-v $(pwd)/exec-files/:/test-env/exec-files \
-v ~/.ssh:/root/.ssh \
-v $(pwd)/compose-config-files/:/test-env/compose-config-files \
-v $(pwd)/server-config-files:/server flask-server:v1
