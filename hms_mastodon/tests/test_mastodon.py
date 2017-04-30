import unittest
from unittest.mock import Mock

from hms_mastodon.mastodon import HmsMastodon
from hms_mastodon import strings


class MastodonTests(unittest.TestCase):
    def setUp(self):
        self.mastodon = HmsMastodon()
        self.mastodon.mastodon = Mock()
        self.mastodon.mastodon.status_post = Mock()
        self.mocked_status_post = self.mastodon.mastodon.status_post

    def test_toot_new_status_open(self):
        data = {'is_open': True}

        # Check that we tooted when the status changed
        self.mastodon.toot_new_status(data)
        self.mocked_status_post.assert_called_once_with(
            strings.TWAUM_OPEN, spoiler_text=strings.TWAUM_OPEN_SHORT)

    def test_toot_new_status_closed(self):
        data = {'is_open': False}

        # Check that we tooted when the status changed
        self.mastodon.toot_new_status(data)
        self.mocked_status_post.assert_called_once_with(
            strings.TWAUM_CLOSED, spoiler_text=strings.TWAUM_CLOSED_SHORT)

    def test_toot(self):
        self.mastodon.toot('test')
        self.mocked_status_post.assert_called_once_with('test')