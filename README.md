# Docker Events Notifier 
Receive Slack notifications when a container dies

## How it works
This image connects to the host machine socket, through a volume mapping, and listen [Docker Events API](https://docs.docker.com/engine/reference/api/docker_remote_api_v1.24/#/monitor-dockers-events).

When a `die` event is triggered it sends the affected container's information to the selected Slack channel.  


## Build

```shell
docker build \
    -t docker-events-notifier:$VERSION \
    -t docker-events-notifier .
```

## Run
1. Because this app is just for you, you'll be fine with  a [Slack Tokens for Testing and Development](https://api.slack.com/docs/oauth-test-tokens)

#### Single docker engine
Run the container on a single docker engine, using slack api key and channel.

```shell
docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e SLACK_API_KEY="xoxp-9999999999-9999999999-9999999999-99999999999999999999999" \
    -e SLACK_CHANNEL="#foo" \
    socialmetrix/docker-events-notifier:$VERSION
```

#### Docker swarm mode
Run the container on every node of your swarm.

```shell
docker service create \
    --mode global \
    --restart-condition any \
    --mount type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
    -e SLACK_API_KEY="xoxp-9999999999-99999999999-999999999999-99999999999999999999999999999999" \
    -e SLACK_CHANNEL="#foo" \
    --name docker-events-notifier \
    socialmetrix/docker-events-notifier:$VERSION
```

## License
Apache License Version 2.0

