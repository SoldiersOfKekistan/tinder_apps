"""
Program to calculate average and median.
"""
from path import Path
from helper_functions import extract_data

def read(file, list_ages, list_pictures, list_lengths):    
    try:
        with open(file, encoding='utf-8', errors='replace') as bios_file:
            profile = ""
            for line in bios_file:
                if line == ";\n":
                    length, age, n_pictures = self.extract_data(profile)
                    if 18<=age<120:
                        list_ages[age] += 1
                    list_pictures[n_pictures] += 1
                    list_lengths[length] += 1
                    profile = ""
                else:
                    profile += line
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
    return total/n, median

list_ages = [0 for i in range(120)]
list_pictures = [0 for i in range(100)]
list_lengths = [0 for i in range(10000)]
#read(Path().out+"/men_merged_bios.txt", list_ages, list_pictures, list_lengths)
#read(Path().out+"/women_merged_bios.txt", list_ages, list_pictures, list_lengths)
avg_age, median_age = get_stats(list_ages)
avg_pictures, median_pictures = get_stats(list_ages)
avg_lengths, median_lengths = get_stats(list_ages)

print("Average\tMedian")
print(str(avg_age)+"\t\t", str(median_age))
print(str(avg_pictures)+"\t\t", str(median_pictures))
print(str(avg_lengths)+"\t\t", str(median_lengths))
