from abc import ABC, abstractmethod

from flask import Flask


class TestDatabase(ABC):

    # @abstractmethod
    def setup(self):
        pass
    
    # @abstractmethod
    def assert_user_exists(self, app: Flask, username: str):
        pass