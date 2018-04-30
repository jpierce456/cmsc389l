import json
import boto3
import datetime

def start_session(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    # print(str(event))
    # print('Type of event' + str(type(event)))
    # for k, v in event.items():
    #     print('Key: ' + str(k) + ' \tValue: ' + str(v))
    
    sns_client = boto3.client('sns')
    dynamodb_client = boto3.client('dynamodb')
    now = datetime.datetime.now()
    future = now + datetime.timedelta(seconds=30)
    message_text = 'Received ' + event['clickType'] + ' from pomodoro button ' + event['serialNumber'] + ' at time ' + str(now)
    
    dynamodb_response = dynamodb_client.put_item(
        TableName='IncomingMessages',
        Item={
            'Click Type': {
                "S": str(event['clickType']),
            },
            'Message Send Time': {
                "S": str(future)
            },
        }
    )        
    sbs_response = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:120317662445:PomodoroButtonSNSTopic',
        Message=message_text,
    )

    return 0