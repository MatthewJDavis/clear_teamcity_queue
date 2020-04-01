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

def request_teamcity(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')
    return response

# remove from queue
def remove_builds(buildId, headers):
    try:
        data = "<buildCancelRequest comment='No agents' readdIntoQueue='false' />"
        buildUrl = f'{queueUrl}/id:{buildId}'
        response = requests.post(buildUrl, data=data, headers=headers)
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Another error occurred {err}')

# Check if build has an agent and delete if not
def check_for_agent(queueUrl, buildId):
    agentUrl = f'{queueUrl}/id:{buildId}/compatibleAgents'
    agentInfo = request_teamcity(agentUrl,headers)
    xml = agentInfo.content.decode()
    agent = untangle.parse(xml)
    if agent.agents['count'] == '0':
        response = remove_builds(buildId,headers)
        removed = untangle.parse(response.content.decode())
        return (f"Removed build: {removed.build.buildType['webUrl']}")


response = request_teamcity(queueUrl,headers)
xml = response.content.decode()
queueList = untangle.parse(xml)

if len(queueList.builds) > 0:
    for buildInfo in queueList.builds.build:
        check_for_agent(queueUrl=queueUrl, buildId=buildInfo['id'])
else:
    print('No builds in the queue')




