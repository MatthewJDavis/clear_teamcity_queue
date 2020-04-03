import requests
from requests.exceptions import HTTPError
import untangle


def request_teamcity(url, headers):
    ''' Helper function to connect to TeamCity API '''
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    return response


def get_queue_info(queue_url, headers):
    ''' Returns TeamCity queue information as parsed XML '''
    response = request_teamcity(queue_url, headers)
    xml = response.content.decode()
    return untangle.parse(xml)


def remove_builds(queue_url, build_id, headers):
    ''' Removes builds when no agents available '''
    try:
        data = "<buildCancelRequest \
                comment = 'No available agents to run build.'\
                readdIntoQueue='false' />"
        build_url = f'{queue_url}/id:{build_id}'
        response = requests.post(build_url, data=data, headers=headers)
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')


def check_for_agent(queue_url, build_id, headers):
    ''' Checks to see if the build has agents to run on '''
    agent_url = f'{queue_url}/id:{build_id}/compatibleAgents'
    agent_info = request_teamcity(agent_url, headers)
    xml = agent_info.content.decode()
    agent = untangle.parse(xml)
    if agent.agents['count'] == '0':
        response = remove_builds(queue_url, build_id, headers)
        removed = untangle.parse(response.content.decode())
        return f"Removed build: {removed.build.buildType['webUrl']}"
    return 'Build has agents to run on.'
