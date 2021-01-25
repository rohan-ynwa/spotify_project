import spotipy
from spotipy.oauth2 import SpotifyOAuth
import statistics

moods = ["mellow", "melancholy", "happy", "sad", "cheerful", "angry"]
track_Valence = []
median_Valence = 0
stdev_Valence = 0
track_Tempo = []
mean_Tempo = 0
stdev_Tempo = 0
track_Energy = []
mean_Energy = 0
stdev_Energy = 0

#current mood
curr_mood = "Happy"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="326a452a53254fa9bc90368567c70861", client_secret = "7d518966cb804f019a4301db077c1c31", redirect_uri = "http://localhost:8888/callback", scope = scope))

def get_top_artists(sp):

    top_artists = sp.current_user_top_artists(time_range = "short_term", limit = 10)

    top_artists_uri = []

    for i in top_artists["items"]:
        top_artists_uri.append(i["uri"])

    return top_artists_uri

def get_top_tracks(sp, top_artists):

    top_tracks_uri = []
    for i in top_artists:
        top_tracks_all_data = sp.artist_top_tracks(i)
        top_tracks_data = top_tracks_all_data['tracks']
        for track_data in top_tracks_data:
            top_tracks_uri.append(track_data['uri'])

    return top_tracks_uri

def get_valence(sp, top_tracks_uri):
    track_Valence = []
    for tracks in top_tracks_uri:
        tracks_all_data = sp.audio_features(tracks)
        for track_data in tracks_all_data:
            track_Valence.append(track_data["valence"])
    return track_Valence


def get_mean_Valence(track_Valence):
    mean_Valence = statistics.mean(track_Valence)
    return mean_Valence

def get_stdev_Valence(track_Valence):
    stdev_Valence = statistics.stdev(track_Valence)
    return stdev_Valence


def get_tempo(sp, top_tracks_uri):

    for tracks in top_tracks_uri:
        tracks_all_data = sp.audio_features(tracks)
        for track_data in tracks_all_data:
            track_Tempo.append(track_data["tempo"])

def get_mean_Tempo(track_Tempo):
    mean_Tempo = statistics.mean(track_Tempo)
    return mean_Tempo

def get_stdev_Tempo(track_Tempo):
    stdev_Tempo = statistics.stdev(track_Tempo)
    return stdev_Tempo

def get_energy(sp, top_tracks_uri):

    for tracks in top_tracks_uri:
        tracks_all_data = sp.audio_features(tracks)
        for track_data in tracks_all_data:
            track_Energy.append(track_data["energy"])

def get_mean_Energy(track_Energy):
    mean_Energy = statistics.mean(track_Energy)
    return mean_Energy

def get_stdev_Energy(track_Energy):
    stdev_Energy = statistics.stdev(track_Energy)
    return stdev_Energy


# high_valence = all valence greater than equal to mean_valence + stddev_valence

# medium_valence = all valence between mean_valence - stddev_valence & mean_valence + stddev_valence

# low_valence = all valence lesser than mean_valence - stddev_valence

# Mellow - Major, High valence, Low tempo, Low energy
# Melancholy - Minor, low valence, Low tempo, Low energy

# Happy - Major, high valence, medium tempo, medium energy
# Sad - Minor, low valence, medium tempo, medium energy

# Cheerful- Major, High valence, High tempo, High energy
# Angry - Minor, low valence, High tempo, High energy


def select_the_tracks(sp, top_tracks_uri, mood):
    selected_tracks_uri = []

    mean_Valence = get_mean_Valence(get_valence(sp, top_tracks_uri))

    for tracks in top_tracks_uri:
        tracks_all_data = sp.audio_features(tracks)
        for track_data in tracks_all_data:

            if mood == "Mellow":
                if track_data["mode"] == 1  and track_data["valence"] >= (mean_Valence + stdev_Valence): # and track_data["tempo"] < (mean_Tempo - stdev_Tempo)and track_data["energy"] < (mean_Energy - stdev_Energy):
                    selected_tracks_uri.append(track_data["uri"])
            if mood == "Melancholy":
                if track_data["mode"] == 0 and track_data["valence"] < (mean_Valence - stdev_Valence): # and track_data["tempo"] < (mean_Tempo - stdev_Tempo) and track_data["energy"] < (mean_Energy - stdev_Energy):
                    selected_tracks_uri.append(track_data["uri"])
            if mood == "Happy":
                if track_data["mode"] == 1 and track_data["valence"] >= (mean_Valence + stdev_Valence): # and ((mean_Tempo - stdev_Tempo) < track_data["tempo"] < (mean_Tempo + stdev_Tempo)) and ((mean_Energy - stdev_Energy) < track_data["energy"] < (mean_Energy + stdev_Energy))
                    selected_tracks_uri.append(track_data["uri"])
            if mood == "Sad":
                if track_data["mode"] == 0 and track_data["valence"] < (mean_Valence - stdev_Valence): # and ((mean_Tempo - stdev_Tempo) < track_data["tempo"] < (mean_Tempo + stdev_Tempo)) and ((mean_Energy - stdev_Energy) < track_data["energy"] < (mean_Energy + stdev_Energy)):
                    selected_tracks_uri.append(track_data["uri"])
            if mood == "Cheerful":
                if track_data["mode"] == 1 and track_data["valence"] >= (mean_Valence + stdev_Valence): # and track_data["tempo"] >= (mean_Tempo + stdev_Tempo) and track_data["energy"] >= (mean_Energy + stdev_Energy):
                    selected_tracks_uri.append(track_data["uri"])
            if mood == "Angry":
                if track_data["mode"] == 0 and track_data["valence"] < (mean_Valence - stdev_Valence): # and track_data["tempo"] >= (mean_Tempo + stdev_Tempo) and track_data["energy"] >= (mean_Energy + stdev_Energy):
                    selected_tracks_uri.append(track_data["uri"])



    return selected_tracks_uri


#creates and names the playlist for the user using the tracks found in the the select_the_tracks method
def make_playlist(sp, selected_tracks_uri, mood):
    user_all_data = sp.current_user()
    user_id = user_all_data["id"]
    playlist_all_data = sp.user_playlist_create(user_id, mood)
    playlist_id = playlist_all_data["id"]
    sp.user_playlist_add_tracks(user_id, playlist_id, selected_tracks_uri)
