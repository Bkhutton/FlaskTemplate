from abc import ABC, abstractmethod


class Database(ABC):

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def register_user(self, username: str, password: str):
        pass

    @abstractmethod
    def get_user_by_username(self, username: str):
        pass
    
    @abstractmethod
    def get_user_by_id(self, id: int):
        pass

    @abstractmethod
    def test_if_unique(self, table, field, data):
        pass