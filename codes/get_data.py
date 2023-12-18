import os
import config 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import time
import pandas as pd 

# -----------------------------
# Get ID of selected artist
# Look for search

def getArtist_ID(author, sp):
    """
    Retrieves the IDs of artists on Spotify based on the given author's name.

    Inputs:
    - `author` (string): The name of the author to search for.

    Outputs:
    - `artist_id` (list): A list of artist IDs.
    """

    # Initialize an empty list to store artist IDs
    artist_id = []
    
    # Search for artists on Spotify based on the provided author name
    results = sp.search(author, type='artist', limit=3)

    # Extract the 'items' field from the search results
    allArtists = results['artists']['items']

    # Iterate over each artist in the search results
    for artist in allArtists:
        # Extract the ID of the artist and add it to the artist_id list
        artist_id.append(artist['id'])
        
        print(artist['name'], artist['id'])
        print('----------------------------------------\n')
    # Return the list of artist IDs
    return artist_id

# -----------------------------
## Get tracks features
def getTrack_features(artist_id, sp):
    """
    Retrieves various features of tracks by an artist on Spotify based on the given artist ID.

    Inputs:
    - `artist_id` (string): The ID of the artist to retrieve track features for.

    Outputs:
    - `tracks` (list): A list containing various features of the tracks by the artist.
    """

    # Get albums by the artist using the provided artist ID
    albums = sp.artist_albums(artist_id)

    # Initialize an empty list to store track IDs
    track_ids = []
    
    # Iterate over each album in the search results
    for album in albums['items']:
        album_id = album['id']
        # Get the tracks of the album
        album_tracks = sp.album_tracks(album_id)
        # Iterate over each track in the album and append its ID to track_ids list
        for track in album_tracks['items']:
            track_ids.append(track['id'])

    # Initialize an empty list to store track features
    tracks = []

    # Iterate over each track ID
    for track in track_ids:
        # Get the track information and audio features using the track ID
        track_info = sp.track(track)
        track_features = sp.audio_features(track)[0]

        # Extract the desired features from the track information and audio features
        track_name = track_info['name']
        track_id = track_info['id']
        track_duration = track_info['duration_ms'] / 1000
        track_popularity = track_info['popularity']
        track_url = track_info['external_urls']['spotify']
        track_uri = track_info['uri']

        # Extract the track features, replacing null values with None
        if track_features: 
            track_danceability = track_features['danceability']
            track_energy = track_features['energy'] 
            track_key = track_features['key'] 
            track_loudness = track_features['loudness']
            track_speechiness = track_features['speechiness']
            track_acousticness = track_features['acousticness']
            track_instrumentalness = track_features['instrumentalness']
            track_liveness = track_features['liveness'] 
            track_valence = track_features['valence'] 
            track_tempo = track_features['tempo'] 
            track_time_signature = track_features['time_signature']
    
            # Create a list containing the extracted track features
            tracks_features = [track_name, track_id, track_duration, track_popularity, 
                               track_url, track_uri, track_energy, track_danceability, 
                               track_key, track_loudness, track_speechiness, track_acousticness, 
                               track_instrumentalness, track_liveness, track_valence, 
                               track_tempo, track_time_signature]

            # Add the track features to the tracks list
            tracks.append(tracks_features)

    return tracks


# -----------------------
# Make df with songs scrapepd
def make_df(data):
    # Change column names of df
    Columns = ['track_name', 'track_id', 'track_duration', 'track_popularity', 
              'track_url', 'track_uri', 'track_danceability', 'track_energy', 
              'track_key', 'track_loudness', 'track_speechiness', 'track_acousticness', 
              'track_instrumentalness', 'track_liveness', 'track_valence', 'track_tempo', 
              'track_time_signature']
    
    df = pd.DataFrame(data)
    df.columns = Columns

    return df

# --------------------------------