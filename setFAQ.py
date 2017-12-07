import boto3
from botocore.exceptions import ClientError
import urllib2
import os

def setter_handler(event, context):
        params = event.get('body-json', '').split('&')
 
        event_params = {}
        for param in params:
            key_value = param.split('=')
            event_params[key_value[0]] = key_value[1]
            
        if event_params.get('channel_id', '') != os.environ['CHANNEL_ID']:
            return "You don't have permission to do that"
            
        key_value = event_params.get('text', '').split('%3A%3A%3A')
        
        response = "Failed."
        if len(key_value) == 2:
            faq_key = key_value[0]
            faq_response = urllib2.unquote(key_value[1]).replace('+', ' ')
            
            # Setup Dynamo connection
            dynamodb = boto3.resource('dynamodb', region_name='us-west-1')
            table = dynamodb.Table('SlackFAQ')
        
        
            table.put_item(
               Item={
                    'key': faq_key,
                    'response': faq_response,
                }
            )
            
            response = "Successfully set {} to {}".format(faq_key, faq_response)

        return { "response_type": "in_channel", "text": response}
