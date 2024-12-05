# SlackBridge API

![made-with-python][made-with-python]
![Python Versions][pyversion-button]
![Hits][hits-button]

[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[made-with-python]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
[hits-button]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpassword123456%2Fslackbridge-api&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false

Slack Bridge API is a Flask-based REST API designed for user management, email-based user search, and Slack message integration.

Currently, this API only supports querying users and sending messages to users through a Slack bot. Features such as file attachments (e.g., images), sending messages to multiple users via the bot, sending messages to a specific channel (similar to a webhook), and responding to bot commands are not yet implemented. You can continue to modify and update the API as needed to include these features.

If you find this helpful, please the "star"🌟 to support further improvements.

## Features  

- **User Search:** Fetch user details by email or retrieve all users.  
- **Health Check:** Validate server status with a lightweight endpoint.  
- **Slack Message Integration:** Send Slack messages to `users/channels` via the Slack API.  

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

## Getting Started
To start using SlackBridge API:

Clone the repository:
```
git clone https://github.com/password123456/slackbridge-api.git
```
Install dependencies:
```
pip install -r requirements.txt
```

# API Endpoints
  * [1.Send Message - Users](#1send-messages-to-users)
    + [Request](#11request)
    + [Response](#12response)
  * [2.Send Message - Channels](#2send-messages-to-channels)
    + [Request](#21request)
    + [Response](#22response)
  * [3.Retrieve User Data](#3retrieve-user-data)
    + [Request](#31request)
    + [Response](#32response)
  * [4.List All Users](#4list-all-users)
    + [Request](#41request)
    + [Response](#42response)
  * [5.Error Handling](#5error-handling)
  * [6.Token Generator](#6token-generator)
  * [7.Slack Bot Scopes](#7slack-bot-scopes)

## 1.Send Messages To Users
**Endpoint:** `/api/v1/messages/users`

**Method**: `POST`

**Description**
- Sends a message to a specific Slack users.
- Sends the message via a `Slack Bot`.
- The size of a single message must not exceed the limit defined by the `verify_params_length` decorator.
- The request body format is `JSON`.

**Headers:**
- `Authorization: <API_TOKEN>`
- `Content-Type: application/json`

**Body Parameters:**

| **Name** | **Type**        | **Description**                                                                                              | **Required** |
|----------|-----------------|--------------------------------------------------------------------------------------------------------------|--------------|
| users    | `String`,`List` | Recipient's email address. The email format is validated by the `verify_params_suffix` decorator.            | Yes          |
| message  | `String`        | The text message to send. Message must not exceed the limit defined by the `verify_params_length` decorator. | Yes          |

### 1.1.Request:

```
POST /api/v1/messages/users HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
Content-Type: application/json
        
{
  "users": "john.doe@example.com",
  "message": "Hello John, Get Out!"
}
```

```
POST /api/v1/messages/users HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
Content-Type: application/json

{
  "users": ["jane.doe@example.com"],
  "message": "Hello, Jane"
}
```

```
POST /api/v1/messages/users HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
Content-Type: application/json

{
  "users": ["john.doe@example.com", "jane.doe@example.com", "baby.doe@example.com"],
  "message": "Hello, Guys"
}
```

### 1.2.Response:
- Success (200):
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": true,
  "result": {
    "users": "john.doe@example.com",
    "message": "Message sent successfully, 2024-08-27T12:00:00Z"
}
```

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": true,
  "result": {
    "users": [
      "john.doe@example.com",
      "jane.doe@example.com",
      "baby.doe@example.com"
    ],
    "message": "Message sent successfully! 2024-12-02T04:42:18+00:00"
  }
}
```


- Error (400):
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": false,
  "error": "Required fields are missing in the request body. Please check and try again."
}
```

## 2.Send Messages To Channels
**Endpoint:** `/api/v1/messages/channels`

**Method**: `POST`

**Description**
- Sends a message to a specific Slack Channels.
- Sends the message via a `Slack Bot`.
- `Slack Bot` must be joined the Channel
- The size of a single message must not exceed the limit defined by the `verify_params_length` decorator.
- The request body format is `JSON`.

**Headers:**
- `Authorization: <API_TOKEN>`
- `Content-Type: application/json`

**Body Parameters:**

| **Name** | **Type**        | **Description**                                                                                              | **Required** |
|----------|-----------------|--------------------------------------------------------------------------------------------------------------|--------------|
| channels | `String`,`List` | Channel ids to Sending Message.                                                                              | Yes          |
| message  | `String`        | The text message to send. Message must not exceed the limit defined by the `verify_params_length` decorator. | Yes          |

### 2.1.Request:

```
POST /api/v1/messages/channels HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
Content-Type: application/json
        
{
  "channels": "C0769GJ758U",
  "message": "<@U072E6GR1LM> Hello John, Get Out!"
}
```

```
POST /api/v1/messages/channels HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
Content-Type: application/json

{
  "channels": ["C0769GJ758U"],
  "message": "Hello, Guys BE happy"
}
```

```
POST /api/v1/messages/channels HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
Content-Type: application/json

{
  "channels": ["C0769GJ758U","C06U8V03R0T"],
  "message": "Hello, Guys BE happy"
}
```

### 2.2.Response:
- Success (200):
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": true,
  "result": [
    {
      "status": true,
      "channel": "C0769GJ758U",
      "message": "Message sent successfully! 2024-12-05T08:48:17+00:00"
    }
  ]
}
```

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": true,
  "result": [
    {
      "status": true,
      "channel": "C0769GJ758U",
      "message": "Message sent successfully! 2024-12-05T08:50:08+00:00"
    },
    {
      "status": true,
      "channel": "C06U8V03R0T",
      "message": "Message sent successfully! 2024-12-05T08:50:09+00:00"
    }
  ]
}
```

- Error (400):
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": false,
  "error": "Required fields are missing in the request body. Please check and try again."
}
```

## 3.Retrieve User Data
**Endpoint**: `/api/v1/users/search`

**Method:** `POST`

**Description**
- Retrieves information about a specific Slack user.
- Returns the user's `email`, `username`, `display name`, and `Slack member_id`.
- Time-related data in the response body follows the `ISO 8601` format (`YYYY-MM-DDTHH:MM:SSZ`).
- Both the request and response body formats are in `JSON`.

**Headers:**
- `Authorization: <API_TOKEN>`
- `Content-Type: application/json`

**Body Parameters:**

| **Name** | **Type** | **Description**                                                                                   | **Required** |
|----------|----------|---------------------------------------------------------------------------------------------------|--------------|
| user     | `String` | Recipient's email address. The email format is validated by the `verify_params_suffix` decorator. | Yes          |

### 3.1.Request

```
POST /api/v1/users/search HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
Content-Type: application/json

{
  "user": "john.doe@example.com",
}
```

### 3.2.Response
- Success (200):
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": true,
  "result": {
    "datetime": "2024-11-22T10:09:14+09:00",
    "real_name": "john.doe",
    "display_name": "john",
    "member_id": "U072E6GR1LM",
    "user_email": "john.doe@example.com"
  }
}
```

- Error (404):
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": false,
  "message": "The specified user could not be found. Please check the input and try again."
}
```

## 4.List All Users
**Endpoint:** `/api/v1/users/all`

**Method:** `GET`

**Description**
- Retrieves information about all Slack users.
- Returns the user's `email`, `username`, `display name`, and `Slack member_id`.
- Time-related data in the response body follows the `ISO 8601` format (`YYYY-MM-DDTHH:MM:SSZ`).
- Both the request and response body formats are in `JSON`.
  
**Headers:**
- `Authorization: <API_TOKEN>`

**Body Parameters:**
- `None`

### 4.1.Request
```
GET /api/v1/users/all HTTP/1.1
Host: slack-alim.example.com
Authorization: <api_token>
```

### 4.2.Response
- Success (200):
```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": true,
  "message": [
    {
      "datetime": "2024-11-22T10:09:14+09:00",
      "real_name": "john.doe",
      "display_name": "john",
      "member_id": "U072E6GR1LM",
      "user_email": "john.doe@example.com"
    },
    {
      "datetime": "2024-11-22T10:09:14+09:00",
      "real_name": "jane.doe",
      "display_name": "jane",
      "member_id": "U092P6GRALM",
      "user_email": "jane.doe@example.com"
    },
    {
      "datetime": "2024-11-22T10:09:14+09:00",
      "real_name": "baby.doe",
      "display_name": "babybaby",
      "member_id": "U132E6BR1LM",
      "user_email": "baby.doe@example.com"
    }
  ]
}
```

## 5.Error Handling
The SlackBridge API uses standard HTTP response codes to indicate success or failure. Additional details are provided in the response body.

| HTTP Code | Meaning               | Example                           |
|-----------|-----------------------|-----------------------------------|
| 200       | Success               | The request was successful.       |
| 400       | Bad Request           | Invalid parameters were provided. |
| 401       | Unauthorized          | Invalid or missing token.         |
| 404       | Not Found             | The resource could not be found.  |
| 500       | Internal Server Error | An error occurred on the server.  |

## 6.Token Generator
`token_generator.py` simplifies the creation, encryption, decryption, and validation of API tokens using `AES-GCM encryption`, ensuring high security and integrity. It is particularly useful for managing access keys with expiration and IP-based restrictions.

### Features:
- `Secure Token Management:` Generates encrypted tokens, stores them in a database, and retrieves them securely.
- `Expiration & IP Validation:` Tokens include metadata such as issuer, expiration time, and allowed IP addresses for access control.
- `AES-GCM Encryption:` Ensures confidentiality and integrity using a 32-byte passphrase key and a 12-byte nonce.

## 7.Slack Bot Scopes
- Below are the scopes required for creating a new Slack Bot.
- The list also includes optional scopes that are not necessary (e.g., files:read, files:write).
- Carefully review and grant scopes based on your specific use case and requirements.

Scopes does not allow Slackbots to send messages to arbitrary channels. To send messages to a channel, the Slackbot must be a member of the channel.

| **OAuth Scope**          | **Description**                                                                      |
|--------------------------|--------------------------------------------------------------------------------------|
| `channels:history`       | View messages and other content in public channels that wawa has been added to       |
| `channels:join`          | Join public channels in a workspace                                                  |
| `channels:manage`        | Manage public channels that wawa has been added to and create new ones               |
| `channels:read`          | View basic information about public channels in a workspace                          |
| `channels:write.invites` | Invite members to public channels                                                    |
| `chat:write`             | Send messages as @wa-bot                                                             |
| `chat:write.customize`   | Send messages as @wa-bot with a customized username and avatar                       |
| `chat:write.public`      | Send messages to channels @wa-bot isn't a member of                                  |
| `files:read`             | View files shared in channels and conversations that wawa has been added to          |
| `files:write`            | Upload, edit, and delete files as wawa                                               |
| `groups:history`         | View messages and other content in private channels that wawa has been added to      |
| `groups:read`            | View basic information about private channels that wawa has been added to            |
| `groups:write`           | Manage private channels that wawa has been added to and create new ones              |
| `groups:write.invites`   | Invite members to private channels                                                   |
| `im:history`             | View messages and other content in direct messages that wawa has been added to       |
| `im:read`                | View basic information about direct messages that wawa has been added to             |
| `im:write`               | Start direct messages with people                                                    |
| `incoming-webhook`       | Post messages to specific channels in Slack                                          |
| `mpim:history`           | View messages and other content in group direct messages that wawa has been added to |
| `mpim:read`              | View basic information about group direct messages that wawa has been added to       |
| `mpim:write`             | Start group direct messages with people                                              |
| `users.profile:read`     | View profile details about people in a workspace                                     |
| `users:read`             | View people in a workspace                                                           |
| `users:read.email`       | View email addresses of people in a workspace                                        |
