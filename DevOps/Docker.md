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

### Debugging a failed build by running intermediate layers
https://docs.docker.com/develop/develop-images/multistage-build/#stop-at-a-specific-build-stage

With a Dockerfile specifying intermediate stages like so:
```dockerfile
FROM python:3.9.13-slim-buster AS stage-01
VOLUME /data

FROM stage-01 AS stage-02
RUN pip3 install --upgrade pip setuptools

FROM stage-02 AS stage-03
WORKDIR /app
COPY . .

FROM stage-03 AS stage-04
RUN pip3 install .
```

but the build is failing at, say, `stage-04`, just build everything up to that point:
```bash
docker build --target stage-03 -t myapp:dev .
```

Then `docker images` reveals an image that you can interact with:
```bash
docker run --rm -it myapp:dev /bin/bash
```

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
