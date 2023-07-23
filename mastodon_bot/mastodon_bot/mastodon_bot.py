from abc import ABC
from os import _Environ
from typing import Any

from mastodon import Mastodon

from mastodon_bot.mastodon_bot.streaming import (
    BotStreamListener,
    CallbackStreamListener,
)


class BotInterface(ABC):
    """
    Mastodon APIのインスタンスをどうにかして取得したかった
    BotInterfaceを実装しているクラスを受け取るようにしておけば
    モックなど、置き換えがしやすくなるかもしれない
    """

    def get_api_instance(self) -> Mastodon:
        ...

    def add_middleware(self, middleware: list[Any]) -> None:
        ...

    def add_listener(self, listener: CallbackStreamListener) -> None:
        ...

    def add_listener_many(self, listeners: list[CallbackStreamListener]) -> None:
        ...

    def run(self) -> None:
        ...


class MastodonBot(BotInterface):
    def __init__(self, env: _Environ[str]) -> None:
        self.__env = env
        self.__api = Mastodon(
            api_base_url=env.get("MASTODON_API_BASE_URL", "http://localhost"),
            client_id=env.get("MASTODON_CLIENT_KEY", "mastodon_client_key"),
            client_secret=env.get("MASTODON_CLIENT_SECRET", "mastodon_client_secret"),
            access_token=env.get("MASTODON_ACCESS_TOKEN", "mastodon_access_token"),
        )
        self.__listener = BotStreamListener()

        self.__middlewares: list[Any] = []

    def get_api_instance(self) -> Mastodon:
        """
        Get the Mastodon API
        """
        return self.__api

    def add_middleware(self, middleware: list[Any]) -> None:
        """
        Add a middleware to the bot
        """
        self.__middlewares.append(middleware)

    def add_listener(self, listener: CallbackStreamListener) -> None:
        """
        Add a listener to the bot
        """
        self.__listener.add_listener(listener)

    def add_listener_many(self, listeners: list[CallbackStreamListener]) -> None:
        """
        Add multiple listeners to the bot
        """
        for listener in listeners:
            self.add_listener(listener)

    def run(self) -> None:
        """
        Run the bot
        """
        self.__api.stream_user(self.__listener, run_async=True, reconnect_async=True)
