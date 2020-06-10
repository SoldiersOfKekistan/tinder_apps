"""
Counts words in bios.
nltk seems to be flawed as somethines it strips more of the words needed, but
it's consistent and still easy to guess what is what.
Uses merged bio files, so if you don't have them already, run bio_merger.py.
"""

from nltk.stem.snowball import SnowballStemmer
from path import Path
from helper_functions import extract_data

def replace_separators(text):
    separators = ['.', ',', ';', ':']
    for sep in separators:
        text = text.replace(sep, ' ')

def get_words(file):
    words = {}
    stemmer = SnowballStemmer("english")

    try:
        with open(file, encoding='utf-8', errors='replace') as bios_file:
            profile = ""
            for line in bios_file:
                if line == ";\n":
                    bio, age, n_pictures = extract_data(profile)
                    replace_separators(bio)
                    for word in bio.split():
                        root = stemmer.stem(word)
                        if root in words:
                            words[root] += 1
                        else:
                            words[root] = 1
                    profile = ""
                else:
                    profile += line
        return words
    except FileNotFoundError:
        print("merged bios not found, run bio_merger.py then try again")
        quit()

def write_list(file, _list):
    with open(file, "a", encoding='utf-8') as out_file:
        for i in _list:
            out_file.write(i[0]+":"+str(i[1])+"\n")
        
def merge_dicts(d1, d2):
    out = {key: value for key, value in d1.items()}
    for k in d2.keys():
        if k in out:
            out[k] += d2[k]
        else:
            out[k] = d2[k]
    return out

def sort_dict(d):
    out = []
    for key in d.keys():
        out.append((key, d[key]))
    out.sort(key = lambda x: x[1], reverse=True)
    return out

men = get_words(Path().out+"/men_merged_bios.txt")
women = get_words(Path().out+"/women_merged_bios.txt")
merged = merge_dicts(men, women)

men_list = sort_dict(men)
women_list = sort_dict(women)
merged_list = sort_dict(merged)

write_list(Path().out+"/men_words.txt", men_list)
write_list(Path().out+"/women_words.txt", women_list)
write_list(Path().out+"/merged_words.txt", merged_list)
print("done.")
