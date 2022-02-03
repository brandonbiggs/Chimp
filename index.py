import pickle

from utility.Train import train
from utility.Utility import *
from utility.print import *
from utility.ChimpSentenceGenerator import *
from models.CHiMP import *

print("Setting up..")
number_of_sentences = 10000
# John likes the blue house at the end of the street.
# text_file_path = "data"
# text_file_name = "one_sentence.txt"

text_file_path = "/home/biggbs/school/COCA-Dataset/CocaDataset-01/"
text_file_name = "2016_acad.txt"

text_file_path = f"{text_file_path}/{text_file_name}"
pickle_hmm_file = f"pickle_files/{text_file_name}.pickle"
pickle_chimp_model_file = f"pickle_files/{text_file_name}_chimp.pickle"

model = "chimp"
verbose = True
markov_order = 1
pickle_model_bool = True

# print_sentence_tree("John likes the blue house at the end of the street.")
print("Starting training..")
model = train(number_of_sentences, text_file_path, pickle_hmm_file, model, verbose, markov_order=markov_order, pickle_model_bool=pickle_model_bool)
# model_to_json(model, output_file=f"output/{text_file_name}")
# print_chimp_markov_probabilities(model)
print_model(model)
exit(0)

with open(pickle_hmm_file, "rb") as handle:
    model = pickle.load(handle)

length = 3
# hidden_constraints = [[ConstraintIsPartOfSpeech("NP", True)], [ConstraintIsPartOfSpeech("VP", True)], None]
# hidden_constraints = [[ConstraintIsPartOfSpeech("NP", True)], None, None]

hidden_constraints = [None, None, None]
observed_constraints = []
for _ in range(length):
    observed_constraints.append(None)

NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
NHHMM.process()
pickle_model(pickle_chimp_model_file, NHHMM, True)
print("NHHMM Finished")
# print_chimp_markov_probabilities(NHHMM)
# print_model(NHHMM)

# sentence_generator = ChimpSentenceGenerator(NHHMM, length)
# for _ in range(10):
#     print(sentence_generator.create_sentence())
#     print("\n")
