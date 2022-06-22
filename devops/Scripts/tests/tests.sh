#!/bin/bash
curl -s -I 3.68.253.241:8080/health | grep HTTP/ | awk {' print $2 '}
curl -s -I 3.68.253.241:8081/health | grep HTTP/ | awk {' print $2 '}
