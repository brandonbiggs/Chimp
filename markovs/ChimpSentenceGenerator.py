import copy
from utility.Utility import get_rand_num


class ChimpSentenceGenerator:
    """
    Generate sentences with the given NHHMM
    """
    NHHMM = ""
    sentence = ""
    initial_pos = ""
    length = 0

    def __init__(self, NHHMM, length):
        self.NHHMM = NHHMM
        self.length = length

    def create_sentence(self) -> str:
        sentence = ""
        for node_layer in range(self.length):
            if node_layer == 0:
                pos = self.get_first_pos()
            else:
                pos = self.get_pos(node_layer, self.initial_pos)
            next_word = self.get_emission_word(node_layer, pos)
            if next_word is not None:
                sentence += next_word + " "
        return sentence.rstrip()

    def get_pos(self, node_layer, pos):
        """

        :param node_layer:
        :return:
        """
        rand = get_rand_num()
        count = 0
        emission_probs = \
            self.NHHMM.constrained_transition_probabilities[node_layer].get(pos)
        if emission_probs is None:
            return None
        for key in emission_probs.keys():
            count += emission_probs.get(key)
            if rand < count:
                if key is not None:
                    self.initial_pos = key
                    return key

    def get_first_pos(self) -> str:
        """
        Gets the part of speech from the initial probabilities using
            a binning technique of picking from the dictionary
        """
        rand = get_rand_num()
        sum = 0
        initial_probs = self.NHHMM.constrained_transition_probabilities[0]
        for key in initial_probs.keys():
            if len(initial_probs.keys()) == 1:
                self.initial_pos = key
                return key
            sum += initial_probs.get(key)
            if rand < sum:
                if key is not None:
                    self.initial_pos = key
                    return key

    def get_emission_word(self, node_layer: int, pos: str) -> str:
        """

        :param node_layer:
        :param pos:
        :return: word from the emission probability
        """
        rand = get_rand_num()
        sum = 0
        emission_probs = \
            self.NHHMM.constrained_observed_emission_probabilities[node_layer].get(pos)

        if emission_probs is None:
            return None
        for key in emission_probs.keys():
            sum += emission_probs.get(key)
            if rand < sum:
                return key

    def create_all_sentences(self, num_sentences=100):
        sentences = []
        for x in range(num_sentences):
            sentence = self.create_sentence()
            # print(sentence.split(" "))
            if sentence not in sentences and len(sentence.split(" ")) == self.length:
                sentences.append(sentence)
        return sentences

    def create_possible_sentence_structure(self) -> []:
        """
        This currently isn't used for anything
        :return:
        """
        sentence_structure = []
        previous_pos = []
        for layer in range(self.length):
            pos_list = []
            if layer == 0:
                for key in self.NHHMM.constrained_transition_probabilities[layer]:
                    pos_list.append(key)
                    sentence_structure.append([layer, key])
            else:
                for pos in previous_pos:
                    for key in self.NHHMM.constrained_transition_probabilities[layer].get(pos):
                        if self.NHHMM.constrained_transition_probabilities[layer].get(pos).get(key) != 0:
                            pos_list.append(key)
                            sentence_structure.append([layer, key])
            previous_pos.clear()
            previous_pos = copy.deepcopy(pos_list)
        print("Sentence Structure:", sentence_structure)
        return sentence_structure
