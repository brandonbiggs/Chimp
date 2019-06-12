from constraints.Constraint import *
from constraints.ConstraintContainsString import *
from constraints.ConstraintIsPartOfSpeech import *
from constraints.ConstraintRhymesWith import *
from constraints.ConstraintMatchesString import *
from constraints.NoConstraint import *
from markovs.HiddenMarkovModel import *
from markovs.NonHomogeneousHMM import *
from markovs.NonHomogeneousHMMSentences import *


def first_dog() -> None:
    """
    First example based on the simple noun, verb, determinate example we did
        while in our research meeting. The parts of speech are defined from
        NLTK.

    DT: Determinate/articles
    NN: Noun
    NNS: Supposed to be verbs, but NLTK takes our words in their context as NNS
    :return: None
    """

    # Define the part of speech dictionaries
    DT = {"the": 0.1, "a": 0.3, "an": 0.6}
    NN = {"dog": 0.2, "cat": 0.4, "ant": 0.4}
    NNS = {"eats": 0.5, "kicks": 0.25, "bites": 0.25}

    # Define the sets of hidden and observed nodes
    hidden_nodes = [DT, NN, NNS]
    observed_nodes = ["dog", "cat", "ant", "bites", "kicks", "eats", "the", "a", "an"]

    # Define the initial probabilities
    initial_probs = {"DT": 0.6, "NN": 0.3, "NNS": 0.1}

    # Define the transition probabilities
    # transition_probs = {"DT": {"NN": 1.0, "DT": 0.0, "NNS": 0.0},
    #              "NN": {"NN": 0.1, "DT": 0.2, "NNS": 0.7},
    #              "NNS": {"NN": 0.4, "DT": 0.5, "NNS": 0.1}}
    transition_probs = {"DT": {"DT": 0.0, "NN": 1.0, "NNS": 0.0},
                 "NN": {"NN": 0.1, "DT": 0.2, "NNS": 0.7},
                 "NNS": {"NNS": 0.1, "DT": 0.5, "NN": 0.4}}

    # Define the emission probabilities.
    emission_probs = {"DT": DT, "NN": NN, "NNS": NNS}
    # emission_probs = {"DT": {"the": 0.1, "a": 0.3, "an": 0.6},
    #             "NN": {"dog": 0.2, "cat": 0.4, "ant": 0.4},
    #             "NNS": {"eats": 0.5, "kicks": 0.25, "bites": 0.25}}

    # Number of nodes in the graph. In our example, we're doing the same number of hidden and observed
    length = 3

    # Constraints for hidden and observed nodes
    #   The position of these is important as they represent the specific positions in the graphs
    hidden_constraints = [None, ConstraintIsPartOfSpeech("NNS", True), ConstraintIsPartOfSpeech("NN", True)]
    observed_constraints = [None, None, ConstraintContainsString("t", True)]
    # hidden_constraints = [None, None, None]
    # observed_constraints = [None, None, None]

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(hidden_nodes, observed_nodes)
    hidden_markov_model.initial_probs = initial_probs
    hidden_markov_model.transition_probs = transition_probs
    hidden_markov_model.emission_probs = emission_probs
    # hidden_markov_model.print()
    # return

    # Create our NHHMM and calculate new probabilities from the constraints
    NHHMM = NonHomogeneousHMM(length, hidden_markov_model, hidden_constraints, observed_constraints)
    NHHMM.process()
    NHHMM.print_new_markov_probabilities()

    # sentence_generator = NonHomogeneousHMMSentences(NHHMM, 3)
    # sentences = sentence_generator.create_all_sentences()
    # for sentence in sentences:
    #     sentence = sentence.strip().split(" ")
    #     print(sentence)
    # print("Number of sentences:", len(sentences))