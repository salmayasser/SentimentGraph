#~Sometimes, reality is the illusion, and the truth only visible where our eyes can’t see.

import csv
import spacy
import json
import pandas as pd
import sys, csv ,operator
from operator import itemgetter
spacy_nlp = spacy.load('en_core_web_sm')

LEX_FILE = "lexicons.csv"
CAT_FILE = "catCol/cat.json"
csv_file = 'Radiohead_Discography.csv'
OUTPUT_FILE = 'Quantified_Discography.csv'


def save_to_output(file):
    with open(file, 'w') as myFile:
        myFields = ['#', 'Album', 'Track', 'Title', 'lexD', 'Emotion', 'Sentiment', 'Valence', 'Color', 'Gloom']
        writer = csv.DictWriter(myFile, fieldnames=myFields)
        writer.writerow(
            {
                '#': '#',
                'Album': 'Album',
                'Track': 'Track',
                'Title': 'Title',
                'lexD':  'lexD',
                'Emotion': 'Emotion',
                'Sentiment': 'Sentiment',
                'Valence': 'Valence',
                'Color': 'Color',
                'Gloom': 'Gloom'
            }
        )
    df = pd.read_csv(file)
    df['#'] = all_albumno
    df.Album = all_album
    df.Track = all_trackno
    df.Title = all_names
    df.lexD = all_lexD
    df.Emotion = all_emotion
    df.Sentiment = all_sentemint
    df.Valence = all_V
    df.Color = all_color
    df.Gloom = all_gloom
    df.to_csv(file, index=False)


def read_from_csv_file(file):
    lyrics = []
    V = []
    names=[]
    album = []
    trackno = []
    albumno = []
    with open(file) as myFile:
        reader = csv.DictReader(myFile)
        for row in reader:
            lyrics.append(row['Lyrics'].lower())
            V.append(row['Valence'])
            names.append(row['Title'])
            album.append(row['Album'])
            trackno.append(row['Track'])
            albumno.append(row['#'])
    return lyrics, V, names, albumno, album, trackno


def read_lex(file):
    words = []
    lexRow = []
    with open(file) as f:
        rows = csv.reader(f, delimiter=',')
        headers = next(rows, None)
        for row in rows:
            entry = {}
            for i, h in enumerate(headers):
                entry[h] = row[i]
            lexRow.append(entry)
        words = [v['word'] for v in lexRow]
    return words, lexRow


def read_cat(file):
    categories = {}
    category_headers = []
    with open(file) as f:
        categories = json.load(f)
        category_headers = categories.keys()
    return categories, category_headers


def get_lyrical_density(lyrics):

    doc = spacy_nlp(lyrics)
    tokens = [token.text for token in doc if not token.is_stop]
    newdoc = ' '.join(tokens)
    #newdoc = spacy_nlp(newdoc)
    #x = [token.lemma_ for token in newdoc] # list comprehension
    #print( len(lyrics), len(tokens),len(x))
    if not tokens:
        lexD = 0
    else:
        lexD = float((len(tokens)/len(doc)))
    return len(lyrics), len(tokens), tokens, lexD



def do_tokens(words):
    emotion_count = [0]*8
    sen_count = [0]*2
    color_count = [0]*11
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


def do_token(word):
    global lexRow
    global categories
    global category_headers
    global words

    match = -1
    for i, w in enumerate(words):
        if w == word:
            match = i
            break


    if match != -1:
        entry = lexRow[match]
        row = []
        for c in category_headers:
            if entry[c]:
                row.append(categories[c].index(entry[c]))
            else:
                row.append(-1)
        return row


def get_sentiment(tokens):
    numbers = []
    data = []
    for token in tokens:
         data = do_token(token)
         if data is not None:
            numbers.append(data)
    if len(numbers) == 0:
        return 0, 0, 0, 0
    if len(numbers) != 0:
        return do_tokens(numbers)


def neg(text):
    negation = False
    delims = "?.,!:;"
    result=""
    words = text.split()
    for word in words:
        stripped = word.strip(delims).lower()
        negated = "not_" + stripped if negation else stripped
        result+=negated
        result+=" "

        if any(neg in word for neg in ["not", "n't", "no", "dont", "wont", "doesnt"]):
            negation = not negation

        if any(c in word for c in delims):
            negation = False

    return result




res = read_from_csv_file(csv_file)
all_Lyrics = res[0]
all_V = res[1]
all_names = res[2]
all_albumno = res[3]
all_album = res[4]
all_trackno = res[5]
all_emotion = []
all_sentemint = []
all_lexD = []
all_gloom = []
all_color = []

res = read_lex(LEX_FILE)
words = res[0]
lexRow = res[1]

res = read_cat(CAT_FILE)
categories = res[0]
category_headers = res[1]


for idx in range(len(all_Lyrics)):
    valence = float(all_V[idx])
    #lyrics = neg(all_Lyrics[idx]);

    res = get_lyrical_density(all_Lyrics[idx])

    lenLyrics = res[0]
    lenTokens = res[1]
    tokens = res[2]
    lexD = round(float(res[3]), 4)
    all_lexD.append(lexD)
    #print(tokens)
    if tokens:
        res = get_sentiment(tokens)
        emotion = categories['emotion'][res[0]]
        sentiment = categories['sentiment'][res[1]]
        color = categories['color'][res[2]]
        share = res[3]
        if sentiment == 'negative':
            gloom = (1 - valence + share * (1 + lexD)) / 2
        else:
            gloom = (valence + share * (1 + lexD)) / 2
    else:
        gloom = valence
    gloom = round(float(gloom), 4)

    all_color.append(color)
    all_emotion.append(emotion)
    all_sentemint.append(sentiment)
    all_gloom.append(gloom)

save_to_output(OUTPUT_FILE)