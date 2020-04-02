import os
from helpers import check_for_agent, get_queue_info

BASE_URL = 'http://localhost:8111/app/rest'
QUEUE_URL = f'{BASE_URL}/buildQueue'
TOKEN = os.getenv('TOKEN')
HEADERS = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/xml',
}

QUEUE = get_queue_info(queue_url=QUEUE_URL, headers=HEADERS)

if len(QUEUE.builds) > 0:
    for buildInfo in QUEUE.builds.build:
        removed = check_for_agent(
            queue_url=QUEUE_URL, build_id=buildInfo['id'], headers=HEADERS)
        print(removed)
else:
    print('No builds in the queue')
