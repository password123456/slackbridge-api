__author__ = 'https://github.com/password123456/'
__date__ = '2024.11.20'
__version__ = '1.2'
__status__ = 'Production'

import sys
import requests
import json
from flask import current_app
from datetime import datetime, timezone


def slack_conversations_open(headers, set_proxy, user_id):
    api_method = 'conversations.open'
    result = ''
    try:
        response = requests.post(
            f'https://slack.com/api/{api_method}',
            headers=headers,
            proxies=set_proxy,
            json={'users': user_id}
        )
        result = response.json()
        if result['ok']:
            return result['channel']['id']

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'- Exception::{e}')
    return result


def slack_chat_post_message(headers, set_proxy, user_chat_id, message):
    api_method = 'chat.postMessage'
    result = ''
    try:
        response = requests.post(
            f'https://slack.com/api/{api_method}',
            headers=headers,
            proxies=set_proxy,
            json={'channel': user_chat_id, 'text': message, 'as_user': True}
        )
        # result = response.json()
        result = response.text

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'- Exception::{e}')
    return result


def send_message(user_id, message):
    token = current_app.config['SLACK_BOT']
    # set_proxy = current_app.config['PROXY']
    set_proxy = None

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    dm_chat_id = slack_conversations_open(headers, set_proxy, user_id)
    if dm_chat_id:
        message = f'<@{user_id}>\n{message}'
        result = slack_chat_post_message(headers, set_proxy, dm_chat_id, message)
        data = json.loads(result)
        if data['ok']:
            ret_result = True
            ret_data = (f'Message sent successfully! '
                        f'{datetime.utcfromtimestamp(float(data["ts"])).replace(tzinfo=timezone.utc, microsecond=0).isoformat()}')
        else:
            ret_result = False
            ret_data = f'Message sent failed! {data["error"]}'
        return ret_result, ret_data
