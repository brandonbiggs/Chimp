import os
import subprocess
from utility.Utility import *

python_path = "/usr/bin/python3.7"
python_file = "index.py"
iterations = 100
sentences = [250, 25]
lengths = [4, 6]
data_file = "data/w_fic_2012.txt"

for length in lengths:
    results_file = "results/batch_results_" + str(length) + ".txt"
    pickle_file = "pickle_files/batch_results_" + str(length) + ".pickle"
    pickle_mm_file = "pickle_files/batch_results_mm_" + str(length) + ".pickle"
    # train(length, data_file, pickle_file, "chimp", False)
    # train(length, data_file, pickle_mm_file, "markovmodel", False)
    for sentence in sentences:
        command = python_path + " " + python_file + " -g iterations:" + str(iterations) + \
                  " sentences:" + str(sentence) + " length:" + str(length) + " data_file:" + \
                  data_file + " results_file:" + results_file + " pickle_file:" + pickle_file + \
                  " pickle_mm_file:" + pickle_mm_file
        # command = "iterations:" + str(iterations) + \
        #           " sentences:" + str(sentence) + " length:" + str(length) + " data_file:" + \
        #           data_file + " results_file:" + results_file + " pickle_file:" + pickle_file + \
        #           " pickle_mm_file:" + pickle_mm_file
        # print(command)
        os.system(command)
        # gc.collect()

