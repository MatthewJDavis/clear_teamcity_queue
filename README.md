# Clear TeamCity queue

Python script to remove builds from the build queue.

TeamCity [API docs]

Uses [poetry] to manage dependencies.

```bash
poetry install
```

docker.txt file has docker command to run TeamCity locally for testing.

Working on:
Removes builds that have no agents that they can run on.

[API docs]: https://www.jetbrains.com/help/teamcity/rest-api.html
[poetry]: https://python-poetry.org/