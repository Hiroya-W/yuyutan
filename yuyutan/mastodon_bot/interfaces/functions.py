from abc import ABC


class BotFunctionInterface(ABC):
    def run(self) -> None:
        """

        Note
        ----
        実装は基本的にwhile Trueするようなもの
        この関数をスレッドで実行することを想定している
        """
        ...
