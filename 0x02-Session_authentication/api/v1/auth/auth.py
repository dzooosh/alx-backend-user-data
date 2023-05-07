#!/usr/bin/env python3
""" API authentication class """
from flask import request
from typing import List, TypeVar
import re
from os import getenv

class Auth():
    """ API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require authentication from user
        Return:
            - True: if path is None or path is not in excluded_paths
            - False: if path in excluded_path
        """
        if path is None:
            return True
        if (excluded_paths is None or excluded_paths == []):
            return True
        else:
            for e_path in excluded_paths:
                pattern = r'{}/?$'.format(re.escape(e_path))
                if re.match(path, pattern):
                    return False
                if e_path[-1] == "*":
                    if path.startswith(e_path[:-1]):
                        return False
            return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        request - Flask request object
        Return:
            - None or
                the value of the Authorization request header
        """
        if request is None:
            return None
        if not request.headers.get('Authorization'):
            return None
        else:
            return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ checks the current user
        """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request
        """
        if request is None:
            return None
        cookie_name = getenv("SESSION_NAME")
        cookie_value = request.cookies.get(cookie_name, None)
        return cookie_value
