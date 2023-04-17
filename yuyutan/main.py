from pathlib import Path
import markovify

DATA_DIR = Path("datas")


def main() -> None:
    with open(DATA_DIR / Path("model/model.json"), "r") as fp:
        model_json = fp.read()
    model = markovify.Text.from_json(model_json)

    for _ in range(10):
        sentece = model.make_short_sentence(140)
        print("".join(sentece.split()))


if __name__ == "__main__":
    main()
