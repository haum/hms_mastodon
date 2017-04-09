import logging

from mastodon import Mastodon

from hms_mastodon import settings, strings


def get_logger():
    return logging.getLogger(__name__)


class HmsMastodon:
    """A class that provides features around the Mastodon wrapper."""

    def __init__(self):
        """Default constructor."""
        self.mastodon = Mastodon(
            settings.CLIENT_CREDS_FILE,
            access_token=settings.USER_CREDS_FILE,
            api_base_url=settings.API_BASE_URL
        )

    def toot_new_status(self, data):
        """Toots the new status of the space."""
        if data['is_open']:
            message = strings.TWAUM_OPEN
        else:
            message = strings.TWAUM_CLOSED

        get_logger().info("Sending new status toot: {}".format(message))
        self.mastodon.toot(message)