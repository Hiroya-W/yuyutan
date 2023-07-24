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

logger = logging.getLogger(__name__)


class CallbackStreamListener:
    """Mastodon Streaming APIのリスナー

    Note
    ----
    Mastodon.pyで用意されているStreamListenerではなく、これを継承してリスナーを作成する。
    継承先のクラスでは、必要なハンドラのみオーバーライドすれば良い。

    Mastodon Streaming APIで発生したイベントを受け取るのは、全てのリスナーを集約するBotStreamListenerが担う。
    """

    def __init__(
        self,
        update_handler: Optional[Any] = None,
        local_update_handler: Optional[Any] = None,
        delete_handler: Optional[Any] = None,
        notification_handler: Optional[Any] = None,
        conversation_handler: Optional[Any] = None,
        unknown_event_handler: Optional[Any] = None,
        status_update_handler: Optional[Any] = None,
        filters_changed_handler: Optional[Any] = None,
        announcement_handler: Optional[Any] = None,
        announcement_reaction_handler: Optional[Any] = None,
        announcement_delete_handler: Optional[Any] = None,
        encryted_message_handler: Optional[Any] = None,
    ) -> None:
        self.update_handler = update_handler
        self.local_update_handler = local_update_handler
        self.delete_handler = delete_handler
        self.notification_handler = notification_handler
        self.filters_changed_handler = filters_changed_handler
        self.conversation_handler = conversation_handler
        self.unknown_event_handler = unknown_event_handler
        self.status_update_handler = status_update_handler
        self.announcement_handler = announcement_handler
        self.announcement_reaction_handler = announcement_reaction_handler
        self.announcement_delete_handler = announcement_delete_handler
        self.encryted_message_handler = encryted_message_handler

    def on_update(self, status: Status) -> None:
        if self.update_handler is not None:
            self.update_handler(status)

    def on_delete(self, deleted_id: IdType) -> None:
        if self.delete_handler is not None:
            self.delete_handler(deleted_id)

    def on_notification(self, notification: Notification) -> None:
        if self.notification_handler is not None:
            self.notification_handler(notification)

    def on_filters_changed(self) -> None:
        if self.filters_changed_handler is not None:
            self.filters_changed_handler()

    def on_conversation(self, conversation: Conversation) -> None:
        if self.conversation_handler is not None:
            self.conversation_handler(conversation)

    def on_announcement(self, annoucement: Announcement) -> None:
        if self.announcement_handler is not None:
            self.announcement_handler(annoucement)

    def on_announcement_reaction(self, reaction: StreamReaction) -> None:
        if self.announcement_reaction_handler is not None:
            self.announcement_reaction_handler(reaction)

    def on_announcement_delete(self, annoucement_id: IdType) -> None:
        if self.announcement_delete_handler is not None:
            self.announcement_delete_handler(annoucement_id)

    def on_status_update(self, status: Status) -> None:
        if self.status_update_handler is not None:
            self.status_update_handler(status)

    def on_encrypted_message(self, unclear: AttribAccessDict) -> None:
        if self.encryted_message_handler is not None:
            self.encryted_message_handler(unclear)

    def on_unknown_event(self, name: Any, unknown_event: Optional[Any] = None) -> None:
        if self.unknown_event_handler is not None:
            self.unknown_event_handler(name, unknown_event)


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
