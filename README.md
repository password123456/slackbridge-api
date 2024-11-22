# SlackBridge API

![made-with-python][made-with-python]
![Python Versions][pyversion-button]
![Hits][hits-button]

[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[made-with-python]: https://img.shields.io/badge/Made%20with-Python-1f425f.svg
[hits-button]: https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fpassword123456%2Fslackbridge-api&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false

Slack Bridge API is a Flask-based REST API designed for user management, email-based user search, and Slack message integration.

Currently, this API supports querying users and sending messages to users through a Slack bot. Features such as file attachments (e.g., images), sending messages to multiple users via the bot, sending messages to a specific channel (similar to a webhook), and responding to bot commands are not yet implemented. You can continue to modify and update the API as needed to include these features.

If you find this helpful, please the "star"🌟 to support further improvements.

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
  * [1.Send Message](#1send-message)
    + [Request](#11request)
    + [Response](#12response)
  * [2.Retrieve User Data](#2retrieve-user-data)
    + [Request](#21request)
    + [Response](#22response)
  * [3.List All Users](#3list-all-users)
    + [Request](#31request)
    + [Response](#32response)

***

## 1.Send Message
**Endpoint:** `/api/v1/message/send`

**Method**: `POST`

**Description**
- Sends a message to a specific Slack user.
- Sends the message via a `Slack Bot`.
- The name of the sending `Bot` is the one configured in Slack.
- The size of a single message must not exceed the limit defined by the `verify_params_length` decorator.
- The request body format is `JSON`.

**Headers:**
- `Authorization: <API_TOKEN>`
- `Content-Type: application/json`

**Body Parameters:**

| **Name** | **Type** | **Description**                                                                                        | **Required** |
|----------|----------|--------------------------------------------------------------------------------------------------------|--------------|
| email    | `String` | Recipient's email address. The email format is validated by the `verify_email_param_suffix` decorator. | Yes          |
| message  | `String` | The text message to send. Must not exceed `4000 bytes`.                                                | Yes          |

### 1.1.Request:

```json
{
  "email": "stark@example.com",
  "message": "Hello Tony, Get Out!"
}
```

### 1.2.Response:
- Success (200):
```json
{
  "status": true,
  "result": {
    "email": "stark@example.com",
    "message": "Message sent successfully, 2024-08-27T12:00:00Z"
}
```

- Error (400):
```json
{
  "status": false,
  "error": "Required fields are missing in the request body. Please check and try again."
}
```

## 2.Retrieve User Data
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

| **Name** | **Type** | **Description**                                                                                        | **Required** |
|----------|----------|--------------------------------------------------------------------------------------------------------|--------------|
| email    | `String` | Recipient's email address. The email format is validated by the `verify_email_param_suffix` decorator. | Yes          |

### 2.1.Request

```json
{
  "email": "stark@example.com",
}
```

### 2.2.Response
- Success (200):
```json
{
  "status": true,
  "result": {
    "datetime": "2024-11-22T10:09:14+09:00",
    "real_name": "tony.stark",
    "display_name": "stark",
    "member_id": "U072E6GR1LM",
    "user_email": "tony.stark@example.com"
  }
}
```

- Error (404):
```json
{
  "status": false,
  "message": "The specified user could not be found. Please check the input and try again."
}
```

## 3.List All Users
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

### 3.1.Request
```
GET /api/v1/users/all
```

### 3.2.Response
- Success (200):
```json
{
  "status": true,
  "message": [
    {
      "datetime": "2024-11-22T10:09:14+09:00",
      "real_name": "tony.stark",
      "display_name": "stark",
      "member_id": "U072E6GR1LM",
      "user_email": "tony.stark@example.com"
    },
    {
      "datetime": "2024-11-22T10:09:14+09:00",
      "real_name": "Happy.Hogan",
      "display_name": "happy",
      "member_id": "U092P6GRALM",
      "user_email": "happy.hogan@example.com"
    },
    {
      "datetime": "2024-11-22T10:09:14+09:00",
      "real_name": "Steve.Rogers",
      "display_name": "steve",
      "member_id": "U132E6BR1LM",
      "user_email": "steve.rogers@example.com"
    }
  ]
}
```

## Error Handling
The SlackBridge API uses standard HTTP response codes to indicate success or failure. Additional details are provided in the response body.

| HTTP Code | Meaning               | Example                           |
|-----------|-----------------------|-----------------------------------|
| 200       | Success               | The request was successful.       |
| 400       | Bad Request           | Invalid parameters were provided. |
| 401       | Unauthorized          | Invalid or missing token.         |
| 404       | Not Found             | The resource could not be found.  |
| 500       | Internal Server Error | An error occurred on the server.  |



