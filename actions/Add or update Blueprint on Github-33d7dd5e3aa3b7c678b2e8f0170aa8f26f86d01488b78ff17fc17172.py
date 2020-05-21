from github import Github
import json
import yaml 
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(context, inputs):
    '''
    Get secrets 
    '''
    github_token = get_secrets(inputs['region_name'],inputs['githubToken'])
    
    bp_json = inputs['bp_version_content']
    # convert content in yaml
    bp_content = yaml.safe_load(bp_json['content'])
    # get the blueprint name
    bp_name = bp_json['name']
    # Update the yaml version to match the submitted version
    bp_content['version'] = bp_json['version']
    # Add or update the bp Name
    bp_content['name'] = bp_name
    print(bp_content)

    g = Github(github_token)

    # repo = g.get_repo("americanbwana/gitpython-play")
    repo = g.get_repo(inputs['githubRepo'])
    # See if bluprint.yaml exists in the BP directory.  If so, then update the content.  Otherwise create a new directory and save bp_content as blueprint.yaml
    try:
        existing_bp = repo.get_contents(bp_name+"/blueprint.yaml")
        print("This blueprint folder already exists.  Updating the content")
        repo.update_file(existing_bp.path, bp_json['versionDescription'], yaml.dump(bp_content, sort_keys=False), existing_bp.sha ,branch="master")
        outputs ={"bp_github": "Github version updated"}
    except:
        print("File does not exist. Creating folder and uploading blueprint.yaml")
        repo.create_file(bp_name+"/blueprint.yaml", bp_json['versionDescription'], yaml.dump(bp_content, sort_keys=False), branch="master")
        outputs ={"bp_github": "New Github version created"}


def get_secrets(region,ssm_parameter):
 
    # Create a Secrets Manager client
    session = boto3.session.Session()
    ssm = session.client(
        service_name='ssm',
        region_name=region)
    
    parameterSecret = ssm.get_parameter(Name=ssm_parameter, WithDecryption=True)
    return parameterSecret['Parameter']['Value']

