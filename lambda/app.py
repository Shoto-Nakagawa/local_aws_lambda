import json
import boto3
import os
from datetime import datetime
import uuid
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    try:
        event_body = ""
        if event["httpMethod"] == "POST":
            event_body = XEEX_EXC_Insert(event)
        elif event["httpMethod"] == "GET":
            event_body = XEEX_EXC_Query(event)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "succeeded",
                "data":event_body
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": e.args,
                "event": event
            }),
    }


def XEEX_EXC_Insert(event):
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

    # UUID生成、登録データ（json）に追加
    event_body['UUID'] = str(uuid.uuid4())

    # パラメータ情報を対象のテーブルに登録
    table.put_item(Item=event_body)

    return event_body


def XEEX_EXC_Query(event):
    # パラメータ情報 取得
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

    # DynamoDBへのquery処理実行
    queryData = table.get_item(Key={'UUID': "0d318d6a-d2ad-4551-b45c-7c56f002c7c3"})

    return queryData

