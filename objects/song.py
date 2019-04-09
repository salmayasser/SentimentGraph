class Song:

    def __init__(self, song_name, lyrics, valence):
        """
        Represents all needed and calculated fields for a song
        :param song_name: song's name
        :type song_name: str
        :param lyrics:  song's lyrics
        :type lyrics: str
        :param valence: song's valence
        :type valence: int
        """
        self.name = song_name
        self.lyrics = lyrics
        self.valence = valence
        self.lexD = None
        self.emotion = None
        self.sentiment = None
        self.color = None
        self.gloom = None

    def set_color(self, color):
        """
        :param color: sets calculated color of a song
        :type color: str
        """
        self.color = color

    def set_emotion(self, emotion):
        """
        :param emotion: sets calculated emotion of a song
        :type emotion: str
        """
        self.emotion = emotion

    def set_sentiment(self, sentiment):
        """
        :param sentiment: sets calculated sentiment of a song
        :type sentiment: str
        """
        self.sentiment = sentiment

    def set_gloom(self,gloom):
        """
        :param gloom: sets calculated gloom of a song
        :type gloom: float
        """
        self.gloom = gloom

    def set_lexD(self, lexD):
        """
        :param lexD: sets calculated lyrical density of a song
        :type lexD: float
        """
        self.lexD = lexD


