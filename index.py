from nltk import text
from utility.Train import train
from models.CHiMP import *
from utility.ChimpSentenceGenerator import *
import pickle
from utility.print import *

number_of_sentences = 1000
text_file_path = "data"
# text_file_name = "ccil.txt"
# text_file_name = "one_sentence.txt"
# text_file_name = "book_medium.txt"
text_file_name = "w_fic_2012.txt"
text_file_path = f"{text_file_path}/{text_file_name}"
pickle_file = f"pickle_files/{text_file_name}.pickle"
model = "chimp"
verbose = True
markov_order = 1
pickle_model = True

model = train(number_of_sentences, text_file_path, pickle_file, model, verbose, markov_order=markov_order, pickle_model=pickle_model)
model_to_json(model, output_file=f"output/{text_file_name}")
# quit(0)

with open(pickle_file, "rb") as handle:
    model = pickle.load(handle)
# print_model(model)
# quit(0)

length = 3
# hidden_constraints = [[ConstraintIsPartOfSpeech("NP", True)], [ConstraintIsPartOfSpeech("VP", True)], None]
hidden_constraints = [[ConstraintIsPartOfSpeech("NP", True)], None, None]

# hidden_constraints = [None, None, None]
observed_constraints = [None, None, None]
# observed_constraints = []
# for _ in range(length):
#     observed_constraints.append(None)

NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
NHHMM.process()
print("NHHMM Finished")
# print_chimp_markov_probabilities(NHHMM)

sentence_generator = ChimpSentenceGenerator(NHHMM, length)
for _ in range(10):
    print(sentence_generator.create_sentence())
    print("\n")
