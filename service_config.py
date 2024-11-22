import gunicorn
import os

# Define Server
bind = '127.0.0.1:8888'
workers = 5
name = 'jf'
timeout = 30
keepalive = 2
daemon = True

# Define Gunicorn Process User, Group
user='www-data'
group='www-data'

# Define Log
loglevel = 'info'
errorlog = f'{os.path.dirname(os.path.abspath(__file__))}/logs/slack_bridge.http_error.log'
accesslog = f'{os.path.dirname(os.path.abspath(__file__))}/logs/slack_bridge.http_access.log'
access_log_format = '%({X-Forwarded-For}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
