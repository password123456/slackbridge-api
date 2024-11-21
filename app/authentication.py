__author__ = 'https://github.com/password123456/'
__date__ = '2024.11.19'
__version__ = '1.1'
__status__ = 'Production'

from flask import current_app
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode


def decrypt_api_token(encrypted_key):
    passphrase_key = get_key_data(encrypted_key)
    if not passphrase_key:
        return None

    try:
        passphrase_key = b64decode(passphrase_key)
        encrypted_key_bytes = b64decode(encrypted_key)

        nonce = encrypted_key_bytes[:12]
        tag = encrypted_key_bytes[12:28]
        ciphertext = encrypted_key_bytes[28:]

        decryptor = Cipher(
            algorithms.AES(passphrase_key),
            modes.GCM(nonce, tag),
            backend=default_backend()
        ).decryptor()

        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        result = decrypted_data.decode('utf-8')
        return result
    except Exception:
        return None


def get_key_data(encrypted_access_key):
    try:
        result = None
        with open(current_app.config['KEY_DB'], 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('#') or len(line.strip()) == 0:
                    continue
                split_line = line.split('|')
                if len(split_line) > 3 and str(split_line[3].strip()) == str(encrypted_access_key):
                    result = split_line[2].strip()
                    break
        return result
    except FileNotFoundError:
        return None
