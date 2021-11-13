class Node:
    children = []

    def __init__(self, key):
        self.key = key


class MarkovTree:
    root_nodes = []

    def __init__(self, markov_model, length: int):
        self.markov_model = markov_model
        self.length = length

    def create_tree(self):
        pass
        # for layer in range(self.length):
