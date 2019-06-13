import numpy
from markovs_matrix.HiddenMarkovModelMatrices import *
from markovs.NonHomogeneousHMM import *
from markovs.NonHomogeneousHMMSentences import *
from constraints.ConstraintContainsString import *
from constraints.ConstraintIsPartOfSpeech import *
from constraints.ConstraintMatchesString import *
from constraints.ConstraintRhymesWith import *


def red_rhyme_matrix() -> None:
    """
    Example we'll be using for our research paper.
    :return: None
    """

    # Number of nodes in the graph. In our example, we're doing the same number of hidden and observed
    node_layers = 4

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
    initial_probs = numpy.array([1.0, 0.0, 0.0, 0.0])

    # Setup the initial transition probability matrix
    transition_probs = [
        [0.0,  0.4, 0.6, 0.0],
        [0.25, 0.0, 0.0, 0.75],
        [0.0,  1.0, 0.0, 0.0],
        [0.0,  0.0, 0.0, 0.0]
    ]

    list_of_matricies = []
    for i in range(node_layers):
        list_of_matricies.append(transition_probs)
    transition_probs_matrix = numpy.array(list_of_matricies)
    # print(transition_probs_matrix.shape)
    # print(transition_probs_matrix)

    emission_probs = [
        [0.2, 0, 0, 0],             # Ted
        [0, 0, 0.66666, 0],         # now
        [0, 0.5, 0, 0],             # likes
        [0, 0, 0, 0.33333],         # green
        [0.6, 0, 0, 0],             # Mary
        [0, 0, 0, .66666],          # red
        [0, 0.25, 0, 0],            # loves
        [0.2, 0, 0, 0],             # Fred
        [0, 0.25, 0, 0],            # sees
        [0, 0, 0.3333, 0],          # sometimes
    ]

    list_of_matricies = []
    for i in range(node_layers):
        list_of_matricies.append(emission_probs)
    emission_probs_matrix = numpy.array(list_of_matricies)
    # print(emission_probs_matrix.shape)
    # print(emission_probs_matrix)

    # Constraints for hidden and observed nodes
    #   The position of these is important as they represent the specific positions in the graphs
    hidden_constraints = [None, None, None, None]
    observed_constraints = [ConstraintRhymesWith("red", True), None, None,
                            ConstraintMatchesString("red", True)]

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModelMatrix(hidden_nodes, observed_nodes)
    hidden_markov_model.initial_probs = initial_probs
    hidden_markov_model.transition_probs = transition_probs_matrix
    hidden_markov_model.emission_probs = emission_probs_matrix
    hidden_markov_model.print()

    # Create our NHHMM and calculate new probabilities from the constraints
    # NHHMM = NonHomogeneousHMM(length, hidden_markov_model, hidden_constraints, observed_constraints)
    # NHHMM.process()
    # NHHMM.print_new_markov_probabilities()

    # Print the sentences
    # sentence_generator = NonHomogeneousHMMSentences(NHHMM, 4)
    # sentences = sentence_generator.create_all_sentences()
    # for sentence in sentences:
    #     # sentence = sentence.strip().split(" ")
    #     print(sentence)
    # print("Number of sentences:", len(sentences))
