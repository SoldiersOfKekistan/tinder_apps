version: 1.1.1
These are my analiser and helper files for the Tinder dataset.
Currently includes:

File                Use                                                 Required moduls
- path.py           Define where your files are                         
- app.py            Local tinder application                            Tkinter, Pillow
- bio_merger.py     Merges bios for faster text analisation             
- bio_length.py     Plots bio length distribution                       matplotlib
- histogram.py      Interactive histograms                              Tkinter
- avg.py            Calculating average and median                      
- wc.py             Counts frequency of words                           nltk, nltk.data(popular)
- filters.txt       Filters for swear and sexual words                  
- filtered_words.py Selects words with given filters                    

Start with setting up your path in path.py.
Python 3+ is expected for running any of the files.
Further information and manuals are in the files.

Planned features:
- histograms for filtered words
- picture statistics targeting number of faces found
- neural network to recognise specific groups of people
- GAN neural network to generate faces from specific groups of people

Message me at atkakukac@citromail.com if you are interested.

Sincerelly,
Anon
