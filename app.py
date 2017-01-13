# Copyright 2016 Socialmetrix
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function

import docker
from slackclient import SlackClient
import os
import sys
import time
import signal
import socket

slack_token = None
slack_channel = None

APP_NAME = 'Docker Events Notifier'


def get_config(env_key):
    value = os.getenv(env_key)
    if not value:
        print('Environment variable {} is missing. Can\'t continue'.format(env_key))
        sys.exit(1)
    return value


def watch_and_notify_events():
    event_filters = {"event": "die"}

    client = docker.DockerClient(base_url='unix://var/run/docker.sock')

    for event in client.events(filters=event_filters, decode=True):
        container_id = event['Actor']['ID'][:12]
        attributes = event['Actor']['Attributes']
        when = time.strftime('%Y-%m-%d %H:%M:%S %Z', time.localtime(event['time']))

        message = ":rotating_light:  At _{}_ your container *{}* (_{}_) died. Image: *{}* Exit Code: *{}* Origin: *{}*" \
            .format(when,
                    attributes['name'],
                    container_id,
                    attributes['image'],
                    attributes['exitCode'],
                    socket.gethostname())

        send_message(slack_channel, message)


def send_message(channel, message):
    global slack_token
    global slack_channel

    sc = SlackClient(slack_token)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message
    )
    pass


def exit_handler(_signo, _stack_frame):
    send_message(slack_channel,
                 ':disappointed: *{}* received *SIGTERM* on _{}_. Goodbye!'.format(APP_NAME, socket.gethostname()))
    sys.exit(0)


if __name__ == '__main__':
    slack_token = get_config("SLACK_API_KEY")
    slack_channel = get_config("SLACK_CHANNEL")

    signal.signal(signal.SIGTERM, exit_handler)
    signal.signal(signal.SIGINT, exit_handler)

    message = ':bulb: *{}* reporting for duty on _{}_. '.format(APP_NAME, socket.gethostname()) + \
              '  Alerts will be sent to this channel.'

    send_message(slack_channel, message)

    watch_and_notify_events()
