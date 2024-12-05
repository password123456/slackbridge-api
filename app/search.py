__author__ = 'https://github.com/password123456/'
__date__ = '2024.12.04'
__version__ = '1.3'
__status__ = 'Production'

from flask import current_app


def export_all_users():
    result = []
    try:
        with open(current_app.config['USERS_DB'], 'r', encoding='utf-8') as database:
            for line in database:
                if line.startswith('#') or len(line.strip()) == 0:
                    continue

                split_line = line.split(',')
                result.append({
                    'datetime': split_line[1].strip(),
                    'real_name':  split_line[2].strip(),
                    'display_name': split_line[3].strip(),
                    'member_id': split_line[4].strip(),
                    'user_email': split_line[5].strip()
                })
        return result
    except FileNotFoundError:
        return None


def search_email(user):
    member_info = None
    member_id = None

    if not isinstance(user, str):
        user = ','.join(user)

    try:
        with open(current_app.config['USERS_DB'], 'r', encoding='utf-8') as database:
            for line in database:
                if line.startswith('#') or len(line.strip()) == 0:
                    continue

                split_line = line.split(',')
                user_email = split_line[5].strip()
                if str(user) == str(user_email):
                    member_info = {
                        'datetime': split_line[1].strip(),
                        'real_name': split_line[2].strip(),
                        'display_name': split_line[3].strip(),
                        'member_id': split_line[4].strip(),
                        'user_email': user_email
                    }
                    member_id = member_info['member_id']
                    break  # if found, stop searching
        return member_id, member_info
    except FileNotFoundError:
        return None


def search_member_ids(email_list):
    member_ids = []

    if isinstance(email_list, str):
        email_list = [email_list]

    try:
        with open(current_app.config['USERS_DB'], 'r', encoding='utf-8') as database:
            for line in database:
                if line.startswith('#') or len(line.strip()) == 0:
                    continue
                split_line = line.split(',')
                user_email = split_line[5].strip()
                for email in email_list:
                    if email.strip() == user_email:
                        member_id = split_line[4].strip()
                        member_ids.append(member_id)
    except FileNotFoundError:
        return None

    if member_ids:
        if len(member_ids) == 1:
            return member_ids[0]
        elif member_ids:
            return ','.join(member_ids)
    else:
        return None
