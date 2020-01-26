import os
import subprocess
from utility.Utility import *
from utility.CountSentences import *
from utility.SendEmail import SendEmail

# import gc
import time

start = time.time()
python_path = "/usr/bin/python3.7"
python_file = "index.py"
iterations = 100000
sentences = [25, 250, 2500, 25000, 250000, 2500000]
lengths = [4, 6, 8, 10, 12, 14]
data_file = "data/w_fic_2012.txt"
number_of_shuffles = 10

contents = utility.CountSentences.CountSentences(data_file)

for length in lengths:
    results_file = "results/batch_results_" + str(length) + ".txt"
    pickle_file = "pickle_files/batch_results_" + str(length) + ".pickle"
    pickle_mm_file = "pickle_files/batch_results_mm_" + str(length) + ".pickle"

    for sentence in sentences:
        contents.shuffle_sentences(number_of_shuffles)
        file_contents = contents.sentence_list_as_string(
            contents.get_sentences(sentence)
        )
        train(length, file_contents, pickle_file, "chimp", False, text_contents=True)
        train(
            length,
            file_contents,
            pickle_mm_file,
            "markovmodel",
            False,
            text_contents=True,
        )
        command = (
            python_path
            + " "
            + python_file
            + " -g iterations:"
            + str(iterations)
            + " sentences:"
            + str(sentence)
            + " length:"
            + str(length)
            + " data_file:"
            + data_file
            + " results_file:"
            + results_file
            + " pickle_file:"
            + pickle_file
            + " pickle_mm_file:"
            + pickle_mm_file
        )
        # command = "iterations:" + str(iterations) + \
        #           " sentences:" + str(sentence) + " length:" + str(length) + " data_file:" + \
        #           data_file + " results_file:" + results_file + " pickle_file:" + pickle_file + \
        #           " pickle_mm_file:" + pickle_mm_file
        # print(command)
        os.system(command)
        # gc.collect()

message = "Test complete. It took " + str(time.time() - start) + " seconds"
print(message)
email = SendEmail(message)
email.send_email()
