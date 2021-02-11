
# 1.DynamoDB-local用のコンテナ作成（コンテナ名：dynamodb）
docker-run:
	docker run --network XEEX-EXC-Network --name XEEX-EXC-Dynamodb -p 8000:8000 amazon/dynamodb-local -jar DynamoDBLocal.jar -sharedDb

# 2.dynamodbコンテナを実行
docker-start:
	docker start XEEX-EXC-Dynamodb 

# 3.テーブル作成（テーブル名：XEEX-EXC-Data）
create:
	aws dynamodb create-table --cli-input-json file://./db/XEEX-EXC-Data.json --endpoint-url http://localhost:8000

# 5.ビルド
build:
	sam build

# 6.Lambda・APIゲートウェイ起動
start:
	sam local start-api --docker-network XEEX-EXC-Network

# テーブル削除（テーブル名：XEEX-EXC-Data）
delete:
	aws dynamodb delete-table --table-name XEEX-EXC-Data --endpoint-url http://localhost:8000

