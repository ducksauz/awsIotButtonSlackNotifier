'''
This is an example of how to send data to Slack webhooks in Python with the
requests module.
Detailed documentation of Slack Incoming Webhooks:
https://api.slack.com/incoming-webhooks

'''

from __future__ import print_function

import boto3
import json
import logging
from botocore.vendored import requests
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    webhook_url = 'https://hooks.slack.com/services/XXXXXXXXXX/XXXXXXXXXXXX/XXXXXXXXXXXXXXXXXX'
    message_list = [
        'Someone just started a fresh pot of  :coffee:',
        'The Joe will be ready in a few minutes',
        'Lennart probably just put some more coffee on to brew',
        'You know you want some coffee... it will be ready in 5 minutes'
        ]

    slack_data = {'text': random.choice(message_list)}
    logger.info('Received event: ' + json.dumps(event))
    response = requests.post(
        webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        logger.error('Request to slack returned an error %s, the response is:\n%s'% (response.status_code, response.text))
    else:
        logger.info('Slack sent successfully')

