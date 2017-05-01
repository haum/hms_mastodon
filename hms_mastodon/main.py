import logging
from threading import Thread

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

    def stream():
        mastodon.init_streaming(rabbit)

    streaming_thread = Thread(target=stream)
    streaming_thread.setDaemon(True)

    streaming_thread.start()

    # Register callback for spacestatus broadcast messages
    @topic('spacestatus.broadcast')
    def on_spacestatus_broadcast(client, topic, dct):
        mastodon.toot_new_status(dct)

    # Register callback for toot
    @topic('mastodon.toot')
    def on_mastodon_toot(client, topic, dct):
        mastodon.toot(dct['message'])

    rabbit.listeners.append(on_spacestatus_broadcast)
    rabbit.listeners.append(on_mastodon_toot)

    # Start service
    get_logger().info("Starting passive consumming...")
    rabbit.start_consuming()
