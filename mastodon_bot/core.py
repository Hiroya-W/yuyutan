from os import _Environ

from sqlalchemy.orm import Session


class Bot:
    def __init__(self, env: _Environ[str], db: Session) -> None:
        self.__env = env
        self.__db = db

    def run(self) -> None:
        """
        Run the bot
        """
        raise NotImplementedError
