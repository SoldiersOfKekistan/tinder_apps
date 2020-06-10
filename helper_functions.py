"""
Program for functions used by multiple programs.
Less redundancy in code results in more flexibility and less mistakes.
"""
from path import Path

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

# converts dict to sorted array
def dict_to_sorted_array(d):
    out = []
    for key in d.keys():
        out.append((key, d[key]))
    out.sort(key = lambda x: x[1], reverse=True)
    return out
