"""
Counts words from filters in filters.txt
"""

from path import Path

class Filter:
    def __init__(self, category, words):
        self.category = category
        self.words = words
    def member(self, word):
        return False
    
def read_filters():
    return 0

def read_words(file):
    words = {}
    try:
        with open(file, encoding='utf-8', errors='replace') as words_file:
            for line in words_file:
                data = line.split(":")
                words[data[0]] = int(data[1])
        return words
    except FileNotFoundError:
        print("words not found, run wc.py then try again")
        quit()

filters = read_filters()

men_words = read_words(Path().out+"/men_words")
women_words = read_words(Path().out+"/women_words")
merged_words = read_words(Path().out+"/merged_words")
