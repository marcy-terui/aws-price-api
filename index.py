# -*- coding: utf-8 -*-

import json
import requests

API_BASE_URL = 'https://pricing.us-east-1.amazonaws.com'
LIST_API_PATH = '/offers/v1.0/aws/index.json'

def lambda_handler(event, contect):
    res = requests.get('{}{}'.format(API_BASE_URL, LIST_API_PATH))
    api_list = json.load(res.text)

    offer = event.get('offer')
    offer_code = None
    offer_path = None
    for k,v in api_list['offers'].items():
        if k == offer:
            offer_code = v['offerCode']
            offer_path = v['currentVersionUrl']
