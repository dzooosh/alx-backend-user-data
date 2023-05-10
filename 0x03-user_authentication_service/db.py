#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import re
import bcrypt

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to database
        Args:
            email (str): user's email address
            hashed_password (str): password hashed by bcrypt's hashpw
        Return:
            Newly created User object
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ finds user by any stated parameter
         Args:
            attributes (dict): a dictionary of attributes to match the user
        Return:
            matching user or raise error
        """
        users = self._session.query(User)
        for k, v in kwargs.items():
            if not hasattr(User, k):
                raise InvalidRequestError
            for user in users:
                if getattr(user, k) == v:
                    return user
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Updates user database using user_id to search
        Args:
            user_id: User ID which is unique to one user
            attributes (dict): a dictionary of attributes to update user data
        Return:
            None or raise error
        """
        user = self.find_user_by(id=user_id)
        for k, v in kwargs.items():
            if not hasattr(user, k):
                raise ValueError
            setattr(user, k, v)
        self._session.commit()
