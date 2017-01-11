# Docker Events Notifier 
Receive Slack notifications when a container dies

##How it works
This image connects to the host machine socket, through a volume mapping, and listen [Docker Events API](https://docs.docker.com/engine/reference/api/docker_remote_api_v1.24/#/monitor-dockers-events).

When a `die` event is triggered it sends the affected container's information to the selected Slack channel.  


## Build

```shell
docker build \
    -t docker-events-notifier:0.5 \
    -t docker-events-notifier .
```


## Run
1. Because this app is just for you, you'll be fine with  a [Slack Tokens for Testing and Development](https://api.slack.com/docs/oauth-test-tokens)

1. Run the container passing `SLACK_API_KEY` and `SLACK_CHANNEL` parameters

```shell
docker run \
    -d --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -e SLACK_API_KEY="xoxp-9999999999-9999999999-9999999999-9999999999e6c9999999999" \
    -e SLACK_CHANNEL="#foo" \
    docker-events-notifier
```

## License
Apache License Version 2.0

