import csv
import json
import sys


OUTPUT_FILE = "lexicons.csv"
CAT_FILE = "catCol/cat.json"


words = []
categories = {}
with open(CAT_FILE) as f:
    categories = json.load(f)
category_headers = categories.keys()
headers = ['word']
headers.extend(category_headers)


# Adds new word or extends exisiting word
def add_word(_w):
    global words
    global headers

    matches = [w for w in words if w['word'] == _w['word']]
    if len(matches) > 0:
        match = matches[0]
        for header in match:
            if not match[header] and header in _w and _w[header]:
                words[match['index']][header] = _w[header]
    else:
        word = _w
        word['index'] = len(words)
        for h in headers:
            if h not in word:
                word[h] = ""
        words.append(word)


def read_lex(file):
    with open(file) as f:
        row = csv.reader(f, delimiter='\t')
        for wordL, categoryL, associationL in row:
            if int(associationL) != 1:
                continue
            word = {}
            word['word'] = wordL
            if categoryL in categories['emotion']:
                word['emotion'] = categoryL
                if categoryL == 'anger' or categoryL == 'fear' or categoryL =='sadness'or categoryL =='disgust':
                    word['sentiment'] = "negative"
                elif categoryL == "surprise" or categoryL == "joy" :
                    word['sentiment']="positive"
            elif categoryL in categories['sentiment']:
                 word['sentiment'] = categoryL
            add_word(word)


def read_colors(file):
    with open(file) as f:
        rows = csv.reader(f, delimiter='\t')
        for _word_sense, _color, _votes, _votes_total in rows:
            word = {}
            word['word'] = _word_sense.split("--")[0]
            word['color'] = _color.split("=")[1]
            word['source'] = 'colour'
            votes = _votes.split("=")[1]
            votes_total = _votes_total.split("=")[1]
            if votes.isdigit() and votes_total.isdigit() and word['color'] in categories['color'] and float(
                    votes_total) and float(votes) / float(votes_total) > 0.5:
                add_word(word)


def save_to_output_file(file):
    with open(file, 'w', newline='') as f:
        cw = csv.writer(f)
        cw.writerow(headers)
        for w in words:
            row = []
            for h in headers:
                row.append(w[h])
            cw.writerow(row)




EMOLEX_FILE = "myLex/NRC-emotion-lexicon-wordlevel-alphabetized-v0.92.txt"
COLOR_FILE = "myLex/NRC-Colour-Lexicon-v0.92NRC-color-lexicon-senselevel-v0.92.txt"
read_lex(EMOLEX_FILE)
read_colors(COLOR_FILE)
save_to_output_file(OUTPUT_FILE)
