#!/usr/bin/python3
"""Defines City class"""


from models.base_model import BaseModel


class City(BaseModel):
    """
    child class of BaseModel
    """
    state_id = ""
    name = ""
