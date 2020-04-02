import os
from helpers import request_teamcity, check_for_agent, get_queue_info

baseUrl = 'http://localhost:8111/app/rest'
queueUrl = f'{baseUrl}/buildQueue'
token = os.getenv('TOKEN')
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/xml',
}

queueList = get_queue_info(queueUrl=queueUrl, headers= headers)

if len(queueList.builds) > 0:
    for buildInfo in queueList.builds.build:
        removed = check_for_agent(
            queueUrl=queueUrl, buildId=buildInfo['id'], headers=headers)
        print(removed)
else:
    print('No builds in the queue')
