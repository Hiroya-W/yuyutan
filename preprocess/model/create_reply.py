from pathlib import Path
import MeCab
import sqlite3
import markovify

DATA_DIR = Path("datas")


def main() -> None:
    m = MeCab.Tagger(
        "-Owakati -d /usr/lib/aarch64-linux-gnu/mecab/dic/mecab-ipadic-neologd"
    )

    connect = sqlite3.connect(DATA_DIR / Path("twitter/replies.db"))
    cursor = connect.cursor()

    tweets = cursor.execute("SELECT tweet FROM tweets").fetchall()

    all_wakatigaki = []
    for tweet in tweets:
        wakatigaki = m.parse(str(tweet[0]))
        all_wakatigaki.append(wakatigaki)

    corpus = "\n".join(all_wakatigaki)
    model = markovify.NewlineText(corpus, state_size=3, well_formed=False)

    model_json = model.to_json()

    with open(DATA_DIR / Path("model/reply_model.json"), "w") as fp:
        fp.write(model_json)


if __name__ == "__main__":
    main()
