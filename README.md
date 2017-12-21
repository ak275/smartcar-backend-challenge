# smartcar-backend-challenge

REST API

A simple python-based API using flask.

INSTALL

pip install -r requirements.txt

RUN

python smartcar_api.py

TEST CASES

1) Vehicle Info
$ curl http://127.0.0.1:5000/vehicles/1234 -X GET                                          
$ curl http://127.0.0.1:5000/vehicles/1235 -X GET

2) Security
$ curl http://127.0.0.1:5000/vehicles/1234/doors -X GET                                    
$ curl http://127.0.0.1:5000/vehicles/1235/doors -X GET                                                                                         

3) Fuel Range
$ curl http://127.0.0.1:5000/vehicles/1234/fuel -X GET                                     
$ curl http://127.0.0.1:5000/vehicles/1235/fuel -X GET                                                                                         

4) Battery Range
$ curl http://127.0.0.1:5000/vehicles/1234/battery -X GET                                                        
$ curl http://127.0.0.1:5000/vehicles/1235/battery -X GET

5) Engine Action
$ curl http://127.0.0.1:5000/vehicles/1234/engine -X POST -H 'Content-Type: application/json' -d '{"action" : "START"}'  
$ curl http://127.0.0.1:5000/vehicles/1234/engine -X POST -H 'Content-Type: application/json' -d '{"action" : "STOP"}
$ curl http://127.0.0.1:5000/vehicles/1235/engine -X POST -H 'Content-Type: application/json' -d '{"action" : "START"}'                         
$ curl http://127.0.0.1:5000/vehicles/1235/engine -X POST -H 'Content-Type: application/json' -d '{"action" : "STOP"}'    
 




