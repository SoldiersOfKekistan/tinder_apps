"""
Program for functions used by multiple programs.
Less redundancy in code results in more flexibility and less mistakes.
"""
from path import Path
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet

# extracts the data from the plaintext profile
def extract_data(text):
    lines = text.split("\n")
    n_pictures = int(lines[0])
    bio = ""
    age = 0
    for line in lines[1:]:
        if not line.startswith("birth date: "):
            bio += line + "\n"
        else:
            try:
                year = int(line.split("birth date: ")[1][:4])
                age = 2020-year
            except ValueError:
                print(line)
            break
    bio = bio[len("bio: "):-1]
    return bio, age, n_pictures

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def lemmatize_sentence(sentence, lemmatizer):
    res = []
    for word, pos in pos_tag(word_tokenize(sentence)):
        wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
        res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
    return res

# converts dict to sorted array
def dict_to_sorted_array(d):
    out = []
    for key in d.keys():
        out.append((key, d[key]))
    out.sort(key = lambda x: x[1], reverse=True)
    return out
