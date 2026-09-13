import json
import os
import urllib.request
import boto3

ssm = boto3.client("ssm")

def get_bot_token():
    resp = ssm.get_parameter(
        Name="/streamingapp/telegram-bot-token",
        WithDecryption=True
    )
    return resp["Parameter"]["Value"]

def handler(event, context):
    bot_token = get_bot_token()
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    for record in event["Records"]:
        sns_message = record["Sns"]
        subject = sns_message.get("Subject", "StreamingApp notification")
        message = sns_message.get("Message", "")

        text = f"*{subject}*\n{message}"

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = json.dumps({
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req) as response:
                print(f"Telegram response: {response.status}")
        except Exception as e:
            print(f"Failed to send Telegram message: {e}")
            raise

    return {"statusCode": 200}