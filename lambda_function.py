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
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def post_to_slack():
    # Set your slack url
    slack_webhook_url  = 'https://hooks.slack.com/services/XXXXXXXXXX/XXXXXXXXXXXX/XXXXXXXXXXXXXXXXXX'

    # Set your goofy messages for slack to announce the coffee
    message_list = [
        'Someone just started a fresh pot of  :coffee:',
        'The Joe will be ready in a few minutes',
        'Lennart probably just put some more coffee on to brew',
        'You know you want some coffee... it will be ready in 5 minutes'
    ]

    slack_data = {'text': random.choice(message_list)}
    response = requests.post(
        slack_webhook_url, data=json.dumps(slack_data),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        logger.error('Request to slack returned an error %s, the response is:\n%s'% (response.status_code, response.text))
    else:
        logger.info('Slack sent successfully')


def post_sumo_metrics():
    # Set your slack url
    sumo_collector_url = "https://endpoint1.collection.eu.sumologic.com/receiver/v1/http/XXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # Set your Sumo headers appropriately
    headers = {
        'X-Sumo-Category': "your/sourceCatetory/seattleCoffeePot",
        'X-Sumo-Host': "coffepot.example.org",
        'Content-Type': "application/vnd.sumologic.prometheus"
    }

    # payload is a brute force Prometheus metric
    payload = "# HELP pot_of_coffee_brewed Count of pots brewed\n# TYPE pot_of_coffee_brewed counter\npot_of_coffee_brewed{reason=\"coffee\"} 1 %s"%(time.time())

    response = requests.request("POST", sumo_collector_url, data=payload, headers=headers)

    if response.status_code != 200:
        logger.error('Sumo metrics post returned an error %s, the response is:\n%s'% (response.status_code, response.text))
    else:
        logger.info('Sumo metrics sent successfully')

def lambda_handler(event, context):
    logger.info('Received event: ' + json.dumps(event))
    post_to_slack()
    post_sumo_metrics()


