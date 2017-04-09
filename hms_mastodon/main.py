import logging

import coloredlogs

from hms_base.client import Client
from hms_base.decorators import topic

from hms_mastodon import settings
from hms_mastodon.mastodon import HmsMastodon


def get_logger():
    return logging.getLogger(__name__)


def main():
    """Entry point of the program."""

    # Logging
    coloredlogs.install(level='INFO')

    # Connect to Rabbit
    rabbit = Client('hms_mastodon', settings.RABBIT_EXCHANGE,
                    settings.RABBIT_ROUTING_KEYS)
    rabbit.connect(settings.RABBIT_HOST)

    # Mastodon
    mastodon = HmsMastodon()

    # Register callback for spacestatus broadcast messages
    @topic('spacestatus.broadcast')
    def on_spacestatus_broadcast(client, topic, dct):
        mastodon.toot_new_status(dct)

    rabbit.listeners.append(on_spacestatus_broadcast)

    # Start service
    get_logger().info("Starting passive consumming...")
    rabbit.start_consuming()
