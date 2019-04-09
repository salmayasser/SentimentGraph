import sys

from secrets import SPOTIFY_SCOPE
from secrets import SPOTIFY_USERNAME
from secrets import SPOTIFY_CLIENT_ID
from secrets import SPOTIFY_CLIENT_SECRET
from secrets import GENIUS_TOKEN
from api.spotify import Spotify
from api.genius import Genius
from objects.artist import Artist
from sentiment_analyzer import SentimentAnalyzer
import json

if __name__ == '__main__':
    """
    Entry point of the program, receives three command line arguments:
    artist_name: name of the artist whose discography we want to analyze.
    lexicon_file: location of the lexicon file
    categories_file: location of the categories file 
    """

    artist_name = sys.argv[1]
    lexicon_file = sys.argv[2]
    categories_file = sys.argv[3]

    spotify_client = Spotify(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        scope=SPOTIFY_SCOPE,
        username=SPOTIFY_USERNAME
    )
    genius_client = Genius(
        token=GENIUS_TOKEN
    )
    my_artist = Artist(
        artist_name,
        spotify_client,
        genius_client
    )

    my_artist.get_artist()
    my_artist.show_artist()
    my_artist.get_discography()

    analyzer = SentimentAnalyzer(lexicon_file, categories_file)
    dataset = {}
    for album in my_artist.discography.albums:
        album_songs = []
        for song in album.songs:
            color, emotion, sentiment, gloom = analyzer.analyze(song)
            album_songs.append(
                dict(
                    song_name=song.name,
                    gloom=gloom,
                    sentiment=sentiment,
                    emotion=emotion
                )
            )
        dataset[album.album_name] = album_songs

    dataset_json = json.dumps(dataset)
    print(dataset_json)