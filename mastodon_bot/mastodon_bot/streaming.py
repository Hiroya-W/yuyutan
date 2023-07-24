import logging
from typing import Any, Optional

from mastodon.streaming import StreamListener
from mastodon.types import (
    Announcement,
    AttribAccessDict,
    Conversation,
    IdType,
    Notification,
    Status,
    StreamReaction,
)

from .interfaces.streaming import CallbackStreamListener

logger = logging.getLogger(__name__)


class BotStreamListener(StreamListener):  # type: ignore
    """Mastodon Streaming APIの全てのリスナーが集約されるクラス

    Note
    ----
    各リスナーのハンドラはこのクラスから呼び出されるよう、add_listener()で登録しておく
    """

    def __init__(self) -> None:
        super(BotStreamListener, self).__init__()
        self.__listeners: list[CallbackStreamListener] = []

    def add_listener(self, listener: CallbackStreamListener) -> None:
        self.__listeners.append(listener)

    def on_update(self, status: Status) -> None:
        logger.debug("on_update: %s", status)
        for listener in self.__listeners:
            listener.on_update(status)

    def on_delete(self, deleted_id: IdType) -> None:
        logger.debug("on_delete: %s", deleted_id)
        for listener in self.__listeners:
            listener.on_delete(deleted_id)

    def on_notification(self, notification: Notification) -> None:
        logger.debug("on_notification: %s", notification)
        for listener in self.__listeners:
            listener.on_notification(notification)

    def on_filters_changed(self) -> None:
        logger.debug("on_filters_changed")
        for listener in self.__listeners:
            listener.on_filters_changed()

    def on_conversation(self, conversation: Conversation) -> None:
        logger.debug("on_conversation: %s", conversation)
        for listener in self.__listeners:
            listener.on_conversation(conversation)

    def on_announcement(self, annoucement: Announcement) -> None:
        logger.debug("on_announcement: %s", annoucement)
        for listener in self.__listeners:
            listener.on_announcement(annoucement)

    def on_announcement_reaction(self, reaction: StreamReaction) -> None:
        logger.debug("on_announcement_reaction: %s", reaction)
        for listener in self.__listeners:
            listener.on_announcement_reaction(reaction)

    def on_announcement_delete(self, annoucement_id: IdType) -> None:
        logger.debug("on_announcement_delete: %s", annoucement_id)
        for listener in self.__listeners:
            listener.on_announcement_delete(annoucement_id)

    def on_status_update(self, status: Status) -> None:
        logger.debug("on_status_update: %s", status)
        for listener in self.__listeners:
            listener.on_status_update(status)

    def on_encrypted_message(self, unclear: AttribAccessDict) -> None:
        logger.debug("on_encrypted_message: %s", unclear)
        for listener in self.__listeners:
            listener.on_encrypted_message(unclear)

    def on_unknown_event(self, name: Any, unknown_event: Optional[Any] = None) -> None:
        logger.debug("on_unknown_event: %s, %s", name, unknown_event)
        for listener in self.__listeners:
            listener.on_unknown_event(name, unknown_event)
