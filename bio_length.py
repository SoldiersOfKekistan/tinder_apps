"""
A program to plot statistics about bio length distributions.
Uses merged bio files, so if you don't have them already, run bio_merger.py.
"""
import os
import matplotlib.pyplot as plt
from path import Path

def avg(array):
    n = sum(array)
    total = 0
    for i, v in enumerate(array):
        total += i*v
    return round(total/n, 2)
def percent(array):
    n = sum(array)
    for i in range(len(array)):
        array[i] = 100*array[i]/n

def get_bio(text):
    return text.split("bio: ")[1].split("\nbirth date: ")[0].replace("\n", " ")

def get_stats(filename, max_w=1000, max_c=7000):
    words = [0 for i in range(max_w)]
    chars = [0 for i in range(max_c)]
    try:
        with open(filename, "r", encoding="utf-8", errors='replace') as file:
            profile = ""
            for line in file:
                if line == ";\n":
                    try:
                        bio = get_bio(profile)
                    except:
                        pass
                    if len(bio.split()) < max_w:
                        words[len(bio.split())] += 1
                    if len(bio) < max_c:
                        chars[len(bio)] += 1
                    profile = ""
                else:
                    profile += line
        return words, chars
    except FileNotFoundError:
        print("merged bios not found, run bio_merger.py then try again")
        quit()

def print_results(men_w, men_c, women_w, women_c):
    sum_w = [men_w[i]+women_w[i] for i in range(len(men_w))]
    sum_c = [men_c[i]+women_c[i] for i in range(len(men_c))]

    percent(men_w)
    percent(women_w)
    percent(men_c)
    percent(women_c)

    plt.subplot(2, 2, 1)
    plt.plot(women_w)
    plt.plot(men_w)
    plt.xlabel('Words')
    plt.ylabel('In percent excluding empty bios')
    plt.grid()
    
    plt.subplot(2, 2, 2)
    plt.plot(women_c)
    plt.plot(men_c)
    plt.xlabel('Charachters')
    plt.ylabel('In percent excluding empty bios')
    plt.grid()

    plt.subplot(2, 2, 3)
    plt.plot(sum_w)
    plt.xlabel('Word count summed')
    plt.grid()
    
    plt.subplot(2, 2, 4)
    plt.plot(sum_c)
    plt.xlabel('Charachter count summed')
    plt.grid()

    plt.subplots_adjust(wspace=0.3, hspace=0.5)
    plt.show()

men_w, men_c = get_stats(Path().out+"/men_merged_bios.txt", max_w=110, max_c=550)
women_w, women_c = get_stats(Path().out+"/women_merged_bios.txt", max_w=110, max_c=550)

print("Averages for men:\n\twords: "+str(avg(men_w))+"\n\tcharachters: "+str(avg(men_c)))
print("Averages for women:\n\twords: "+str(avg(women_w))+"\n\tcharachters: "+str(avg(women_c)))

"""
Dropping empty bios as there are too many of them which make
all the others seem as zero.
"""
men_w[0], men_c[0], women_w[0], women_c[0] = men_w[1], men_c[1], women_w[1], women_c[1]
print_results(men_w, men_c, women_w, women_c)
