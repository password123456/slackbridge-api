import os


class Config:
    DEBUG = False

    PROXY = {
        'http': 'your-proxy-server',
        'https': 'your-proxy-server'
    }

    SLACK_BOT = 'your-slack-bot-token'

    APP_PATH = os.path.dirname(os.path.abspath(__file__))
    KEY_DB = os.path.join(APP_PATH, 'app/db/keys.db')
    USERS_DB = os.path.join(APP_PATH, 'app/db/users.db')
