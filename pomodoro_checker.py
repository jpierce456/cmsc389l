import datetime
import json
import boto3

def pomodoro_checker(event, context):
    # print("Received event: " + json.dumps(event, indent=2))
    sns_client = boto3.client('sns')
    dynamodb_client = boto3.client('dynamodb')
    now = datetime.datetime.now()
    print('current time: ' + str(now))
    
    scan_response = dynamodb_client.scan(
        TableName='IncomingMessages',    
    )
        
    if scan_response['Items']:
        click_type = ''
        send_time = 0
    
        for item in scan_response['Items']:
            click_type = item['Click Type']['S']
            send_time = int(item['TTL']['S'])
            start_time = item['Message Send Time']['S']
            
    
        print('click_type: ' + click_type)
        print('ttl: ' + str(send_time))
        
        cur_time = int(now.strftime('%s'))
        
        if (cur_time >= send_time):
            # send message, delete entry from db
            session_type = ''
            if (click_type == 'SINGLE'):
                session_type = 'work session'
            elif (click_type == 'DOUBLE'):
                session_type = 'short break'
            elif (click_type == 'LONG'):
                session_type = 'long break'
            message_text = 'Your ' + session_type + ' is over!'
            sns_response = sns_client.publish(
                TopicArn='arn:aws:sns:us-east-1:120317662445:PomodoroButtonSNSTopic',
                Message=message_text,
            )
            dynamodb_client.delete_item(
                TableName='IncomingMessages',
                Key={
                    'Click Type': {
                        'S': click_type,
                    },
                },
            )
            
            dynamodb_client.put_item(
                TableName='StudyData',
                Item={
                    'Start Time': {
                        'S': start_time,
                    },
                    'End Time': {
                        'S': str(now),
                    },
                    'Session Type': {
                        'S': session_type,
                    }
                }
            )