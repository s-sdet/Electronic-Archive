import json
import requests
import logging
from requests import Response

logger = logging.getLogger("Electronic Archive")


class BaseClass:
    def __init__(self, app):
        self.app = app

    def to_dict(self) -> dict:
        """
        Метод конвертации вложенных объектов в словарь.
        """
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
