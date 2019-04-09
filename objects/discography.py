import threading

from objects.album import Album
from objects.song import Song


class Discography:

    def __init__(self,spotify_client, genius_client):
        """
        Responsible for collecting a discography for an artist that we want to analyse
        :param spotify_client: An object of Spotify API
        :param genius_client: An object of  Genius API
        """
        self.spotify_client = spotify_client
        self.genius_client = genius_client
        self.albums = []

    def get_valence(self, track_id):
        """
        Responsible for getting song's valence
        :param track_id: Spotify ID
        :type track_id: str
        :return: float representing song's valence
        """
        return self.spotify_client.get_valence_for_track(track_id)

    def get_lyrics_for_track(self,track_id, track_name, artist_name,  song_list):
        """
        Responsible for getting lyrics and track for each song
        :param track_id: spotify ID
        :type track_id: str
        :param track_name: name of the song
        :type track_name: str
        :param artist_name: name of the artist singing the song
        :type artist_name: str
        :param song_list: a list song objects carrying songs information needed for analysis
        :type song_list: list
        """
        valence = self.get_valence(track_id)
        lyrics = self.genius_client.get_lyrics_for_track(track_name, artist_name)
        if lyrics:
            curr_song = Song(track_name, lyrics, valence)
            song_list.append(curr_song)

    def show_album_tracks(self, album, artist_name):
        """
        creating list of songs objects by gathering valence and lyrics information

        :param album: Spotify object with information about the album
        :type album: dict ( Spotify's album object )
        :param artist_name: name of the artist te help us get the lyrics of each song later on
        :type artist_name: str
        :return: bool answering the question : were we able to create an object for any of the songs in this album ?
               : List of songs objects
        """
        results = self.spotify_client.get_album_tracks(album)
        any_song_added = False
        song_list = []
        threads = []
        for track in results:
            th = threading.Thread(
                target=self.get_lyrics_for_track,
                args=(
                    track['id'],
                    track['name'],
                    artist_name,
                    song_list
                )
            )
            th.start()
            threads.append(th)

        for thread in threads:
            thread.join()

        if len(song_list):
            any_song_added = True

        return any_song_added, song_list

    def get_discography(self, artist):
        """
        creating a list of albums objects
        :param artist: Spotify object
        :type artist: dict
        """
        results = self.spotify_client.get_artist_album(artist)
        unique = set()  # skip duplicate albums
        for album in results:
            name = album['name'].lower()
            if name not in unique:
                unique.add(name)
                any_song_added, song_list = self.show_album_tracks(album, artist['name'])
                if any_song_added:
                    curr_album = Album(name)
                    curr_album.set_songs(song_list)
                    self.albums.append(curr_album)
