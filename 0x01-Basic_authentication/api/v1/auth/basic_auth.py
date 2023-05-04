#!/usr/bin/env python3
"""
BasicAuth class
"""
from .auth import Auth
import base64
import re


class BasicAuth(Auth):
    """ Implement Basic Authorization
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Basic Base64 part of the Authorization header
        for a Basic Auth
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        match = re.search(r'Basic (.+)', authorization_header)
        if match:
            token = match.group(1)
            return token
        else:
            return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """ Decodes value of a Base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            # encode Base64 to string
            decoded = base64_authorization_header.encode('utf-8')
            # decode the string into binary data
            decoded = base64.b64decode(decoded)
            # convert the binary data to a string ('utf-8')
            return decoded.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> str:
        """ Extracts the user email and password from the Base64
        decoded value
        """
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        pattern = r'(.+):(.+)'
        match = re.search(pattern, decoded_base64_authorization_header)
        if match:
            user_email = match.group(1)
            user_password = match.group(2)
            return (user_email, user_password)
