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

    def add_listeners(self, listener: list[CallbackStreamListener]) -> None:
        ...

    def add_functions(self, function: list[BotFunctionInterface]) -> None:
        ...

    def run(self) -> None:
        ...
