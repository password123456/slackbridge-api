__author__ = 'https://github.com/password123456/'
__date__ = '2024.12.02'
__version__ = '1.7'
__status__ = 'Production'

import json
from datetime import datetime, timezone
from flask import Blueprint, make_response
from app.exceptions import http_response_server_error
from app.validators import (verify_request_data_format, verify_required_params,
                            verify_params_length, verify_email_param_suffix, authentication_required)
from app.search import search_email, search_member_ids, export_all_users
from app.sendmessage import send_message

default = Blueprint('default', __name__)


@default.route('/')
def hello_world():
    response_data = {
        'status': True,
        'message': 'Hello, JF'
    }

    return make_response(
        json.dumps(response_data, indent=2) + '\n',
        200, {'Content-Type': 'application/json'})


@default.route('/health')
def health_check():
    response_data = {
        'status': True,
        'message': f'Yes, I\'m Alive. '
                   f'{datetime.now(timezone.utc).replace(tzinfo=timezone.utc, microsecond=0).isoformat()}'
    }
    return make_response(
        json.dumps(response_data, indent=2) + '\n',
        200, {'Content-Type': 'application/json'})


api_v1 = Blueprint('api', __name__, url_prefix='/api/v1')


@api_v1.route('/users/all', methods=['GET'])
@authentication_required
def export_all():
    try:
        ret_result = export_all_users()
        if ret_result:
            response_data = {
                'status': True,
                'message': ret_result
            }
            return make_response(
                json.dumps(response_data, indent=2) + '\n',
                200, {'Content-Type': 'application/json'})
    except Exception:
        return http_response_server_error('SERVER_ERROR')


@api_v1.route('/users/search', methods=['POST'])
@authentication_required
@verify_request_data_format
@verify_required_params({'email': str})
@verify_params_length({'email': 30})
@verify_email_param_suffix({'email': '@example.com'})
def users_search_by_email(data):
    if data is not None:
        ret_member_id, ret_member_info = search_email(data['email'])
        if ret_member_id and ret_member_info:
            response_data = {
                'status': True,
                'result': ret_member_info
            }
            return make_response(
                json.dumps(response_data, indent=2) + '\n',
                200, {'Content-Type': 'application/json'})
        else:
            return http_response_server_error('USER_NOT_FOUND')
    else:
        return http_response_server_error('SERVER_ERROR')


@api_v1.route('/messages/send', methods=['POST'])
@verify_request_data_format
@verify_required_params({'email': (str, list), 'message': str})
@verify_params_length({'email': 30, 'message': 4000})
@verify_email_param_suffix({'email': '@example.com'})
def messages_send(data):
    if data is not None:
        ret_member_ids = search_member_ids(data['email'])
        if ret_member_ids:
            ret_send_status, ret_send_result = send_message(ret_member_ids, data['message'])

            response_data = {
                'status': True,
                'result': {'email': data['email'], 'message': ret_send_result}
            }
            # Update status based on the result of send_message
            if ret_send_status:
                response_data['status'] = True
            else:
                response_data['status'] = False

            return make_response(
                json.dumps(response_data, indent=2) + '\n',
                200, {'Content-Type': 'application/json'})
        else:
            return http_response_server_error('USER_NOT_FOUND')
    else:
        return http_response_server_error('SERVER_ERROR')
