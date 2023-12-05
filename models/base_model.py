#!/usr/bin/env python3

"""BaseModel class for AirBnB"""

import uuid
from datetime import datetime


class BaseModel:
    """
    BaseModel class for AirBnB
    """

    def __init__(self) -> None:
        """
        Initialize BaseModel class
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self) -> None:
        """
        Print BaseModel class
        """
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """
        Updates the public instance attribute updated_at with the current datetime
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of __dict__ of the instance
        """
        return self.__dict__.copy()
