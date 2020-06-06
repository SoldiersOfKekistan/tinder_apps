"""
Interactive histograms for complex analisation of data.
Click on a column to deselect every record in the category. Click again to make it selected again.
Colors and their meanings:
    Blue   - All records shown. Category is deselected.
    Red    - All records shown. Category is selected.
    Orange - Proportion of selected records in the category.
"""

from tkinter import *
from path import Path
import random
"""
Widget to display an interactive histogram. View in the Document-View architecture.
"""
class Histogram(Frame):
    def __init__(self, parent, labels, width, height, name, document, row):
        Frame.__init__(self, parent)
        doc.views.append(self)

        # attributes
        self.parent = parent
        self.labels = labels
        self.width = width
        self.height = height
        self.name = name
        self.document = document
        self.row = row
        self.values = [0 for i in range(len(labels))]
        self.selected_values = [0 for i in range(len(labels))]
        self.selected = [True for i in range(len(labels))]
        self.canvas = Canvas(self, width=width, height=height)

        # initialising attributes
        for r in range(len(self.document.records)):
            self.values[self.document.records[r][self.row]] += 1
            self.selected_values[self.document.records[r][self.row]] += 1

        # initialising graphic attributes
        self.canvas.pack()
        self.show()
        self.canvas.bind("<Button-1>", self.clicked)

    # tells if record is selected by this view or not
    def selector(self, record):
        return self.selected[record[self.row]]

    def show(self):
        if len(self.values) != len(self.labels):
            return

        self.canvas.delete(ALL)
        self.canvas.create_text(self.width//2, 10, text=self.name, font=("Times", "14", "bold"))
        self.canvas.create_line(5, self.height-25, self.width-5, self.height-25, arrow=LAST)
        self.canvas.create_line(5, self.height-25, 5, 5, arrow=LAST)
        for i in range(len(self.labels)):
            self.canvas.create_line( 10+int((self.width-25)*i/len(self.labels)), self.height-20, 10+int((self.width-25)*i/len(self.labels)), self.height-30 )
            self.canvas.create_text( 10+int( (self.width-25)*( (i+0.5)/len(self.labels) ) ), self.height-8, text=str(self.labels[i]), font=("Times", "10", "bold") )

        max_v = max(self.values)
        if max_v <= 0:
            max_v = 1
        for v in range(len(self.values)):
            self.canvas.create_rectangle(int((self.width-25)*v/len(self.labels))+10,
                                            self.height-25,
                                            int((self.width-25)*(v+1)/len(self.labels))+10,
                                            self.height-25-self.values[v]/max_v*(self.height-50),
                                            fill = "red" if self.selected[v] else "light blue"
                                         )
            self.canvas.create_rectangle(int((self.width-25)*v/len(self.labels))+10,
                                            self.height-25,
                                            int((self.width-25)*(v+1)/len(self.labels))+10,
                                            self.height-25-self.selected_values[v]/max_v*(self.height-50),
                                            fill = "orange"
                                         )
            self.canvas.create_text(int((self.width-25)*(v+0.5)/len(self.labels))+10,
                                    self.height-30-self.values[v]/max_v*(self.height-50),
                                    text=str(self.values[v]),
                                    font=("Times", "10", "bold")
                                    )
            self.canvas.create_text(int((self.width-25)*(v+0.5)/len(self.labels))+10,
                                    self.height-30-self.selected_values[v]/max_v*(self.height-50)+10,
                                    text=str(self.selected_values[v])+"("+ str(0 if self.values[v]==0 else round(self.selected_values[v]/self.values[v]*100, 2)) +"%)",
                                    font=("Times", "10")
                                    )

    def clicked(self, event):
        max_v = max(self.values)
        if max_v <= 0:
            max_v = 1
        for v in range(len(self.values)):
            left = int((self.width-25)*v/len(self.labels))+10
            right = int((self.width-25)*(v+1)/len(self.labels))+10
            bottom = self.height-15
            top = self.height-15-self.values[v]/max_v*(self.height-40)+5
            if left<event.x<right and top<event.y<bottom:
                if self.selected[v] == True:
                    self.selected[v] = False
                    self.document.reduce_selection(self)
                else:
                    self.selected[v] = True
                    self.document.expand_selection()
                return

    # updates numbers shown
    def update(self):
        self.selected_values = [0 for i in range(len(self.values))]
        for r in range(len(self.document.records)):
            if self.document.selected[r]:
                self.selected_values[self.document.records[r][self.row]] += 1
        self.show()

"""
Document class in the Document-View architecture.
Records must be a touple containing numbers with each number x meaning value is in the x-th category.
"""
class Document:
    def __init__(self, records):
        self.records = records
        self.n = len(self.records)
        self.selected = [True for i in range(len(self.records))]
        self.views = []
    # reduces the selected records with a criterion given by @param view
    def reduce_selection(self, view):
        for r in range(self.n):
            if self.selected[r]:
                self.selected[r] = view.selector(self.records[r])
        for v in self.views:
            v.update()
    # recalculates deselected records after a criterion was deleted
    def expand_selection(self):
        self.selected = [True for i in range(len(self.records))]
        for r in range(self.n):
            if self.selected[r] == True:
                for v in self.views:
                    if v.selector(self.records[r]) == False:
                        self.selected[r] = False
                        break
        for v in self.views:
            v.update()

"""
Class to read data into Document.
"""
class Reader:
    def __init__(self, i_length, i_age, i_pictures):
        self.i_length = i_length
        self.i_age = i_age
        self.i_pictures = i_pictures
    # calculates which interval the value belongs to
    def get_interval(self, value, intervals):
        for i in range(len(intervals)):
            if intervals[i][0] <= value < intervals[i][1]:
                return i
        raise AttributeError("value "+str(value)+" does not belong to any intervals in:\n"+str(intervals))
    # creates record from given values
    def make_record(self, length, gender, age, n_pictures):
        l = self.get_interval(length, self.i_length)
        a = self.get_interval(age, self.i_age)
        p = self.get_interval(n_pictures, self.i_pictures)
        return (l, gender, a, p)
    # extract values from plaintext profile
    def extract_data(self, text):
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
        return len(bio), age, n_pictures
    # reads all the data
    def read(self):
        out = []
        try:
            wrong_records = 0
            with open(Path().out+"/men_merged_bios.txt", encoding='utf-8', errors='replace') as bios_file:
                profile = ""
                for line in bios_file:
                    if line == ";\n":
                        length, age, n_pictures = self.extract_data(profile)
                        if 18<=age<120:
                            out.append(self.make_record(length, 0, age, n_pictures))
                        else:
                            wrong_records += 1
                        profile = ""
                        #quit()
                    else:
                        profile += line
            with open(Path().out+"/women_merged_bios.txt", encoding='utf-8', errors='replace') as bios_file:
                profile = ""
                for line in bios_file:
                    if line == ";\n":
                        length, age, n_pictures = self.extract_data(profile)
                        if 18<=age<120:
                            out.append(self.make_record(length, 1, age, n_pictures))
                        else:
                            wrong_records += 1
                        profile = ""
                        #quit()
                    else:
                        profile += line
            print('wrong records: ', wrong_records)
        except FileNotFoundError:
            print("merged bios not found, run bio_merger.py then try again")
            quit()
        for i in range(1000):
            gender = random.randrange(2)
            age = random.randrange(18, 65)
            length = random.randrange(501)
            n_pics = random.randrange(7)
            out.append(self.make_record(length, gender, age, n_pics))
        return out

i_length = [(0, 1), (1, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 500), (500, 10000)]
n_length = ["0", "1-9", "10-19", "20-49", "50-99", "100-199", "200-499", "500+"]
i_age = [(18, 23), (23, 28), (28, 33), (33, 38), (38, 43), (43, 48), (48, 120)]
n_age = ["18-22", "23-27", "28-32", "33-37", "38-42", "43-47", "48+"]
i_pictures = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 100)]
n_pictures = [str(i) for i in range(9)]+["9+"]
reader = Reader(i_length, i_age, i_pictures)
records = reader.read()
doc = Document(records)

win = Tk()
win.title("Interactive histograms")
title = Label(win, text="Interactive histograms\n", font=("Times", 30, "bold"))
title.grid(row=0, column=0, columnspan=2)
hist = Histogram(win, n_length, 500, 300, "Character count", doc, 0)
hist.grid(row=1, column=0)
hist2 = Histogram(win, ["Men", "Women"], 500, 300, "Gender", doc, 1)
hist2.grid(row=1, column=1)
hist3 = Histogram(win, n_age, 500, 300, "Age", doc, 2)
hist3.grid(row=2, column=0)
hist4 = Histogram(win, n_pictures, 500, 300, "Number of pictures", doc, 3)
hist4.grid(row=2, column=1)
