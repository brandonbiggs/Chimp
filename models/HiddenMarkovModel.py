from rich.pretty import pprint
from rich.json import JSON

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

    markov_order = 1

    def __init__(self, hidden_nodes, observed_nodes):
        self.hidden_nodes = hidden_nodes
        self.observed_nodes = observed_nodes

    def print(self):
        pprint("Hidden Markov Model")
        
        print(f"Hidden Nodes:")
        pprint(self.hidden_nodes)
        
        print(f"Observed Nodes:")
        pprint(self.observed_nodes)
        
        print(f"Initial Probabilities: ")
        pprint(self.initial_probs)
        
        print(f"Transition Probabilities:")
        pprint(self.transition_probs)
        
        print(f"Emission Probabilities")
        pprint(self.emission_probs)
        
        print(f"Markov Order: {self.markov_order}")
