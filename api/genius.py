import lyricsgenius as genius
import re


class Genius:
    def __init__(self, token):
        """
        wrapper class for Genius API
        :param token:  your token from Genius API
        """
        self.apiG = genius.Genius(token)

    @staticmethod
    def clean_string(self, str):
        """
        regex applied for a better search results
        :param str: name of the song
        :return: name of the song after the regex is applied
        """
        return re.sub(r"(?<=[^a-zA-Z0-9]) ", "", str)

    def get_lyrics_for_track(self, track_name, artist_name):
        """
        gets lyrics for a track
        :param track_name: name of the track we want to get the lyrics for
        :type track_name: str
        :param artist_name: name of the artist of the song
        :type artist_name: str
        :return: string represnting the lyrics of a song
        """
        song = self.apiG.search_song(
            track_name,
            artist_name
        ) or self.apiG.search_song(
            self.clean_string(track_name),
            artist_name
        )
        if song:
            return song.lyrics
