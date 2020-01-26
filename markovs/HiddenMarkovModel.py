class HiddenMarkovModel:
    """
    TODO - Instead of strings as the keys in the probabilities, we need to keep
        just one list of strings that we can look up
    TODO - some kind of ID functionality in keeping track of things. Smaller
        data types. Trade off between memory and speed. May be able to use an
        enum for all the possible items that exist in NLTK
    """

    # transition_probs = dict(key=str, value=dict(key=str, value=float))
    transition_probs = dict()

    # initialProbs = dict(key=str, value=float)
    initial_probs = dict()

    # emissionProbs = dict(key=str, value=dict(key=str, value=float))
    emission_probs = dict()

    # hidden_nodes = List of nodes
    hidden_nodes = []

    # observed_nodes = List of nodes
    observed_nodes = []

    def __init__(self, hidden_nodes, observed_nodes):
        self.hidden_nodes = hidden_nodes
        self.observed_nodes = observed_nodes

    def print(self):
        print("Hidden Markov Model")
        print("Hidden Nodes:", self.hidden_nodes)
        print("Observed Nodes:", self.observed_nodes)
        print("Initial Probabilities:", self.initial_probs)
        print("Transition Probabilities:", self.transition_probs)
        print("Emission Probabilities:", self.emission_probs)
