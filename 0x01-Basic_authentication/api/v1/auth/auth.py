#!/usr/bin/env python3
""" API authentication class """
import flask
from typing import List, TypeVar
import re


class Auth():
    """ API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require authentication from user
        Return:
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
            return True

    def authorization_header(self, request=None) -> str:
        """ authorization_header
        request - Flask request object
        Return:
            - None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ checks the current user
        """
        return None
