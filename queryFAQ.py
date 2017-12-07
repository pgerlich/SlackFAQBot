import boto3
import json
from botocore.exceptions import ClientError

def query_handler(event, context):
        params = event.get('body-json', '').split('&')
        
        event_params = {}
        for param in params:
            key_value = param.split('=')
            event_params[key_value[0]] = key_value[1]

        message = event_params.get('text', '')

        # Setup Dynamo connection
        dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
        table = dynamodb.Table('BloomBotFAQ')
        
        response = 'I don\'t know about that.'
        if message:
                # Query for response
                try:
                    faq_options_response = table.get_item(Key={'key': message})
                except ClientError as e:
                    print(e.response['Error']['Message'])
                else:
                    response_item = faq_options_response.get('Item')
                    response = response_item['response'] if response_item else response

        return { "response_type": "in_channel", "text": response}
