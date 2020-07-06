"""
Counts words from filters in filters.txt.
"""

from path import Path
from helper_functions import dict_to_sorted_array

class Filter:
    def __init__(self, category):
        self.category = category
        self.words = []
    def add_word(self, word):
        self.words.append(word)
    def filter(self, words):
        filtered = {}
        for key in words.keys():
            if key in self.words:
                filtered[key] = words[key]
        return filtered

def read_filters():
    all_filters = []
    with open("filters.txt") as filter_file:
        current = Filter("Unnamed filter")
        for line in filter_file:
            if line[0] == "#":
                continue
            if line.startswith("category:"):
                category = line[len("category:"):]
                current = Filter(category)
                all_filters.append(current)                
            else:
                word = line[:-1]
                current.add_word(word)
    return all_filters

def read_words(file):
    words = {}
    try:
        with open(file, encoding='utf-8', errors='replace') as words_file:
            for line in words_file:
                data = line.split(":")
                try:
                    words[data[0]] = int(data[-1][:-1])
                except ValueError:
                    print(data)
                    quit()
        return words
    except FileNotFoundError:
        print("words not found, run wc.py then try again")
        quit()

def write_filtered(file, filters, words):
    with open(file, "w") as target:
        for f in filters:
            target.write("category:"+f.category)
            filtered = f.filter(words)
            array = dict_to_sorted_array(filtered)
            for w in array:
                target.write(w[0]+":"+str(w[1])+"\n")

filters = read_filters()

men_words = read_words(Path().out+"/men_words.txt")
women_words = read_words(Path().out+"/women_words.txt")
merged_words = read_words(Path().out+"/merged_words.txt")

write_filtered(Path().out+"/filtered_merged_words.txt", filters, merged_words)
write_filtered(Path().out+"/filtered_men_words.txt", filters, men_words)
write_filtered(Path().out+"/filtered_women_words.txt", filters, women_words)
print("done.")
