import os


class Config:
    DEBUG = False

    PROXY = {
        'http': 'your-proxy-server',
        'https': 'your-proxy-server'
    }

    SLACK_BOT = 'your-slack-bot-token'
    CHANNEL_ALL_USERS_IN = 'The channel ID that all users are joined to in order to collect information about Slack users.'
    
    SLACK_REQ_HEADERS = {
        'Authorization': f'Bearer {SLACK_BOT}',
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }
    
    APP_PATH = os.path.dirname(os.path.abspath(__file__))
    KEY_DB = os.path.join(APP_PATH, 'app/db/keys.db')
    USERS_DB = os.path.join(APP_PATH, 'app/db/users.db')
