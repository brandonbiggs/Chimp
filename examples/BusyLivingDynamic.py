from constraints.Constraint import *
from constraints.ConstraintContainsString import *
from constraints.ConstraintIsPartOfSpeech import *
from constraints.ConstraintRhymesWith import *
from constraints.ConstraintMatchesString import *
from constraints.NoConstraint import *
from markovs.HiddenMarkovModel import *
from markovs.ConstrainedHiddenMarkovProcess import *
from markovs.ChimpSentenceGenerator import *
import pickle


def busy_living_dynamic(size=7) -> None:
    # Load data (deserialize)
    with open('pickle_files/hmm.pickle', 'rb') as handle:
        hidden_markov_model = pickle.load(handle)

    hidden_constraints = [
        ConstraintIsPartOfSpeech("NNP", True),
        ConstraintIsPartOfSpeech("JJ", True),
        ConstraintIsPartOfSpeech("NN", True),
        ConstraintIsPartOfSpeech("CC", True),
        ConstraintIsPartOfSpeech("VB", True),
        ConstraintIsPartOfSpeech("JJ", True),
        ConstraintIsPartOfSpeech("VBG", True)
    ]
    # observed_constraints = [None, None, ConstraintContainsString("t", True)]
    observed_constraints = [None, None, None, None, None, None, None]

    length = size

    NHHMM = NonHomogeneousHMM(length, hidden_markov_model,
                              hidden_constraints,
                              observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")

    sentence_generator = NonHomogeneousHMMSentences(NHHMM, length)
    for x in range(10):
        print(sentence_generator.create_sentence())