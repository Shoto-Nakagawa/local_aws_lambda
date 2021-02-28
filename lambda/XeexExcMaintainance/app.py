import json
import boto3
import uuid
from boto3.dynamodb.conditions import Attr,Key
import time
from decimal import Decimal
from EXCLog import XEEX_EXC_Log_Insert

# Decimal を JSON に変換
def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def lambda_handler(event, context):
    event_body = ""
    try:
        if event["httpMethod"] == "POST":
            event_body = XEEX_EXC_Insert(event)
        elif event["httpMethod"] == "GET":
            event_body = json.dumps(XEEX_EXC_Query(event),default=decimal_default_proc)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "succeeded",
                "data": event_body
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
    if "Local" in event_body and event_body["Local"] == True:
        # ローカル環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://XEEX-EXC-Dynamodb:8000")
    else:
        # AWS環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb")

    # 対象テーブルの情報を取得
    table = dynamodb.Table("XEEX-EXC-Maintainance")

    # UUID生成、登録データ（json）に追加
    event_body['UUID'] = str(uuid.uuid4())
    
    # 現在時刻の取得、登録データ（json）に追加
    event_body['Date'] = int(time.time() * 1000)

    # パラメータ情報を対象のテーブルに登録
    table.put_item(Item=event_body)

    # ログテーブルにデータ追加
    XEEX_EXC_Log_Insert(event_body)

    return event_body


def XEEX_EXC_Query(event):
    # パラメータ情報 取得
    event_body = json.loads(event["body"])
    
    # dynamodb = boto3.resource("dynamodb", endpoint_url="http://XEEX-EXC-Dynamodb:8000")
    # ローカル判断
    if "Local" in event_body and event_body["Local"] == True:
        # ローカル環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb", endpoint_url="http://XEEX-EXC-Dynamodb:8000")
    else:
        # AWS環境のDynamoDBを選択
        dynamodb = boto3.resource("dynamodb")

    # 対象テーブルの情報を取得
    table = dynamodb.Table("XEEX-EXC-Maintainance")

    # DynamoDBへのquery処理実行
    response = table.query(KeyConditionExpression=Key("UUID").eq(event_body["UUID"]))
    Items = response["Items"]

    return Items

