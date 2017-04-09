from mastodon import Mastodon

from hms_mastodon import settings


def login():
    """Log in to the Mastodon instance and store creds into a file.
    
    Once the credentials are stored in a file you do not need to
    connect again, the file will be used.
    
    """

    print("Creating Mastodon connection…")
    mastodon = Mastodon(client_id = settings.CLIENT_CREDS_FILE,
                        api_base_url = settings.API_BASE_URL)

    password = input("Enter password for {} Mastodon account: ".format(settings.EMAIL))

    print("Logging in to Mastodon instance with account {} and password {}…".format(settings.EMAIL, password))
    print(mastodon.log_in(
        settings.EMAIL, password,
        to_file = settings.USER_CREDS_FILE,
    ))


if __name__ == '__main__':
    login()