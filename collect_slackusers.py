__author__ = 'https://github.com/password123456/'
__date__ = '2021.01.11'
__version__ = '1.2'
__status__ = 'Production'

import os
import sys
import requests
import json
from datetime import datetime, timezone


def lookup_conversations_members(headers, channel_id, set_proxy):
    api_method = 'conversations.members'
    limit = 1000
    result = ''
    try:
        # https://api.slack.com/methods/conversations.members
        response = requests.get(
            f'https://slack.com/api/{api_method}?channel={channel_id}&limit={limit}&pretty=1',
            headers=headers,
            proxies=set_proxy
        )
        result = response.text
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print(f'- Exception::{error}')
    return result


def lookup_users_info(headers, user_id, set_proxy):
    api_method = 'users.info'
    result = ''
    try:
        # https://api.slack.com/methods/users.info
        response = requests.get(
            f'https://slack.com/api/{api_method}?user={user_id}',
            headers=headers,
            proxies=set_proxy
        )
        result = response.text
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print(f'- Exception::{error}')
    return result


def get_value_or_null(value):
    return 'null' if not value else value


def export_data(filename, data, mode):
    with open(filename, mode, encoding='utf-8', newline='') as file:
        for line in data:
            file.write(f'{line}\n')


def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        return 0
    except Exception as error:
        print(f'- Exception::{error}')
        return -1


def main():
    slack_bot_token = 'your-slack-bot-token'
    channel_id = 'slack-channel-id-where-all-users-are-joined-to-collect-user-info'

    # set_proxy = {
    #    'http': 'your-proxy-server',
    #    'https': 'your-proxy-server'
    # }
    set_proxy = None  # if you don't want to use proxy server

    headers = {
        'Authorization': f'Bearer {slack_bot_token}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }

    result = lookup_conversations_members(headers, channel_id, set_proxy)
    member_data = json.loads(result)

    i = 0
    content_result = []
    export_path = os.path.dirname(os.path.abspath(__file__))
    users_db = os.path.join(export_path, 'app/db/users.db') 
    mode = 'w'

    if member_data['ok']:
        members = member_data['members']
        for user_id in members:
            user_data = lookup_users_info(headers, user_id, set_proxy)
            user_data = json.loads(user_data)
            user_info = user_data['user']
            # Extract user excluding bots account
            if not user_info['is_bot']:
                i = i + 1
                member_id = get_value_or_null(user_info.get('id'))
                display_name = get_value_or_null(user_info.get('name'))
                real_name = get_value_or_null(user_info.get('real_name'))
                mobile = get_value_or_null(user_info['profile'].get('phone'))
                email = get_value_or_null(user_info['profile'].get('email'))
                title = get_value_or_null(user_info['profile'].get('title').replace(' ', '').replace(',', '/'))

                content_result.append(f'{i},{datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()},'
                                      f'{real_name},{display_name},{member_id},{email},{title},{mobile}')

                # save users by 10 count information stored in content_result when it reaches 10
                # i.e. when it reaches 10, break into 10 units and save to users_db
                # after saving, content_result is initialised to an empty list (to avoid duplicate storage)
                if len(content_result) >= 10:
                    export_data(users_db, content_result, mode)
                    content_result = []
                    mode = 'a'

    # If there is data that is less than 10 and could not be saved to users_db, save to file
    # i.e. save the last remaining user information
    mode = 'a'
    if content_result:
        export_data(users_db, content_result, mode)

    message = (f'>> collect slack_users <<\n\n'
               f'- {os.uname()[1]}\n'
               f'- *{datetime.now(timezone.utc).replace(microsecond=0).isoformat()}*')
    if os.path.exists(users_db):
        line_count = count_lines_in_file(users_db)
        if line_count >= 0:
            message = f'*{message}\n\n`{line_count} user record created.`'
        else:
            message = f'*{message}\n\n`{users_db} not found. something wrong?`'
    else:
        message = f'*{message}\n\n`{users_db} not found. something wrong?`'
    print(message)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'- ::Exception:: Func:[{__name__.__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}')

"""
*>> collect slack_users <<

- mymacmacmac.local
- *2024-11-22T01:10:51+00:00*

`257 user record created.`
"""
