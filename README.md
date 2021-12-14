Prerequisits: 
Docker
AWS CLI
SAM CLI

#### comands to run docker network with a container with a dynamodb resource ###
$ docker network create sam-demo
$ docker run --network sam-demo --name dynamodb -d -p 8000:8000 amazon/dynamodb-local

#### create the table ###
$ aws dynamodb create-table `
--table-name carsTable `
--attribute-definitions AttributeName=id,AttributeType=N AttributeName=last_updated,AttributeType=S  `
--key-schema AttributeName=id,KeyType=HASH AttributeName=last_updated,KeyType=RANGE `
--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 `
--endpoint-url http://localhost:8000 

#### call this lambda locally to populate the table with sample data ###
$ sam local invoke LoadDataFunction --parameter-overrides ParameterKey=DDBTableName,ParameterValue=carsTable --docker-network sam-demo

#### check output from table to see if it is populated ###
$aws dynamodb scan --table-name carsTable --endpoint-url http://localhost:8000 

data to compare = 
"make","model","year","chassis_no" ,"id" ,"last_updated",”price”
"Nissan","Micra",2004,"12345A",1,"2017-02-01 00:00:00", 500.0
"Nissan","Micra",2004,"12425A",1,"2017-03-01 00:00:00", 400.0
"Ford","Fiesta",2002,"12345B",2,"2017-03-01 00:00:00", 300.0
"Audi","A3",,"12345C",3,"2017-04-01 00:00:00",
"Nissan","Micra",2004,"12345D",4,"2017-05-01 00:00:00", 200.0
"Peugeot" ,"308",1998,"12345E",5,"2017-06-01 00:00:00", 100.0

#### run local ApiGW ###
$ sam local start-api --parameter-overrides ParameterKey=DDBTableName,ParameterValue=carsTable --docker-network sam-demo

do a get on http://127.0.0.1:3000/car?id=1

