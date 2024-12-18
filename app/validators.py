__author__ = 'https://github.com/password123456/'
__date__ = '2024.12.05'
__version__ = '1.7'
__status__ = 'Production'

import json
from datetime import datetime
from functools import wraps
from flask import request
from app.exceptions import http_response_server_error
from app.logger import setup_logger
from app.authentication import decrypt_api_token
from app.generics import get_client_ip


app_name = 'slack_bridge'
logger = setup_logger(app_name, f'{app_name}.app.validators.exceptions.log')


def verify_request_data_format(func):
    @wraps(func)
    def request_format_verification(*args, **kwargs):
        data = request.get_json(silent=True)
        if data is None:
            logger.error(
                f'IS_NOT_JSON_FORMAT -> '
                f'(request_data) {request.data} | '
                f'{request.remote_addr} {request.method} {request.path}'
            )
            return http_response_server_error('IS_NOT_JSON_FORMAT')
        return func(data, *args, **kwargs)
    return request_format_verification


def verify_required_params(required_types):
    def decorator(func):
        @wraps(func)
        def required_params_data_type_verification(data, *args, **kwargs):
            invalid_data_type_params = []

            # Check for missing or wrong-type parameters
            for param, expected_type in required_types.items():
                if param not in data:
                    logger.error(
                        f'MISSING_REQUIRED_PARAMS | {request.remote_addr} {request.method} {request.path}'
                    )
                    return http_response_server_error('MISSING_REQUIRED_PARAMS')

                value = data[param]

                # Allow expected_type to be a single type or a tuple of types
                if not isinstance(expected_type, tuple):
                    expected_type = (expected_type,)

                if isinstance(value, list):
                    # If `list` is one of the expected types, validate list items
                    if list in expected_type:
                        # Verify each item in the list
                        for item in value:
                            if not isinstance(item, tuple(t for t in expected_type if t is not list)):
                                invalid_data_type_params.append({
                                    "param": param,
                                    "expected": ", ".join(
                                        t.__name__ for t in expected_type
                                    ),
                                    "got": f"list of {type(item).__name__}",
                                })
                                break
                    else:
                        # If `list` is not allowed, this is an invalid type
                        invalid_data_type_params.append({
                            "param": param,
                            "expected": ", ".join(
                                t.__name__ for t in expected_type
                            ),
                            "got": type(value).__name__,
                        })
                elif not isinstance(value, expected_type):
                    # Value is not a list, check against expected types directly
                    invalid_data_type_params.append({
                        "param": param,
                        "expected": ", ".join(
                            t.__name__ for t in expected_type
                        ),
                        "got": type(value).__name__,
                    })

            if invalid_data_type_params:
                for error in invalid_data_type_params:
                    logger.error(
                        f'INVALID_DATA_TYPE -> (param) {error["param"]} -> '
                        f'expected: {error["expected"]}, got: {error["got"]} | '
                        f'{request.remote_addr} {request.method} {request.path}'
                    )
                return http_response_server_error('INVALID_DATA_TYPE')

            # All validations passed
            return func(data, *args, **kwargs)
        return required_params_data_type_verification
    return decorator


def verify_params_length(max_lengths):
    def decorator(func):
        @wraps(func)
        def required_params_length_verification(data, *args, **kwargs):
            invalid_length_params = []

            for param, max_length in max_lengths.items():
                if param in data:
                    value = data[param]

                    if isinstance(value, str):
                        value = [value]
                    elif not isinstance(value, list):
                        logger.error(
                            f'INVALID_DATA_TYPE -> (param) {param} -> '
                            f'expected_type: string or list, got: {type(value).__name__} | '
                            f'{request.remote_addr} {request.method} {request.path}'
                        )
                        return http_response_server_error('INVALID_DATA_TYPE')

                    for item in value:
                        if not isinstance(item, str) or len(item) == 0 or len(item) > max_length:
                            invalid_length_params.append({
                                'param': param,
                                'value': item,
                                'max_length': max_length,
                                'got': len(item) if isinstance(item, str) else 'invalid'
                            })

            if invalid_length_params:
                for error in invalid_length_params:
                    logger.error(
                        f'EXCEEDED_MAX_LENGTH -> (param) {error["param"]}, value: {error["value"]} -> '
                        f'max_length: {error["max_length"]}, got_length: {error["got"]} | '
                        f'{request.remote_addr} {request.method} {request.path}'
                    )
                return http_response_server_error('EXCEEDED_MAX_LENGTH')
            return func(data, *args, **kwargs)
        return required_params_length_verification
    return decorator


