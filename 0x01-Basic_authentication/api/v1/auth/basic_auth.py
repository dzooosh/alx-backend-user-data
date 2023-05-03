#!/usr/bin/env python3
"""
BasicAuth class
"""
from .auth import Auth
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
