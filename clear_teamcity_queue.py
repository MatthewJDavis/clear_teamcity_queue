import os
import requests
from requests.exceptions import HTTPError
import untangle

baseUrl = 'http://localhost:8111/app/rest'
queueUrl = f'{baseUrl}/buildQueue'
token = os.getenv('TOKEN')
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/xml',
}

def request_teamcity(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')
    return response

# remove from queue
def remove_builds(buildId):
    try:
        data = "<buildCancelRequest comment='No agents' readdIntoQueue='false' />"
        headers = {
            'Content-Type': 'application/xml',
            'Authorization': f'Bearer {token}',
        }
        buildUrl = f'{queueUrl}/id:{buildId}'
        response = requests.post(buildUrl, data=data, headers=headers)
        response.raise_for_status()
        print(response.content)
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Another error occurred {err}')

# Check if build has an agent and delete if not
def check_for_agent(queueUrl, buildId):
    agentUrl = f'{queueUrl}/id:{buildId}/compatibleAgents'
    agentInfo = request_teamcity(agentUrl)
    xml = agentInfo.content.decode()
    agent = untangle.parse(xml)
    if agent.agents['count'] == '0':
        remove_builds(buildId)


response = request_teamcity(queueUrl)
xml = response.content.decode()
queueList = untangle.parse(xml)

for buildInfo in queueList.builds.build:
    check_for_agent(queueUrl=queueUrl, buildId=buildInfo['id'])





