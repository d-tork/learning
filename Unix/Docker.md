# Docker

## Concise `ps` output
From [docker ps - Formatting](https://docs.docker.com/engine/reference/commandline/ps/#formatting)
```bash
docker ps --format "table {{.Names}}\t{{.RunningFor}}\t{{.State}}\t{{.Status}}\t{{.Ports}}" -a
```

## Following logs
For a container named `jira`:
```bash
docker logs -f jira

docker-compose logs -f jira
```
