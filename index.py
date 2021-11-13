from utility.Train import train

number_of_sentences = 2
text_file = "data/ccil.txt"
pickle_file = "pickle_files/new_file.pickle"
model = "markovmodel"
verbose = True

train(number_of_sentences, text_file, pickle_file, model, verbose)
