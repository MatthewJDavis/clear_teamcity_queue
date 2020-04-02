import os
from helpers import check_for_agent, get_queue_info

BASEURL = 'http://localhost:8111/app/rest'
QUEUEURL = f'{BASEURL}/buildQueue'
TOKEN = os.getenv('TOKEN')
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/xml',
}

QUEUE = get_queue_info(queueUrl=QUEUEURL, headers=HEADERS)

if len(QUEUE.builds) > 0:
    for buildInfo in QUEUE.builds.build:
        removed = check_for_agent(
            queueUrl=QUEUEURL, buildId=buildInfo['id'], headers=HEADERS)
        print(removed)
else:
    print('No builds in the queue')
