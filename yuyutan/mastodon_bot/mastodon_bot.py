import threading
from os import _Environ

from mastodon import Mastodon

from .interfaces.bot import BotInterface
from .interfaces.functions import BotFunctionInterface
from .streaming import BotStreamListener, CallbackStreamListener


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
        self.__functions: list[BotFunctionInterface] = []

    def get_api_instance(self) -> Mastodon:
        """
        Get the Mastodon API
        """
        return self.__api

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

    def add_functions(self, functions: list[BotFunctionInterface]) -> None:
        """
        Add a function to the bot
        """
        for function in functions:
            self.__functions.append(function)

    def run(self) -> None:
        """
        Run the bot
        """
        self.__api.stream_user(self.__listener, run_async=True, reconnect_async=True)

        for function in self.__functions:
            # スレッドで各機能を並列実行しておく
            # こうすることで、各機能がブロックすることなく、他の機能が実行されるようになる
            # loggingはスレッドセーフなので、各機能でloggingを使っても問題ない
            threading.Thread(
                target=function.run, daemon=True  # メインスレッドが終了したら、各スレッドも終了するように
            ).start()
