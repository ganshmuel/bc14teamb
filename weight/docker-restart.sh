#!/bin/bash
docker-compose down
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -aq)
docker-compose up