def verify_params_suffix(email_suffix):
    def decorator(func):
        @wraps(func)
        def email_param_suffix_verification(data, *args, **kwargs):
            for param, suffix in email_suffix.items():
                if param in data:
                    value = data[param]
                    
                    if isinstance(value, (str, list)):
                        if isinstance(value, str):
                            value = [value]

                        for item in value:
                            if not isinstance(item, str) or not item.endswith(suffix):
                                logger.error(
                                    f'INVALID_PARAMS_SUFFIX -> (param) {param}, item: {item} -> '
                                    f'required_suffix: {suffix} | '
                                    f'{request.remote_addr} {request.method} {request.path}'
                                )
                                return http_response_server_error('INVALID_PARAMS_SUFFIX')
                    else:
                        logger.error(
                            f'INVALID_DATA_TYPE -> (param) {param} -> '
                            f'expected_type: string or list, got: {type(value).__name__} | '
                            f'{request.remote_addr} {request.method} {request.path}'
                        )
                        return http_response_server_error('INVALID_DATA_TYPE')
            return func(data, *args, **kwargs)
        return email_param_suffix_verification
    return decorator


def authentication_required(func):
    @wraps(func)
    def token_authentication(*args, **kwargs):
        # 1. get Authorization Header
        api_token = request.headers.get('Authorization')
        if not api_token:
            logger.error(
                f'UNAUTHORIZED_API_TOKEN -> Missing "Authorization" Header |'
                f'(request_data) {request.data} | '
                f'{request.remote_addr} {request.method} {request.path}'
            )
            return http_response_server_error('UNAUTHORIZED_API_TOKEN')

        # 2. decrypt API Token
        decrypted_token_data = decrypt_api_token(api_token)
        if not decrypted_token_data:
            logger.error(
                f'INVALID_API_TOKEN -> Decryption failed for API TOKEN: {api_token[:50]}... | '
                f'(request_data) {request.data} | '
                f'{request.remote_addr} {request.method} {request.path}'
            )
            return http_response_server_error('INVALID_API_TOKEN')

        # 3. load decrypted_token_data to JSON
        try:
            dicts_raw_token = json.loads(decrypted_token_data)
        except ValueError as e:
            logger.error(
                f'INVALID_API_TOKEN -> Failed to parse decrypted_token_data to JSON: {decrypted_token_data} | '
                f'Error: {str(e)}'
            )
            return http_response_server_error('INVALID_API_TOKEN')

        # 4. verify token is not expired
        current_time = int(datetime.now().timestamp())
        if 'exp' not in dicts_raw_token or current_time > int(dicts_raw_token['exp']):
            logger.error(
                f'EXPIRED_API_TOKEN -> API TOKEN expired. (exp: {dicts_raw_token.get("exp")}) | '
                f'(request_data) {request.data} | '
                f'{request.remote_addr} {request.method} {request.path}'
            )
            return http_response_server_error('EXPIRED_API_TOKEN')

        # 5. verify a remote IP authorized token
        remote_addr = get_client_ip()
        if 'allow_ips' not in dicts_raw_token or remote_addr not in dicts_raw_token['allow_ips']:
            logger.error(
                f'UNAUTHORIZED_API_TOKEN -> IP {remote_addr} not allowed. '
                f'Allowed IPs: {dicts_raw_token.get("allow_ips")} | '
                f'(request_data) {request.data} | '
                f'{request.remote_addr} {request.method} {request.path}'
            )
            return http_response_server_error('UNAUTHORIZED_API_TOKEN')
        return func(*args, **kwargs)
    return token_authentication
