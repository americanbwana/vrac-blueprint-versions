import json
import logging
import requests
import boto3


logger = logging.getLogger()
logger.setLevel(logging.INFO)

VRAC_API_URL = "https://api.mgmt.cloud.vmware.com"

def handler(context, inputs):
    '''
    Get secrets 
    '''
    vrac_refresh_token = get_secrets(inputs['region_name'],inputs['refreshToken'])
    
    ''' 
    get vRAC bearer_token
    work around as the context does not contain auth information for this event
    context.request is responding with Not authenticated
    '''
    bearer_token = get_vrac_bearer_token(vrac_refresh_token)

    outputs = {}
    outputs['bearer_token'] = bearer_token
    return outputs


def get_secrets(region,ssm_parameter):
 
    # Create a Secrets Manager client
    session = boto3.session.Session()
    ssm = session.client(
        service_name='ssm',
        region_name=region)
    
    parameterSecret = ssm.get_parameter(Name=ssm_parameter, WithDecryption=True)
    return parameterSecret['Parameter']['Value']


def get_vrac_bearer_token(vrac_refresh_token):
    url = VRAC_API_URL + "/iaas/api/login"
    payload = { "refreshToken": vrac_refresh_token }
    result = requests.post(url = url, json = payload)
    result_data = result.json()
    bearer_token = result_data["token"]
    return bearer_token