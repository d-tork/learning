# Docker Notes

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

## As a development environment
```dockerfile
FROM <python image>
RUN <build and compile, optional?>
WORKDIR /app
COPY . .
RUN <pip install --production> (or setup.py... these are your dependencies)
CMD <?>
```
But to keep the container running and still edit code, mount your source code in a bind mount:
```bash
docker run -dp 3000:3000 -w /app -v '$(pwd):/app" image \
	sh -c "pip install . && run dev"
```
where `-d` is detached (run in background), `-p` to map ports, `-w` the working directory, `-v`
the volume mount.

## Layer Caching
Since dependencies don't change often, copy just the requirements.txt (or environment.yaml) file
early on and create the venv. Later, copy the whole app dir. Don't forget to .dockerignore the 
`venv/` dir so it doesn't get overwritten in the `COPY . .` step later!


## Environment variables
The docker-compose can override env values set in the Dockerfile.

## Connecting to a running mysql container
```bash
docker exec -it brankerdb mysql -uroot -p
```
where `brankerdb` is the container name, `-uroot` is specifying that the user is "root" and `-p` is
going to prompt you for a password entry.
