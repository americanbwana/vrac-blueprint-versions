import json
import requests
import logging

'''
Get the content when a blueprint is versioned
bearer_token will come from another action as part of a flow
The BP is in YAML.  So will need to convert the JSON into YAML at some point
'''

logger = logging.getLogger()
logger.setLevel(logging.INFO)

VRAC_API_URL = "https://api.mgmt.cloud.vmware.com"

def handler(context, inputs):
    outputs = {}
    outputs['bp_version_content'] = get_blueprint_version_content(inputs)
    return outputs

def get_blueprint_version_content(inputs):
    '''
    inputs['bearer_token'] will come from another action in the flow
    '''
    url = VRAC_API_URL + "/blueprint/api/blueprints/" + inputs['blueprintId'] +"/versions/" + inputs['id']
    logger.info(url)
    headers = {"Authorization": "Bearer " + inputs['bearer_token']}
    logger.info("Sending the request ...")
    result = requests.get(url, headers=headers)
    logger.info(result.text)
    result_data = result.json()
    # content = result_data["content"]
    # logger.info(content)
    logger.info("Getting ready to return ... ")
    return result_data
