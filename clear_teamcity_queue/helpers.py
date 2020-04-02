import requests
from requests.exceptions import HTTPError
import untangle


def request_teamcity(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')
    return response


def get_queue_info(queueUrl, headers):
    response = request_teamcity(queueUrl, headers)
    xml = response.content.decode()
    return untangle.parse(xml)

# remove from queue
def remove_builds(queueUrl, buildId, headers):
    try:
        data = "<buildCancelRequest comment='No available agents to run build.' readdIntoQueue='false' />"
        buildUrl = f'{queueUrl}/id:{buildId}'
        response = requests.post(buildUrl, data=data, headers=headers)
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Another error occurred {err}')

# Check if build has an agent and delete if not
def check_for_agent(queueUrl, buildId, headers):
    agentUrl = f'{queueUrl}/id:{buildId}/compatibleAgents'
    agentInfo = request_teamcity(agentUrl, headers)
    xml = agentInfo.content.decode()
    agent = untangle.parse(xml)
    if agent.agents['count'] == '0':
        response = remove_builds(queueUrl, buildId, headers)
        removed = untangle.parse(response.content.decode())
        return (f"No available agents to run build. Removed build: {removed.build.buildType['webUrl']}")
