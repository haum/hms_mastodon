from mastodon import Mastodon

from hms_mastodon import settings


def create_app():
    """Registers an app on the Mastodon instance.
    
    Be sure to call this fonction only once, you do not
    want to register the application multiple times on the
    instance!
    
    """
    print(Mastodon.create_app(
        settings.APP_NAME,
        api_base_url=settings.API_BASE_URL,
        to_file = settings.CLIENT_CREDS_FILE
    ))


if __name__ == '__main__':
    create_app()