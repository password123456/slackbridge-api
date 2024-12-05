__author__ = 'https://github.com/password123456/'
__date__ = '2024.11.18'
__version__ = '1.5'
__status__ = 'Production'

import json
from flask import make_response


ERROR_MESSAGES = {
    'MISSING_REQUIRED_PARAMS': {
        'http_status': 400,
        'message': {
            'status': False,
            'message': 'Required fields are missing in the request body. Please check and try again.'
        }
    },
    'IS_NOT_JSON_FORMAT': {
        'http_status': 400,
        'message': {
            'status': False,
            'message': 'The request body contains invalid JSON. Please fix the format and resubmit.'
        }
    },
    'INVALID_DATA_TYPE': {
        'http_status': 400,
        'message': {
            'status': False,
            'message': 'Some fields in the request contain incorrect data types. Verify and update the input.'
        }
    },
    'EXCEEDED_MAX_LENGTH': {
        'http_status': 400,
        'message': {
            'status': False,
            'message': 'Input exceeds the allowed length or is empty. Please adjust and try again.'
        }
    },
    'INVALID_PARAMS_SUFFIX': {
        'http_status': 400,
        'message': {
            'status': False,
            'message': 'The param provided does not match the required format or suffix. Check and try again.'
        }
    },
    'INVALID_EMAIL_SUFFIX': {
        'http_status': 400,
        'message': {
            'status': False,
            'message': 'The email provided does not match the required format or domain. Check and try again.'
        }
    },
    'AUTHENTICATION_FAILED': {
        'http_status': 401,
        'message': {
            'status': False,
            'message': 'Authentication failed. The credentials provided are incorrect.'
        }
    },
    'NOT_AUTHENTICATED': {
        'http_status': 401,
        'message': {
            'status': False,
            'message': 'No authentication credentials were provided. Please include valid credentials.'
        }
    },
    'UNAUTHORIZED_API_TOKEN': {
        'http_status': 401,
        'message': {
            'status': False,
            'message': 'The provided API TOKEN is unauthorized. Please verify your key and try again.'
        }
    },
    'INVALID_API_TOKEN': {
        'http_status': 401,
        'message': {
            'status': False,
            'message': 'The API TOKEN is invalid. Ensure the key is correct and has not expired.'
        }
    },
    'EXPIRED_API_TOKEN': {
        'http_status': 401,
        'message': {
            'status': False,
            'message': 'The API TOKEN has expired. Please renew your key and try again.'
        }
    },
    'PERMISSION_DENIED': {
        'http_status': 403,
        'message': {
            'status': False,
            'message': 'You lack the necessary permissions to perform this action.'
        }
    },
    'USER_NOT_FOUND': {
        'http_status': 404,
        'message': {
            'status': False,
            'message': 'The specified user could not be found. Please check the input and try again.'
        }
    },
    'RESOURCE_NOT_FOUND': {
        'http_status': 404,
        'message': {
            'status': False,
            'message': 'The requested resource is unavailable or does not exist.'
        }
    },
    'NOT_ALLOWED_METHOD': {
        'http_status': 405,
        'message': {
            'status': False,
            'message': 'The HTTP method used is not allowed for this endpoint. Please check the API documentation.'
        }
    },
    'SERVER_ERROR': {
        'http_status': 500,
        'message': {
            'status': False,
            'message': 'An unexpected server error occurred. We are working to resolve the issue.'
        }
    },
}


def http_response_server_error(error_key):
    default_error = {
        'http_status': 500,
        'message': {
            'status': False,
            'message': 'An internal server error occurred. Please try again later.'
        }
    }

    error = ERROR_MESSAGES.get(error_key, default_error)

    # Create pretty-printed JSON response with newline at the end
    response_json = json.dumps(
        error['message'],
        indent=2
    ) + '\n'

    # Return response with JSON, status code, and content-type
    return make_response(
        response_json,
        error['http_status'],
        {'Content-Type': 'application/json'}
    )
