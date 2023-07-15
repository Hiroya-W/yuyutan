from os import _Environ

from mastodon import Mastodon


class MastodonBot:
    def __init__(self, env: _Environ[str]) -> None:
        self.__env = env
        self.__api = Mastodon(
            api_base_url=env.get("MASTODON_API_BASE_URL", "http://localhost"),
            client_id=env.get("MASTODON_CLIENT_KEY", "mastodon_client_key"),
            client_secret=env.get("MASTODON_CLIENT_SECRET", "mastodon_client_secret"),
            access_token=env.get("MASTODON_ACCESS_TOKEN", "mastodon_access_token"),
        )

    def run(self) -> None:
        """
        Run the bot
        """
        raise NotImplementedError
