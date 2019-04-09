import csv
import json
import re
import spacy


class SentimentAnalyzer:

    def __init__(self, lexicon_file, categories_file):
        """
        calculates overall color, emotion, sentiment, gloom for a song
        :param lexicon_file: name of your lexicon file
        :type lexicon_file: str
        :param categories_file: name of your categories file
        :type categories_file: str
        """
        self.lexicon_file = lexicon_file
        self.categories_file = categories_file
        self.lexRow = None
        self.words = None
        self.categories = None
        self.categories_headers = None
        self.read_lexicon()
        self.read_categories()

    def read_lexicon(self):
        """
        reads your lexicon file and saves it into a list of words
        """
        with open(self.lexicon_file) as f:
            rows = csv.reader(f, delimiter=',')
            headers = next(rows, None)
            for row in rows:
                entry = {}
                for i, h in enumerate(headers):
                    entry[h] = row[i]
                self.lexRow.append(entry)
                self.words = [v['word'] for v in self.lexRow]

    def read_categories(self):
        """
        reads your categories file and saves it into a dict
        """
        with open(self.categories_file) as f:
            self.categories = json.load(f)
            self.categories_headers = self.categories.keys()

    @staticmethod
    def clean_lyrics(lyrics):
        """
        cleans your lyrics and boils it down to some words that are ready for analysis
        :param lyrics: lyrics of the songs as it is
        :type lyrics: str
        :return: lyrics after its cleaned
        """
        remove_seq = re.compile('\[(.*?)\]')
        remove_pun = re.compile('[^\w\s]')
        remove_new_lines = re.compile('\n+')
        lyrics = remove_seq.sub('', lyrics)
        lyrics = remove_pun.sub('', lyrics)
        lyrics = remove_new_lines.sub(' ', lyrics)
        return lyrics

    @staticmethod
    def get_lyrical_density(lyrics):
        """
        calculates the measure of the number of meaningful words as a proportion of the total number of words
        :param lyrics: lyrics of the song to be analysed
        :type lyrics: str
        :return: list of meaningful words and calculated lyrical density
        """
        doc = spacy_nlp(lyrics)
        tokens = [token.text for token in doc if not token.is_stop]
        if not tokens:
            lexD = 0
        else:
            lexD = float((len(tokens) / len(doc)))
        return tokens, lexD

    @staticmethod
    def do_tokens(words):
        """
        takes list of rows that carries information about each word in a single lyrics and calculates
        it's overall sentiment
        :param words: list of rows
        :type words: list of int
        :return: overall sentiment of a lyrics
        """
        emotion_count = [0] * 8
        sen_count = [0] * 2
        color_count = [0] * 11
        words_with_emotion = 0
        words_with_sen = 0
        share_of_emotion = 0
        share_of_sen = 0

        for w in words:
            if w[0] != -1:
                words_with_emotion += 1
                emotion_count[w[0]] += 1
            if w[1] != -1:
                words_with_sen += 1
                sen_count[w[1]] += 1
            if w[2] != -1:
                color_count[w[2]] += 1

        max_emottion = emotion_count.index(max(emotion_count))
        max_sen = sen_count.index(max(sen_count))
        max_col = color_count.index(max(color_count))

        if words_with_emotion != 0:
            share_of_emotion = emotion_count[max_emottion] / words_with_emotion
        if words_with_sen != 0:
            share_of_sen = sen_count[max_sen] / words_with_sen

        overall_share = (share_of_emotion + share_of_sen) / 2

        return max_emottion, max_sen, max_col, overall_share

    def do_token(self, word):
        """
        takes a word and get it's matching row from your lexicon if found
        :param word: a word to look for
        :type word: str
        :return: a list of information about a single word from the lexicon [ emotion , color , sentiment ]
        """
        match = -1
        for i, w in enumerate(self.words):
            if w == word:
                match = i
                break

        if match != -1:
            entry = self.lexRow[match]
            row = []
            for c in self.categories_headers:
                if entry[c]:
                    row.append(self.categories[c].index(entry[c]))
                else:
                    row.append(-1)
            return row

    def get_sentiment(self, tokens):
        """
        calculates sentimental fields about easch lyrics
        :param tokens: list of meangful words from the lyrics
        :return: list of calculated fields for each song overall : emotion, sentiment, color, share
        """
        numbers = []
        for token in tokens:
            data = self.do_token(token)
            if data is not None:
                numbers.append(data)
            if len(numbers) == 0:
                return 0, 0, 0, 0
            if len(numbers) != 0:
                return self.do_tokens(numbers)

    def analyze(self, song):
        """
        calculaltes final gloom of a song
        :param song: song to ba analysed
        :type song: Song object
        :return: overall color, emotion, sentiment, gloom for a song
        """

        valence = song.valence
        lyrics = self.clean_lyrics(song.lyrics)
        tokens, lexD = self.get_lyrical_density(lyrics)

        lexD = round(float(lexD), 4)

        song.set_lexD(lexD)

        emotion = None
        color = None
        sentiment = None

        if tokens:
            emotion_idx, sentiment_idx, color_idx, share = self.get_sentiment(tokens)

            emotion = self.categories['emotion'][emotion_idx]
            sentiment = self.categories['sentiment'][sentiment_idx]
            color = self.categories['color'][color_idx]

            if sentiment == 'negative':
                gloom = (1 - valence + share * (1 + lexD)) / 2
            else:
                gloom = (valence + share * (1 + lexD)) / 2
        else:
            gloom = valence
        gloom = round(float(gloom), 4)

        return color, emotion, sentiment, gloom
