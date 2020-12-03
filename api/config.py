"""
.. module:: Config
    :platform: Platform Independent
    :synopsis: This module has commonly used config parameters
"""

import os


class Config:
    def __init__(self):
        os.environ["PYTHONUNBUFFERED"] = "1"

