import logging

from mastodon import Mastodon
from mastodon.streaming import StreamListener

import attr
from bs4 import BeautifulSoup

from hms_mastodon import settings, strings


def get_logger():
    return logging.getLogger(__name__)


@attr.s
class Mention:
    """Class that stores useful data from mentions"""
    user = attr.ib()
    url = attr.ib()
    visibility = attr.ib()
    text_content = attr.ib()

    @staticmethod
    def from_notification(notification):
        """Parse useful data from a notification into a mention."""
        text_content = BeautifulSoup(
            notification['status']['content'], 'html.parser').text

        return Mention(
            user=notification['status']['account']['acct'],
            url=notification['status']['url'],
            visibility=notification['status']['visibility'],
            text_content=text_content
        )


class TootStreamListener(StreamListener):
    def __init__(self, rabbit):
        """Default constructor."""
        self.rabbit = rabbit

    def on_notification(self, notification):
        """Handle Mastodon notifications."""

        get_logger().info(
            "Received streaming notification: {}".format(notification))

        # If the notification is a mention
        if notification['type'] == 'mention':
            mention = Mention.from_notification(notification)
            get_logger().info("Parsed notification: {}".format(mention))

            self.rabbit.publish(
                "mastodon.mention", attr.asdict(mention))


class HmsMastodon:
    """A class that provides features around the Mastodon wrapper."""

    def __init__(self):
        """Default constructor."""
        self.mastodon = Mastodon(
            settings.CLIENT_CREDS_FILE,
            access_token=settings.USER_CREDS_FILE,
            api_base_url=settings.API_BASE_URL
        )
        self.listener = None

    def init_streaming(self, rabbit):
        """Initialize the Mastodon streaming API."""
        self.listener = TootStreamListener(rabbit)
        self.mastodon.user_stream(self.listener)

    def toot_new_status(self, data):
        """Toots the new status of the space."""
        if data['is_open']:
            short_msg = strings.TWAUM_OPEN_SHORT
            long_msg = strings.TWAUM_OPEN
        else:
            short_msg = strings.TWAUM_CLOSED_SHORT
            long_msg = strings.TWAUM_CLOSED

        get_logger().info("Sending new status toot: {}".format(short_msg))
        self.mastodon.status_post(long_msg, spoiler_text=short_msg)

    def toot(self, message):
        """Send a toot."""
        get_logger().info("Sending toot: {}".format(message))
        self.mastodon.status_post(message)