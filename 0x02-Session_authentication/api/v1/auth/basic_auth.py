#!/usr/bin/env python3
"""
BasicAuth class
"""
from .auth import Auth
import base64
import re
from typing import List, TypeVar
from models.user import User


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
        pattern = r'([^:]+):(.+)'
        match = re.search(pattern, decoded_base64_authorization_header)
        if match:
            user_email = match.group(1)
            user_password = match.group(2)
            return (user_email, user_password)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on Email and Password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for u in users:
                if u.is_valid_password(user_pwd):
                    return u
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user instance
        """
        Auth_header = self.authorization_header(request)
        if Auth_header is not None:
            token = self.extract_base64_authorization_header(Auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, pswd = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(email, pswd)
        return
