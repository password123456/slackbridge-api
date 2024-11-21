__author__ = 'https://github.com/password123456/'
__date__ = '2024.11.20'
__version__ = '1.0'
__status__ = 'Production'

from flask import request


def get_client_ip():
    # The client IP is not remote_addr, Get the client IP address from the X-Forwarded-For header.
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # If there are many IPs in the X-Forwarded-For header, the first IP is selected.
        return forwarded_for.split(',')[0].strip()
    return request.remote_addr
