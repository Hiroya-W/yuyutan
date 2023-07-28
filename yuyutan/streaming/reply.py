from datetime import timedelta
import logging
import random
from pathlib import Path

from mastodon import Mastodon
from mastodon.types import Notification
from rq_scheduler import Scheduler
from spacy.lang.ja import Japanese

from ..markov_chain import MarkovChain
from ..mastodon_bot.interfaces.bot import BotInterface
from ..mastodon_bot.interfaces.streaming import CallbackStreamListener

logger = logging.getLogger(__name__)


DATA_DIR = Path(__file__).parent.parent.parent / "datas"
MODEL_DIR = DATA_DIR / "model"

MAX_REPLY_LENGTH = 5


class ReplyHandler(CallbackStreamListener):
    def __init__(self, bot_instance: BotInterface, scheduler: Scheduler) -> None:
        super().__init__()
        self.__api = bot_instance.get_api_instance()
        self.__scheduler = scheduler
        self.__markov_chain = MarkovChain(MODEL_DIR / "model.json")

    def on_notification(self, notification: Notification) -> None:
        if notification.type == "mention":
            logger.info(f"@{notification.account.acct} mentioned you")
            self.__normal_reply(notification)

    def __normal_reply(self, notification: Notification) -> None:
        from_account = notification.account
        status = notification.status
        content = notification.status.content
        context = self.__api.status_context(status.id)

        if len(context.ancestors) >= MAX_REPLY_LENGTH:
            # あくあたんが無限にリプライを飛ばしてくるので、上限を設ける
            # Botアカウントかどうかでリプライ上限を設定するのもありかも
            logger.debug("Reply length is too long. Skip replying.")
            return

        nlp = Japanese()
        doc = nlp(content)

        candidates = []

        for word in nlp(doc):
            # それっぽい文章にするために、単語として選択する品詞を絞る
            # 名詞だけだと生成できる文章が限られてしまう
            if word.pos_ in ["ADV", "NOUN", "ADJ", "VERB"]:
                try:
                    sentence = self.__markov_chain.make_sentence_with_start(
                        beginning=word.text
                    )
                    sentence = "".join(sentence.split(" "))
                    if len(sentence) < 140:
                        candidates.append(sentence)
                except Exception:
                    # word.textから始まる文章が生成できなかった場合に発生する
                    # 生成出来た文章のみが候補なので、出来なくても問題ない
                    pass

        # 候補がない場合は、ランダムに文章を生成する
        if candidates == []:
            sentence = self.__markov_chain.make_short_sentence(140)
            sentence = "".join(sentence.split(" "))
            candidates.append(sentence)

        random.shuffle(candidates)
        sentence = candidates[0]

        reply_str = f"@{from_account.username} {sentence}"
        logger.info(f"Reply: {reply_str}")

        self.__scheduler.enqueue_in(
            timedelta(seconds=5), self._reply, status.id, reply_str
        )

    @staticmethod
    def _reply(api: Mastodon, reply_to_status_id: str, sentence: str) -> None:
        # api.status_post(
        #     f"@{notification.account.acct} Hello!", in_reply_to_id=notification.status.id
        # )
        pass
