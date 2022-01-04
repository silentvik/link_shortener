import string
from random import choice

from shortener_app.models import Urls

CHAR_LIST = string.ascii_uppercase + string.digits + string.ascii_lowercase


def create_short_url(real_url, current_user):
    """
        Creates an Urls object and returns it.
    """

    current_user_id = 0
    if current_user.is_authenticated:
        current_user_id = current_user.id

    new_url_inst = Urls.objects.create(
        real_url=real_url,
        created_by_id=current_user_id,
        short_url=make_new_short_url(),
    )
    return new_url_inst


def generate_short_url(max_length):
    """
        Returns a random string of the specified length.
    """

    return ''.join(choice(CHAR_LIST) for _ in range(max_length))


def make_new_short_url():
    """
        Creates and returns a short version of the link
        without a prefix in the form of a domain.
        Makes a request to the database to verify uniqueness.
    """

    max_length = 6
    urls = list(Urls.objects.all())

    print(f'urls = {urls}')
    while True:
        short_url = generate_short_url(max_length)
        if short_url not in urls:
            break
    return f"{short_url}"
