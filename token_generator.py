__author__ = 'https://github.com/password123456/'
__date__ = '2023.02.11'
__version__ = '1.1'
__status__ = 'Production'

# Required library: cryptography
# This script provides functionalities for encrypting, decrypting, and validating API tokens.
# Tokens are encrypted using AES-GCM, a secure encryption mode that provides confidentiality and integrity.
# Additionally, tokens are validated for expiration and IP address restrictions.

import os
import sys
import json
from datetime import datetime, timedelta
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt(original_api_token_string, passphrase_key, nonce):
    """
    Encrypts an API token string using AES-GCM encryption.
    Args:
        original_api_token_string (str): The plaintext API token to encrypt.
        passphrase_key (bytes): The key used for encryption (must be 32 bytes for AES-256).
        nonce (bytes): A 12-byte nonce for AES-GCM (unique for each encryption).
    Returns:
        str: The encrypted token, encoded in base64 format.
    """
    encryptor = Cipher(
        algorithms.AES(passphrase_key),
        modes.GCM(nonce),
        backend=default_backend()
    ).encryptor()

    encrypted_data = encryptor.update(original_api_token_string.encode()) + encryptor.finalize()
    # Combine nonce, GCM tag, and encrypted data, and encode it in base64
    encrypted_api_token = b64encode(nonce + encryptor.tag + encrypted_data).decode('utf-8')
    return encrypted_api_token

def decrypt(keydb, encrypted_api_token):
    """
    Decrypts an encrypted API token.
    Args:
        keydb (str): Path to the database file containing keys and tokens.
        encrypted_api_token (str): The encrypted token to decrypt.
    Returns:
        str: The decrypted API token string, or None if decryption fails.
    """
    original_api_token_string = None
    passphrase_key = get_key_data(keydb, encrypted_api_token)

    try:
        if passphrase_key:
            passphrase_key = b64decode(passphrase_key)
            encrypted_api_token_bytes = b64decode(encrypted_api_token)
            # Extract nonce, GCM tag, and ciphertext
            nonce = encrypted_api_token_bytes[:12]
            tag = encrypted_api_token_bytes[12:28]
            ciphertext = encrypted_api_token_bytes[28:]

            # Initialize the AES-GCM decryptor
            decryptor = Cipher(
                algorithms.AES(passphrase_key),
                modes.GCM(nonce, tag),
                backend=default_backend()
            ).decryptor()

            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            original_api_token_string = decrypted_data.decode('utf-8')
    except Exception as e:
        print(str(e))

    return original_api_token_string

def write_to_db(keydb, app_id, passphrase_key, encrypted_api_token):
    """
    Writes encrypted token and associated data to the database file.
    Args:
        keydb (str): Path to the database file.
        app_id (str): The application ID.
        passphrase_key (bytes): The encryption key used (base64 encoded).
        encrypted_api_token (str): The encrypted token.
    """
    try:
        mode = 'a' if os.path.exists(keydb) else 'w'
        with open(keydb, mode, encoding='utf-8') as f:
            f.write(f'{datetime.now()}|{app_id}|{b64encode(passphrase_key).decode("utf-8")}|{encrypted_api_token}\n')
    except Exception as e:
        print(str(e))

def get_key_data(keydb, encrypted_api_token):
    """
    Retrieves the passphrase key associated with an encrypted token from the database.
    Args:
        keydb (str): Path to the database file.
        encrypted_api_token (str): The token for which to retrieve the key.
    Returns:
        str: The base64 encoded passphrase key, or None if not found.
    """
    passphrase_key = None
    with open(keydb, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            if line.split('|')[3].strip() == encrypted_api_token:
                passphrase_key = line.split('|')[2].strip()
                break
    return passphrase_key

def validate_access_key(access_key, remote_addr):
    """
    Validates the access key based on expiration and allowed IP addresses.
    Args:
        access_key (str): The decrypted API token string in JSON format.
        remote_addr (str): The IP address of the client requesting access.
    Returns:
        bool: True if the key is valid, otherwise False.
    """
    current_timestamp = int(datetime.now().timestamp())
    try:
        access_key = json.loads(access_key)

        # Check if the key contains an expiration time and validate it
        if 'exp' not in access_key:
            raise KeyError('exp key is missing')

        if current_timestamp > int(access_key["exp"]):
            print('Key is expired')
            return False

        # Check if the remote IP is in the allowed list
        if 'allow_ips' not in access_key:
            raise KeyError('allow_ips key is missing')

        if remote_addr in access_key['allow_ips']:
            return True
        else:
            return False
    except (KeyError, ValueError) as e:
        print(f'Validation error: {str(e)}')
        return False

def main():
    """
    Main function to demonstrate token encryption, decryption, and validation.
    """
    home_path = os.path.dirname(os.path.realpath(__file__))
    keydb = os.path.join(home_path, 'app/db/keys.db')

    # Generate a random 32-byte key and a 12-byte nonce
    passphrase_key = os.urandom(32)
    nonce = os.urandom(12)

    # Define token metadata
    issuer = 'token_generator'
    app_id = 'apne2-billing01.mydomain.com'  # The name of the service that will use the access token (identifier name)
    iat_time = datetime.now()
    exp_time = iat_time + timedelta(days=90)
    allow_ips = ['10.10.100.12', '10.10.100.3']  # Client IPs where AccessToken is allow

    # Create the original API token as a JSON object
    original_api_token_string = json.dumps({
        'iss': issuer,
        'app_id': app_id,
        'iat': int(iat_time.timestamp()),
        'exp': int(exp_time.timestamp()),
        'allow_ips': allow_ips
    })

    # Encrypt and store the token
    encrypted_access_key = encrypt(original_api_token_string, passphrase_key, nonce)
    write_to_db(keydb, app_id, passphrase_key, encrypted_access_key)

    # Decrypt and validate the token
    decrypted_access_key = decrypt(keydb, encrypted_access_key)
    if decrypted_access_key:
        validate_access_key(decrypted_access_key, '192.168.10.1')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as error:
        print(str(error))


"""
Original Text API Token: {'iss': 'token_generator', 'app_id': 'apne2-billing01.mydomain.com', 'iat': 1732238479, 'exp': 1740014479, 'allow_ips': ['10.10.100.12', '10.10.100.3']}
Passphrase Key: XceT4hVQq0oialnTm/0UOb+6z2MIt67YCPfEOUKVVIg=
Encrypted API Token: ADyimO+utkMkFTtjVhDLAJBKpvSI5zMXUFeHdY8pFMRSXGRKhg3vhtLMCVhFe+uXx+z4JB8Wnhada3ePwTsLTFeZizPuYyjIWJjlhAjn3r/QAkntAqowRSO0LVrSprDV9UJyBT/1QHo+3qOh/2Qvm+SKBPl+nMuVun7RroO+WlOtzaOqoDYWgFCNu0NRFQXVeSP7PMv5zt9CLobSzYtgy/Kkf+E=
Encrypted API Token Length: 220
Decrypted API Token: {"iss": "token_generator", "app_id": "apne2-billing01.mydomain.com", "iat": 1732238479, "exp": 1740014479, "allow_ips": ["10.10.100.12", "10.10.100.3"]}
Access key Expiration: 1740014479
- Key is valid
Access Key Allowed: ['10.10.100.12', '10.10.100.3']
 - Remote address 192.168.10.1 is not allowed
"""
