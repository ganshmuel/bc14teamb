test with curl:  

POST /provider  
creates a new provider record, request must include a 'name' parameter 

curl -H "Content-Type: application/json" -d '{"name":"roy"}' -X POST http://127.0.0.1:5000/provider  

PUT /provider/id  
Update existing provider name  

curl -H "Content-Type: application/json" -d '{"name":"roy"}' -X PUT http://127.0.0.1:5000/provider/420
