#!/usr/bin/env python3
""" Authentication """

import bcrypt


def _hash_password(self, password: str) -> bytes:
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
