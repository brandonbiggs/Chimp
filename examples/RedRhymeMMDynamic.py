from markovs.HiddenMarkovModel import *
from markovs.ConstrainedHiddenMarkovProcess import *
from markovs.ChimpSentenceGenerator import *
from utility.ProcessDataForMM import *


def red_rhyme_mm_dynamic() -> None:
    """

    :return: None
    """
    data = ProcessDataForMM("data/ccil.txt")

    length = 4
    hidden_constraints = [None, None, None, None]
    observed_constraints = [
        ConstraintRhymesWith("red", True),
        None,
        None,
        ConstraintMatchesString("red", True),
    ]

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(data.hidden_nodes, data.observed_nodes)
    hidden_markov_model.initial_probs = data.initial_probs
    hidden_markov_model.transition_probs = data.transition_probs
    hidden_markov_model.emission_probs = data.emission_probs

    # Process the constrained hidden markov model
    NHHMM = ConstrainedHiddenMarkovProcess(
        length, hidden_markov_model, hidden_constraints, observed_constraints
    )
    NHHMM.process()
    # NHHMM.print_new_markov_probabilities()

    # Print the sentences
    sentence_generator = ChimpSentenceGenerator(NHHMM, 4)
    sentences = sentence_generator.create_all_sentences()
    for sentence in sentences:
        print(sentence)
    print("Number of sentences:", len(sentences))
