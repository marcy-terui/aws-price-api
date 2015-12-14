from __future__ import print_function

import json
import requests

API_BASE_URL = 'https://pricing.us-east-1.amazonaws.com'
LIST_API_PATH = '/offers/v1.0/aws/index.json'
RESULT_MAX_LENGTH = 100

def lambda_handler(event, contect):
    res = requests.get(API_BASE_URL + LIST_API_PATH)
    api_list = res.json()

    offer = event['offer']
    offer_code = None
    offer_path = None
    for k,v in api_list['offers'].items():
        if k == offer:
            offer_code = v['offerCode']
            offer_path = v['currentVersionUrl']
    if offer_path is None:
        raise Exception('offer {} is not exists.'.format(offer))

    res = requests.get(API_BASE_URL + offer_path)
    data_list = res.json()
    match_products = {}
    for sku, product in data_list['products'].items():
        match = True
        for cond in event['condition']:
            if product['attributes'].get(cond['key']) != cond['value']:
                match = False
        if match:
            match_products[sku] = {'product': product}
            if len(match_products) > RESULT_MAX_LENGTH:
                msg = 'Too many targets. Please change the conditions (<{})'.format(RESULT_MAX_LENGTH)
                raise Exception(msg)

    results = []
    for sku, product in match_products.items():
        product['price'] = []
        prices = data_list['terms'][event['term']].get(sku)
        if prices is not None:
            for price in prices.values():
                product['price'].append(price)
        results.append(product)

    return results

# lambda_handler({
#     'offer': 'AmazonEC2',
#     'term': 'OnDemand',
#     'condition': [{
#         'key': 'instanceType',
#         'value': 'm4.large'
#     },
#     {
#         'key': 'location',
#         'value': 'US West (Oregon)'
#     }]
# }, {})
