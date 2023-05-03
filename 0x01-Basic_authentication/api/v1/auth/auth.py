#!/usr/bin/env python3
""" API authentication class """
import flask
from typing import List, TypeVar


class Auth():
    """ API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require authentication from user
        Return:
        """
        return False

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
