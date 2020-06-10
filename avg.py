"""
Program to calculate average and median.
Uses merged bio files, so if you don't have them already, run bio_merger.py.
"""
from path import Path
from helper_functions import extract_data

def read(file):
    list_ages = [0 for i in range(120)]
    list_pictures = [0 for i in range(100)]
    list_lengths = [0 for i in range(10000)]
    try:
        with open(file, encoding='utf-8', errors='replace') as bios_file:
            profile = ""
            for line in bios_file:
                if line == ";\n":
                    bio, age, n_pictures = self.extract_data(profile)
                    if 18<=age<120:
                        list_ages[age] += 1
                    list_pictures[n_pictures] += 1
                    list_lengths[len(bio)] += 1
                    profile = ""
                else:
                    profile += line
    return list_ages, list_pictures, list_lengths
    except FileNotFoundError:
        print("merged bios not found, run bio_merger.py then try again")
        quit()

"""
Calculates the average and median of the list given.
Since it's a big data problem, if there are two elements in the middle the
median is the first, not their average.
The i-th index of the list must contain the number of records with value i
"""
def get_stats(_list):
    n = sum(_list)
    mid = n//2
    total = 0
    past = 0
    median = 0
    for index, value in enumerate(_list):
        total += index*value
        if past <= mid < past+value and median == 0:
            median = index
        else:
            past += value
    return round(total/n, 2), median

men_ages, men_pictures, men_lengths = read(Path().out+"/men_merged_bios.txt", list_ages, list_pictures, list_lengths)
women_ages, women_pictures, women_lengths = read(Path().out+"/women_merged_bios.txt", list_ages, list_pictures, list_lengths)
merged_ages = [men_ages[i]+women_ages[i] for i in range(len(men_ages))]
merged_pictures = [men_pictures[i]+women_pictures[i] for i in range(len(men_pictures))]
merged_lengths = [men_lengths[i]+women_lengths[i] for i in range(len(men_lengths))]

avg_age, median_age = get_stats(merged_ages)
avg_pictures, median_pictures = get_stats(merged_pictures)
avg_lengths, median_lengths = get_stats(merged_lengths)

men_avg_age, men_median_age = get_stats(men_ages)
men_avg_pictures, men_median_pictures = get_stats(men_pictures)
men_avg_lengths, men_median_lengths = get_stats(men_lengths)

women_avg_age, women_median_age = get_stats(women_ages)
women_avg_pictures, women_median_pictures = get_stats(women_pictures)
women_avg_lengths, women_median_lengths = get_stats(women_lengths)

print("                     Average\tMen\tWomen\tMedian\tMen\tWomen")
print("               Age"+str(avg_age)+"\t"str(men_avg_age)+"\t"+str(women_avg_age)+"\t"+str(median_age)+"\t"+str(men_median_age)+"\t"+str(women_median_age))
print("Number of pictures"+str(avg_pictures)+"\t"str(men_avg_pictures)+"\t"+str(women_avg_pictures)+"\t"+str(median_pictures)+"\t"+str(men_median_pictures)+"\t"+str(women_median_pictures))
print("Bio length (chars)"+str(avg_lengths)+"\t"str(men_avg_lengths)+"\t"+str(women_avg_lengths)+"\t"+str(median_lengths)+"\t"+str(men_median_lengths)+"\t"+str(women_median_lengths))
