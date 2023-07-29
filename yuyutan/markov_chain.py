from pathlib import Path

import markovify


class MarkovChain:
    def __init__(self, model_path: Path) -> None:
        with open(model_path, "r") as fp:
            model_json = fp.read()

        self.__model = markovify.Text.from_json(model_json)

    def make_short_sentence(self, length: int) -> str:
        sentence = self.__model.make_short_sentence(length)
        return "".join(sentence.split(" "))

    def make_sentence_with_start(self, beginning: str) -> str:
        sentence = self.__model.make_sentence_with_start(beginning=beginning)
        return "".join(sentence.split(" "))
