
docker-run:
	docker run --network ddb-network --name dynamodb -p 8000:8000 amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb

docker-start:
	docker start dynamodb

start:
	sam local start-api --docker-network ddb-network

create:
	aws dynamodb create-table --cli-input-json file://./db/XEEX-EXC-Data.json --endpoint-url http://localhost:8000

delete:
	aws dynamodb delete-table --table-name XEEX-EXC-Data --endpoint-url http://localhost:8000

build:
	sam build
