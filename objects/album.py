class Album:

    def __init__(self, name):
        """
           Represents an Album and it's list of the names for each song
           :param name: Album's name
           :type name: str
        """
        self.name = name
        self.songs = []

    def set_songs(self, songs):
        """
        :param songs: list of names for songs in this album
        :type songs: list
        """
        self.songs = songs
