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
    event_body["Complete"] = 0
    event_body["State"] = 0
    event_body["Date"] = event["Date"]
    event_body["Local"] = event["Local"]

    # 項目「UUID」が存在しない場合
    if "UUID" not in event_body:
        # UUID生成、登録データ（json）に追加
        event_body['UUID'] = str(uuid.uuid4())

    if "Content" in event_body:
        del event_body["Content"]


    # ローカル判断
    if "Local" in event_body and event_body["Local"] == True:
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
    if "Local" in event_body and event_body["Local"] == True:
        # ローカル環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://XEEX-EXC-Dynamodb:8000")
    else:
        # AWS環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb")

    # 対象テーブルの情報を取得
    table = dynamodb.Table("XEEX-EXC-Data")

    # DynamoDBへのquery処理実行
    response = table.query(KeyConditionExpression=Key("UUID").eq(event_body["UUID"]),
                           FilterExpression=Attr('Content').contains(event_body["Content"] if "Content" in event_body else "" ))
    Items = response["Items"]

    return Items

