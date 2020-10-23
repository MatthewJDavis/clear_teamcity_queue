# Clear TeamCity queue

Python script to remove builds from the build queue.

TeamCity [API docs]

Uses [poetry] to manage dependencies.

```bash
workon tc_queue # virtual env
poetry install
```

To run:
```bash
workon tc_queue # virtual env
python clear_teamcity_queue/clear_teamcity_queue.py 
```

## Testing locally

docker-compose file for server to run locally.

```bash
docker-compose up
```

docker.txt file has docker command to run TeamCity agent.

[API docs]: https://www.jetbrains.com/help/teamcity/rest-api.html
[poetry]: https://python-poetry.org/