import unittest
from unittest.mock import Mock

from hms_mastodon.mastodon import HmsMastodon
from hms_mastodon.strings import TWAUM_CLOSED, TWAUM_OPEN


class MastodonTests(unittest.TestCase):
    def setUp(self):
        self.mastodon = HmsMastodon()
        self.mastodon.mastodon = Mock()
        self.mastodon.mastodon.toot = Mock()
        self.mocked_toot = self.mastodon.mastodon.toot

    def test_toot_new_status_open(self):
        data = {'is_open': True}

        # Check that we tooted when the status changed
        self.mastodon.toot_new_status(data)
        self.mocked_toot.assert_called_once_with(TWAUM_OPEN)

    def test_toot_new_status_closed(self):
        data = {'is_open': False}

        # Check that we tooted when the status changed
        self.mastodon.toot_new_status(data)
        self.mocked_toot.assert_called_once_with(TWAUM_CLOSED)

    def test_toot(self):
        self.mastodon.toot('test')
        self.mocked_toot.assert_called_once_with('test')