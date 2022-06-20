test with curl:  

POST /provider  
creates a new provider record, request must include a 'name' parameter 

```curl -H "Content-Type: application/json" -d '{"name":"roy"}' -X POST http://127.0.0.1:5000/provider  ```

PUT /provider/id  
Update existing provider name  

```curl -H "Content-Type: application/json" -d '{"name":"roy"}' -X PUT http://127.0.0.1:5000/provider/420```

Try without a name, see what you get:  

```curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/provider/420```

Empty name:  

```curl -H "Content-Type: application/json" -d '{"name":""}' -X POST http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: application/json" -d '{"name":""}' -X PUT http://127.0.0.1:5000/provider/420```

Wrong request type:  

```curl -H "Content-Type: application/json" -d '{"name":""}' -X DELETE http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: application/json" -d '{"name":""}' -X DELETE http://127.0.0.1:5000/provider/420```

Wrong content type:  

```curl -H "Content-Type: text/xml" -d '{"name":""}' -X DELETE http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: text/xml" -d '{"name":""}' -X DELETE http://127.0.0.1:5000/provider/420```
