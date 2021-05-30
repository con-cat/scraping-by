import logging

import requests
from django.conf import settings


def post_message_to_slack(message: str):
    if settings.SLACK_URL is not None:
        requests.post(
            settings.SLACK_URL,
            json={"text": message},
        )
    else:
        logging.warning("Couldn't post to Slack - SLACK_URL env var not set")
