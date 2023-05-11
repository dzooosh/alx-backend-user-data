#!/usr/bin/env python3
""" Authentication """

import bcrypt
from db import DB, User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid
from typing import Union, TypeVar


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


def _generate_uuid() -> str:
    """ Generates a uuid
    """
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ validates credentials
        Args:
            email (str): email to validate
            password (str): password to validate
        Returns:
            True - if it matches with user details
            False - if it does not match
        """
        try:
            user = self._db.find_user_by(email=email)
            # use bcrypt.checkpw to check the password with password in db
            return bcrypt.checkpw(password.encode('utf-8'),
                                  getattr(user, 'hashed_password'))
        except (NoResultFound):
            return False

    def create_session(self, email: str) -> Union[None, str]:
        """ Get session ID
        Args:
            email (str): email string
        Returns:
            session ID (str)
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None
