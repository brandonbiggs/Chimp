from utility.Train import train
from models.CHiMP import *
from utility.ChimpSentenceGenerator import *

number_of_sentences = 4
text_file = "data/ccil.txt"
pickle_file = "pickle_files/new_file.pickle"
model = "chimp"
verbose = True
markov_order = 1

model = train(number_of_sentences, text_file, pickle_file, model, verbose, markov_order=markov_order)
model.print()

length = 4
hidden_constraints = [[ConstraintIsPartOfSpeech("NNP", True)], None, None, None]

# observed_constraints = [None, None, ConstraintContainsString("t", True)]
observed_constraints = [None, None, None, None]

NHHMM = ConstrainedHiddenMarkovProcess(
        length, model, hidden_constraints, observed_constraints
    )
NHHMM.process()
print("NHHMM Finished")
NHHMM.print_new_markov_probabilities()

# sentence_generator = ChimpSentenceGenerator(NHHMM, length)
# for x in range(10):
#     print(sentence_generator.create_sentence())
#     print("\n")
