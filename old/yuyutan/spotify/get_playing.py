import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

scope = ["user-read-playback-state"]


def get_playing() -> str | None:
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope
        )
    )
    res = sp.current_user_playing_track()
    try:
        return str(res["item"]["external_urls"]["spotify"])
    except Exception:
        return None


if __name__ == "__main__":
    get_playing()
