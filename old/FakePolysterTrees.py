# ~Authenticity doesn't just mean you're not filtering what you're saying,
# it's about being able to know and access the best parts of yourself and bring them forward~


import csv
import pandas as pd
import re

REMOVE_SEQ = re.compile('\[(.*?)\]')
REMOVE_PUN = re.compile('[^\w\s]')
REPLACE_NEW_LINES = re.compile('\n{1,10}')


def read_lyrics_from_csv_file(csv_file):
    lyrics = []
    with open(csv_file) as myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            lyrics.append(row['Lyrics'].lower())
    return lyrics


def filter_lyrics(lyrics):
    lyrics = REMOVE_SEQ.sub('', lyrics)
    lyrics = REMOVE_PUN.sub('', lyrics)
    lyrics = REPLACE_NEW_LINES.sub(' ', lyrics)
    return lyrics


def save_lyrics(clean_lyrics, csv_file):
    df = pd.read_csv(csv_file)
    df.Lyrics = clean_lyrics
    df.to_csv(csv_file, index=False)


csv_file = 'Radiohead_Discography.csv'
all_Lyrics = read_lyrics_from_csv_file(csv_file)
for idx, item in enumerate(all_Lyrics):
    all_Lyrics[idx] = filter_lyrics(all_Lyrics[idx])
save_lyrics(all_Lyrics, csv_file)
