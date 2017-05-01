# Configuration file for hms_mastodon

# RabbitMQ

RABBIT_HOST = 'localhost'                   # Address of the server
RABBIT_EXCHANGE = 'haum'                    # Name of the direct exchanger

RABBIT_ROUTING_KEYS = ['spacestatus.broadcast', 'mastodon.*']       # List of routing keys to listen to

# Mastodon

EMAIL = "mastodon-haum@microjoe.org"
API_BASE_URL = "https://social.svallee.fr"
ACCOUNT_URL = "https://social.svallee.fr/@HAUM"

APP_NAME = "hms_mastodon"

CLIENT_CREDS_FILE = "pytooter_clientcred.txt"
USER_CREDS_FILE = "pytooter_usercred.txt"