

curl -s -I localhost:8080/health | grep HTTP/ | awk {' print $2 '}


