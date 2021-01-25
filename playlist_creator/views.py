from django.shortcuts import render
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config


# Create your views here.
def home(request):
    return render(request, "playlist_creator/index.html")


def music(request):
    sp_curr = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=config.client_id,
                                                        client_secret=config.client_secret,
                                                        redirect_uri="http://localhost:8888/callback",
                                                        scope="user-library-read user-top-read playlist-modify-public"))

    def get_top_artists(sp):
        top_artists = sp.current_user_top_artists(time_range="short_term", limit=10)

        top_artists_uri = []

        for i in top_artists["items"]:
            top_artists_uri.append("https://open.spotify.com/embed/artist/" + i["id"])

        return top_artists_uri

    top_artist = get_top_artists(sp_curr)
    return render(request, "playlist_creator/music.html", {"artists": top_artist})
