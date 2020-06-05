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
    name = path.split("/")[-1].split("_")[0]
    text = name+"\n"+str(n_pictures)+"\n"
    try:
        with open(path+"/info.txt", "r") as info:
            text += info.read().lower().replace(";", " ")
    except FileNotFoundError:
        pass
    return text

def merge_bios(directories, filename):
    finished = 0
    for url in directories:
        profiles = os.listdir(url)
        with open(filename, "a") as biofile:
            for i, p in enumerate(profiles):
                path = url+"/"+p
                bio = extract_profile(path)
                biofile.write(bio+";\n")
                print(str(i)+"/"+str(len(profiles))+" profiles merged", end="\r")
        
        finished += len(profiles)
        print(str(finished)+" profiles merged         ")

men = Path().men
women = Path().women
merge_bios(women, "women_merged_bios.txt")
merge_bios(men, "men_merged_bios.txt")
