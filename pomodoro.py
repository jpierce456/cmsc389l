import json
import boto3
import datetime
import time

def start_session(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    # print(str(event))
    # print('Type of event' + str(type(event)))
    # for k, v in event.items():
    #     print('Key: ' + str(k) + ' \tValue: ' + str(v))
    
    sns_client = boto3.client('sns')
    dynamodb_client = boto3.client('dynamodb')
    now = datetime.datetime.now()
    session_type = ''
    length = 0
    if (event['clickType'] == 'SINGLE'):
        session_type = 'work session'
        length = 25
    elif (event['clickType'] == 'DOUBLE'):
        session_type = 'short break'
        length = 5
    elif (event['clickType'] == 'LONG'):
        session_type = 'long break'
        length = 15
    else:
        session_type = 'invalid'
        length = -1
    future = now + datetime.timedelta(minutes=length)
    # future = now + datetime.timedelta(seconds=0)
    message_text = 'You are beginning a ' + session_type + '. '
    message_text += 'I will notify you in ' + str(length) + ' minutes.'
    
    scan_response = dynamodb_client.scan(
        TableName='IncomingMessages',    
    )
    print(str(scan_response))
    for item in scan_response['Items']:
        print('item key: ' + item['Click Type']['S'])
        dynamodb_client.delete_item(
            TableName='IncomingMessages',
            Key={
                'Click Type': {
                    'S': item['Click Type']['S'],
                }
            } 
        )
    
    ttl = int(future.strftime('%s'))
    dynamodb_response = dynamodb_client.put_item(
        TableName='IncomingMessages',
        Item={
            'Click Type': {
                'S': str(event['clickType']),
            },
            'Message Send Time': {
                'S': str(now)
            },
            'TTL': {
                'S': str(ttl)
            }
        }
    )        
    sns_response = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:120317662445:PomodoroButtonSNSTopic',
        Message=message_text,
    )

    return 0