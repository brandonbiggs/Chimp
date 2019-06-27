from markovs.HiddenMarkovModel import *
from markovs_parallel.ChimpParallel import parallel_nhmm
from markovs.ChimpSentenceGenerator import *
from constraints.ConstraintContainsString import *
from constraints.ConstraintIsPartOfSpeech import *
from constraints.ConstraintMatchesString import *
from constraints.ConstraintRhymesWith import *


def red_rhyme_parallel() -> None:
    """
    Example we'll be using for our research paper.
    :return: None
    """

    # Define the part of speech dictionaries
    NNP = {"Ted": 0.2, "Mary": 0.6, "Fred": 0.2}            # Proper Noun
    RB = {"now": 0.66666, "sometimes": 0.33333}             # Adverb
    VBZ = {"likes": 0.5, "loves": 0.25, "sees": 0.25}       # Verb
    NN = {"green": 0.33333, "red": 0.66666}                 # Singular noun

    # Define the sets of hidden and observed nodes
    hidden_nodes = [NNP, RB, VBZ, NN]
    observed_nodes = ['Ted', 'now', 'likes', 'green', 'Mary', 'red', 'loves',
                      'Fred', 'sees', 'sometimes']

    # Define the initial probabilities
    initial_probs = {"NNP": 1.0}

    # Define the transition probabilities
    transition_probs = {"NNP": {"NNP": 0.0, "VBZ": 0.4, "RB": 0.6, "NN": 0.0},
                        "VBZ": {"NNP": 0.25, "VBZ": 0.0, "RB": 0.0, "NN": 0.75},
                        "RB": {"NNP": 0.0, "VBZ": 1.0, "RB": 0.0, "NN": 0.0},
                        "NN": {"NNP": 0.0, "VBZ": 0.0, "RB": 0.0, "NN": 0.0}}

    # Define the emission probabilities.
    emission_probs = {"NNP": NNP, "VBZ": VBZ, "RB": RB, "NN": NN}

    # Number of nodes in the graph. In our example, we're doing the same number of hidden and observed
    length = 4

    # Constraints for hidden and observed nodes
    #   The position of these is important as they represent the specific positions in the graphs
    # hidden_constraints = [None, None, None, ConstraintIsPartOfSpeech("NN", True)]
    hidden_constraints = [None, None, None, None]
    # observed_constraints = [None, None, None, None]
    observed_constraints = [ConstraintRhymesWith("red", True), None, None,
                            ConstraintMatchesString("red", True)]

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(hidden_nodes, observed_nodes)
    hidden_markov_model.initial_probs = initial_probs
    hidden_markov_model.transition_probs = transition_probs
    hidden_markov_model.emission_probs = emission_probs
    # hidden_markov_model.print()

    # Create our NHHMM and calculate new probabilities from the constraints
    NHHMM = parallel_nhmm(length, hidden_markov_model, hidden_constraints, observed_constraints)
    NHHMM.process()
    # NHHMM.print_new_markov_probabilities()

    # Print the sentences
    sentence_generator = ChimpSentenceGenerator(NHHMM, 4)
    sentences = sentence_generator.create_all_sentences()
    # for sentence in sentences:
        # sentence = sentence.strip().split(" ")
        # print(sentence)
    # print("Number of sentences:", len(sentences))
