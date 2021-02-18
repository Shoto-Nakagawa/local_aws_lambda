import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr,Key
import time
from decimal import Decimal

# Decimal を JSON に変換
def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def XEEX_EXC_Log_Insert(event):
    # ログに必要なデータ整理
    event_body = event
    event_body["UUID"] = event["UUID"]
    event_body["Complete"] = 0
    event_body["State"] = 0
    event_body["Date"] = event["Date"]
    event_body["local"] = event["local"]

    del event_body["content"]

    # ローカル判断
    if "local" in event_body and event_body["local"] == True:
        # ローカル環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://XEEX-EXC-Dynamodb:8000")
    else:
        # AWS環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb")

    # 対象テーブルの情報を取得
    table = dynamodb.Table("XEEX-EXC-Log")
    
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
    response = table.query(KeyConditionExpression=Key("UUID").eq(event_body["UUID"]),
                           FilterExpression=Attr('content').contains(event_body["content"] if "content" in event_body else "" ))
    Items = response["Items"]

    return Items

