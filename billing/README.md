test with curl:  

POST /provider  
creates a new provider record, request must include a 'name' parameter 

```curl -H "Content-Type: application/json" -d '{"name":"roy"}' -X POST http://127.0.0.1:5000/provider  ```

PUT /provider/id  
Update existing provider name  

```curl -H "Content-Type: application/json" -d '{"name":"roy"}' -X PUT http://127.0.0.1:5000/provider/420```

Try without passing a name, see what you get:  

```curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: application/json" -X PUT http://127.0.0.1:5000/provider/420```

Empty name:  

```curl -H "Content-Type: application/json" -d '{"name":""}' -X POST http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: application/json" -d '{"name":""}' -X PUT http://127.0.0.1:5000/provider/420```

Wrong request type:  

```curl -H "Content-Type: application/json" -d '{"name":""}' -X DELETE http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: application/json" -d '{"name":""}' -X DELETE http://127.0.0.1:5000/provider/420```

Wrong content type:  

```curl -H "Content-Type: text/plain" --data "this is raw data" -X POST http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: text/plain" --data "this is raw data" -X PUT http://127.0.0.1:5000/provider/420```

Null values?  

```curl -H "Content-Type: application/json" -d '{"name":null}' -X POST http://127.0.0.1:5000/provider```  
```curl -H "Content-Type: application/json" -d '{"name":null}' -X PUT http://127.0.0.1:5000/provider/420```
