import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    try:
        event_body = json.loads(event["body"])
        # ローカル判断
        if "local" in event_body and event_body["local"] == True:
            # ローカル環境のDynamoDBを選択
            dynamodb = boto3.resource("dynamodb", endpoint_url="http://XEEX-EXC-Dynamodb:8000")
        else:
            # AWS環境のDynamoDBを選択
            dynamodb = boto3.resource("dynamodb")

        # 対象テーブルの情報を取得
        table = dynamodb.Table("XEEX-EXC-Data")
        # パラメータ情報を対象のテーブルに登録
        table.put_item(Item=event_body)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "succeeded",
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": e.args
            }),
    }