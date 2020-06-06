"""
This file is meant to merge the texts of the profiles with all their contents,
since it's extramely ineffective to read small files from a drive.
The resulting files are meant for analization that doesn't require the pictures
such as word frequency analisis.
"""

import os
from path import Path

def extract_profile(path):
    n_pictures = max(0, len(os.listdir(path))-1)
    text = str(n_pictures)+"\n"
    with open(path+"/info.txt", "r", encoding='utf-8', errors='replace') as info:
        text += info.read().lower().replace(";", " ")
    return text

def merge_bios(directories, filename):
    finished = 0
    for url in directories:
        profiles = os.listdir(url)
        with open(filename, "a", encoding='utf-8', errors='replace') as biofile:
            for i, p in enumerate(profiles):
                path = url+"/"+p
                try:
                    bio = extract_profile(path)
                    biofile.write(bio+";\n")
                except FileNotFoundError:
                    pass
                print(str(i)+"/"+str(len(profiles))+" profiles merged", end="\r")
        
        finished += len(profiles)
        print(str(finished)+" profiles merged         ")

men = Path().men
women = Path().women
merge_bios(women, Path().out+"/women_merged_bios.txt")
merge_bios(men, Path().out+"/men_merged_bios.txt")
