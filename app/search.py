__author__ = 'https://github.com/password123456/'
__date__ = '2024.11.19'
__version__ = '1.1'
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


def search_email(email):
    member_info = None
    member_id = None
    try:
        with open(current_app.config['USERS_DB'], 'r', encoding='utf-8') as database:
            for line in database:
                if line.startswith('#') or len(line.strip()) == 0:
                    continue

                split_line = line.split(',')
                user_email = split_line[5].strip()
                if str(email) == str(user_email):
                    member_info = {
                        'datetime': split_line[1].strip(),
                        'real_name': split_line[2].strip(),
                        'display_name': split_line[3].strip(),
                        'member_id': split_line[4].strip(),
                        'user_email': user_email
                    }
                    member_id = member_info['member_id']
                    break  # if found, stop search
        return member_id, member_info
    except FileNotFoundError:
        return None
