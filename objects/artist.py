from objects.discography import Discography


class Artist:
    def __init__(self, artist_name, spotify_client, genius_client):
        """
        Represents an artist whose discography will be analyzed.
        :param artist_name: Name of the artist
        :type artist_name: str
        :param spotify_client: An object of Spotify API
        :param genius_client: An object of  Genius API
        """
        self.artist_name = artist_name
        self.spotify_client = spotify_client
        self.genius_client = genius_client
        self.discography = None
        self.artist = None

    def get_artist(self):
        """
       Uses Spotify's API to load an artist info
        """
        self.artist = self.spotify_client.get_artist(self.artist_name)

    def get_discography(self):
        """
        Uses Spotify's API and Genius's API to load artist's discography to be analyzed
        """
        disco = Discography(self.spotify_client, self.genius_client )
        self.discography = disco.get_discography(self.artist)

    def show_artist(self):
        """
        shows some collected information about the artist from spotify's API
        """
        print('====', self.artist['name'], '====')
        print('Popularity: ', self.artist['popularity'])
        if len(self.artist['genres']) > 0:
            print('Genres: ', ','.join(self.artist['genres']))
