import os
from helpers import request_teamcity, check_for_agent, get_queue_info

BASEURL = 'http://localhost:8111/app/rest'
QUEUEURL = f'{BASEURL}/buildQueue'
TOKEN = os.getenv('TOKEN')
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/xml',
}

queueList = get_queue_info(queueUrl=QUEUEURL, headers=HEADERS)

if len(queueList.builds) > 0:
    for buildInfo in queueList.builds.build:
        removed = check_for_agent(
            queueUrl=QUEUEURL, buildId=buildInfo['id'], headers=HEADERS)
        print(removed)
else:
    print('No builds in the queue')
