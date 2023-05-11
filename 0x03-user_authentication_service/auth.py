#!/usr/bin/env python3
""" Authentication """

import bcrypt
from db import DB, User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Converts a password string arguments to bytes
    Args:
        password: the string password to be converted to bytes
    Return:
        bytes (salted hash of the input password)
    """
    # convert the string to bytes (bcrypt expects bytes)
    password_bytes = password.encode('utf-8')

    # salt the password
    salt = bcrypt.gensalt()

    # hash the password
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers user by adding to the database or checking
        if already exists
        Args:
            email (str): email string arguments
            password(str): password
        Return:
            User (user object)
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(user.email))
