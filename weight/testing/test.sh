#!/bin/bash
curl -s -I localhost:8081/health | grep HTTP/ | awk {'print '}
