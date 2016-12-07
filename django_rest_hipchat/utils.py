import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

try:
    # Allow URL override via settings.
    HIPCHAT_API_URL = settings.HIPCHAT_API_URL
except AttributeError:
    HIPCHAT_API_URL = 'https://api.hipchat.com/v2'


def get_access_token(installation):
    payload = {
        'grant_type': 'client_credentials',
        'scope': 'send_notification',
    }

    res = requests.post(
        '{}/oauth/token'.format(HIPCHAT_API_URL),
        data=payload,
        auth=(str(installation.oauth_id), installation.oauth_secret)
    )

    if res.status_code == 200:
        token_info = res.json()
        return token_info.get('access_token', None)

    return None


def update_glance(installation, glance, new_label):
    """
    Updates glance label.
    """
    access_token = get_access_token(installation)
    if access_token is None:
        logger.error("Unable to fetch hipchat access_token.")
        return None

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }

    res = requests.post(
        '{}/addon/ui/room/{}'.format(HIPCHAT_API_URL, installation.room_id),
        headers=headers,
        json={
            'glance': [
                {
                    'content': {
                        'label': new_label,
                    },
                    'key': glance.get_key()
                }
            ]
        }
    )

    logger.warn(repr(res))
    return res
