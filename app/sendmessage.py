__author__ = 'https://github.com/password123456/'
__date__ = '2024.12.03'
__version__ = '1.5'
__status__ = 'Production'

import sys
import requests
import json
from flask import current_app
from datetime import datetime, timezone


def slack_conversations_open(headers, set_proxy, member_ids):
    api_method = 'conversations.open'
    result = ''
    try:
        response = requests.post(
            f'https://slack.com/api/{api_method}',
            headers=headers,
            proxies=set_proxy,
            json={'users': member_ids}
        )
        result = response.json()
        if result['ok']:
            return result['channel']['id']

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'- Exception::{e}')
    return result


def slack_chat_post_message(headers, set_proxy, channel_id, message):
    api_method = 'chat.postMessage'
    result = ''
    try:
        response = requests.post(
            f'https://slack.com/api/{api_method}',
            headers=headers,
            proxies=set_proxy,
            json={'channel': channel_id, 'text': message, 'as_user': True}
        )
        # result = response.json()
        result = response.text

    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'- Exception::{e}')
    return result


def send_to_users(member_ids, message):
    # set_proxy = current_app.config['PROXY']
    set_proxy = None
    headers = current_app.config['SLACK_REQ_HEADERS']

    channel_ids = slack_conversations_open(headers, set_proxy, member_ids)
    if channel_ids:
        # message = f'<@{user_id}>\n{message}'
        result = slack_chat_post_message(headers, set_proxy, channel_ids, message)
        data = json.loads(result)
        if data['ok']:
            ret_result = True
            ret_data = (f'Message sent successfully! '
                        f'{datetime.utcfromtimestamp(float(data["ts"])).replace(tzinfo=timezone.utc, microsecond=0).isoformat()}')
        else:
            ret_result = False
            ret_data = f'Message sent failed! {data["error"]}'
        return ret_result, ret_data


def send_to_channels(channel_ids, message):
    # set_proxy = current_app.config['PROXY']
    set_proxy = None
    headers = current_app.config['SLACK_REQ_HEADERS']

    if isinstance(channel_ids, str):
        channel_ids = [channel_ids]

    response_results = []
    success_count = 0

    if channel_ids:
        for channel_id in channel_ids:
            result = slack_chat_post_message(headers, set_proxy, channel_id, message)
            data = json.loads(result)

            if data['ok']:
                success_count += 1
                response_results.append({
                    'status': True,
                    'channel': channel_id,
                    'message': f'Message sent successfully! '
                               f'{datetime.utcfromtimestamp(float(data["ts"])).replace(tzinfo=timezone.utc, microsecond=0).isoformat()}'
                })
            else:
                response_results.append({
                    'status': True,
                    'channel': channel_id,
                    'message': f'Message sent failed! {data["error"]}'
                })

    # Aggregate final response status
    # is True or False
    overall_status = success_count == len(channel_ids)

    response_data = {
        "status": overall_status,
        "result": response_results
    }
    return response_data
