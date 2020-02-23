import os
import subprocess
from utility.Utility import *
from utility.CountSentences import *
#from utility.SendEmail import SendEmail

import nltk

import time

start = time.time()
# python_path = "/usr/bin/python3.7"
python_path = "/Users/biggbs/school/Chimp/chimp-env/bin/python3"
python_file = "index.py"
iterations = 100000
sentences_count = 100000
# lengths = [4, 6, 8, 10, 12, 14]
# lengths = [4]
data_file = "data/w_fic_2012.txt"
number_of_shuffles = 0

# This is the part that should be replaced with a pandas dataframe
contents = utility.CountSentences.CountSentences(data_file)

results_file = "results/iccc_2020_mnemonics.txt"
pickle_file = "pickle_files/iccc_2020.pickle"


file_contents = contents.sentence_list_as_string(
    contents.get_sentences(sentences_count)
)
train(number_of_sentences=sentences_count,
      text_file=file_contents,
      pickle_file=pickle_file,
      model="chimp",
      text_contents=True)
command = (python_path + " " + python_file + " -g iterations:" + str(iterations) + " sentences:" + str(sentences_count)
            + " length:" + str(sentences_count) + " data_file:" + data_file + " results_file:" + results_file + " pickle_file:"
            + pickle_file #+ " pickle_mm_file:"+ pickle_mm_file
        )

print(command)
        # os.system(command)

message = "Test complete. It took " + str(time.time() - start) + " seconds"
print(message)
# email = SendEmail(message)
# email.send_email()
