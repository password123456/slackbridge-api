# SlackBridge API

![made-with-python][made-with-python]
![Python Versions][pyversion-button]
![Hits][hits-button]

[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[made-with-python]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
[hits-button]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpassword123456%2Fslackbridge-api&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false

Slack Bridge API is a Flask-based REST API designed for user management, email-based user search, and Slack message integration.

## Features  

- **User Search:** Fetch user details by email or retrieve all users.  
- **Health Check:** Validate server status with a lightweight endpoint.  
- **Slack Message Integration:** Send Slack messages to users via the Slack API.  

## Project Structure  

```plaintext
slack_bridge
├── settings.py
├── wsgi.py
├── token_generator.py
├── service_config.py
├── service_control.sh
├── collect_slackusers.py
├── collect_slackusers.sh
├── requirements.txt
└── app
    ├── authentication.py
    ├── exceptions.py
    ├── generics.py
    ├── logger.py
    ├── route.py
    ├── search.py
    ├── sendmessage.py
    ├── validators.py
    └── db
        ├── keys.db
        └── users.db
    └── logs
        └── slack_bridge.app.validators.exceptions.log
```
