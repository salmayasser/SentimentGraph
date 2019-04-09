import spotipy
import spotipy.util as util


class Spotify:
    def __init__(self, username, client_id, client_secret, scope):
        """
        wrapper class for spotify API
        :param username: your spotify's username
        :param client_id: your client_id for spotify API
        :param client_secret: your client
        :param scope: your scope depending on your application
        """
        token = util.prompt_for_user_token(
            username=username,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri='http://dummyuri.com'
        )
        self.sp = spotipy.Spotify(auth=token)

    def get_artist(self, name):
        """
        get spotify's artist object
        :param name: name of the artist
        :type name: str
        :return: spotify's artist object
        """
        results = self.sp.search(q='artist:' + name, type='artist')
        items = results['artists']['items']
        if len(items) > 0:
            return items[0]
        else:
            return None

    def get_artist_albums(self, artist):
        """
        gets list of albums for an artist
        :param artist: spotify's object of an artist that we want to get albums for
        :return: list of spotify's albums objects
        """
        albums = []
        results = self.sp.artist_albums(artist['id'], album_type='album')
        albums.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])
        return albums

    def get_album_tracks(self, album):
        """
        gets list of tracks for an album
        :param album: spotify's object of an album that we want to get tracks for
        :return:  list of spotify's tracks objects
        """
        tracks = []
        results = self.sp.album_tracks(album['id'])
        tracks.extend(results['items'])
        while results['next']:
            results = self.sp.next(results)
            tracks.extend(results['items'])
        return tracks

    def get_valence_for_track(self, track_id):
        """
        gets valence for a track
        :param track_id: identification of the track we want to get valence for
        :return: float describes the musical positiveness conveyed by a track
        """
        track_audio_features = self. sp.audio_features([track_id])
        valence = -1.0
        if track_audio_features:
            valence = track_audio_features[0]['valence']
        return valence
