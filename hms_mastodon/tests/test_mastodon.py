import unittest
from unittest.mock import Mock

from hms_mastodon.mastodon import HmsMastodon, Mention
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


class MentionParserTest(unittest.TestCase):
    def test_parse_notification(self):
        notification = {
            'status': {
                'account': {
                    'acct': 'test@instance.mastodon'
                },
                'url': 'https://instance.mastodon/users/MyUser/updates/1234',
                'content': '<p><span class="h-card"><a '
                           'href="https://social.svallee.fr/@HAUM">@<span>HAUM</span></a></span> test</p>',
                'visibility': 'private'
            }
        }

        mention = Mention.from_notification(notification)

        self.assertEqual('test@instance.mastodon', mention.user)
        self.assertEqual('https://instance.mastodon/users/MyUser/updates/1234',
                         mention.url)
        self.assertEqual('@HAUM test', mention.content)
        self.assertEqual('private', mention.visibility)