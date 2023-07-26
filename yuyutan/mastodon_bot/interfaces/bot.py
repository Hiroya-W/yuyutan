from abc import ABC

from mastodon import Mastodon

from .functions import BotFunctionInterface
from .streaming import CallbackStreamListener


class BotInterface(ABC):
    """
    Note
    ----
    Mastodon APIのインスタンスをどうにかして取得したかった
    BotInterfaceを実装しているクラスを受け取るようにしておけば
    モックなど、置き換えがしやすくなるかもしれない
    """

    def get_api_instance(self) -> Mastodon:
        ...

    def add_listener(self, listener: CallbackStreamListener) -> None:
        ...

    def add_listener_many(self, listeners: list[CallbackStreamListener]) -> None:
        ...

    def add_function(self, function: BotFunctionInterface) -> None:
        ...

    def run(self) -> None:
        ...
