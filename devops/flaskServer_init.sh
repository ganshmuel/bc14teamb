#/bin/bash
docker stop ci-server
docker build -t ci-server:v2 . && \
docker run --rm -d --name ci-server -p 8090:5000 \
-v /var/run/docker.sock:/var/run/docker.sock  \
-v /test-env:/test-env \
-v $(pwd)/exec-files/:/test-env/exec-files \
-v /home/ubuntu/.ssh:/root/.ssh \
-v $(pwd)/compose-config-files/:/test-env/compose-config-files \
-v $(pwd)/server-config-files:/server ci-server:v2
