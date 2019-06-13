import numpy
class HiddenMarkovModelMatrix:
    """
    TODO - some kind of ID functionality in keeping track of things. Smaller
        data types. Trade off between memory and speed. May be able to use an
        enum for all the possible items that exist in NLTK
    """
    # N = number of parts of speech
    # M = Number of node layers
    # O = # of unique words
    # transition_probs = POS x POS x node layers
    transition_probs = numpy.array([])

    # initial_probs = One dimensional array N long
    initial_probs = numpy.array([])

    # emission_probs = POS x Words x node layers
    emission_probs = numpy.array([])

    # hidden_nodes = List of nodes
    hidden_nodes = []

    # observed_nodes = List of nodes
    observed_nodes = []

    def __init__(self, hidden_nodes, observed_nodes):
        self.hidden_nodes = hidden_nodes
        self.observed_nodes = observed_nodes

    def print(self):
        print("\nHidden Markov Model")
        print("Hidden Nodes:", self.hidden_nodes)
        print("Observed Nodes:", self.observed_nodes)

        print("Initial Probabilities:", self.initial_probs.shape)
        print(self.initial_probs)
        print("Transition Probabilities:", self.transition_probs.shape)
        print(self.transition_probs)
        print("Emission Probabilities:", self.emission_probs.shape)
        print(self.emission_probs)