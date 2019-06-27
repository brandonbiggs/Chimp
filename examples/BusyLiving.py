from constraints.Constraint import *
from constraints.ConstraintContainsString import *
from constraints.ConstraintIsPartOfSpeech import *
from constraints.ConstraintRhymesWith import *
from constraints.ConstraintMatchesString import *
from constraints.NoConstraint import *
from markovs.HiddenMarkovModel import *
from markovs.ConstrainedHiddenMarkovProcess import *
from markovs.ChimpSentenceGenerator import *
from utility.ProcessDataForChimp import *


def busy_living() -> None:
    """

    :return: None
    """
    data = ProcessDataForChimp("data/book.txt")
    # data = ProcessTextFile("data/book_medium.txt")

    length = 7
    # Constraints for hidden and observed nodes
    #   The position of these is important as they represent the
    #   specific positions in the graphs. There needs to be as many of them
    #   as the size of length
    # hidden_constraints = [None, ConstraintIsPartOfSpeech("NNS", True), ConstraintIsPartOfSpeech("NN", True)]
    # hidden_constraints = [None, ConstraintIsPartOfSpeech("NNS", True), ConstraintIsPartOfSpeech("NN", True)]
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

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(data.hidden_nodes, data.observed_nodes)
    hidden_markov_model.initial_probs = data.initial_probs
    hidden_markov_model.transition_probs = data.transition_probs
    hidden_markov_model.emission_probs = data.emission_probs
    print("HMM Finished")

    NHHMM = ConstrainedHiddenMarkovProcess(length, hidden_markov_model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")

    sentence_generator = ChimpSentenceGenerator(NHHMM, length)
    for x in range(10):
        print(sentence_generator.create_sentence())