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

    def __init__(self, NHHMM, length: int) -> None:
        self.NHHMM = NHHMM
        self.length = length

    def create_sentence(self, include_pos_tags: bool = False) -> str:
        sentence = ""
        for node_layer in range(self.length):
            if node_layer == 0:
                pos = self.get_first_pos()
            else:
                pos = self.get_pos(node_layer, self.initial_pos)
            next_word = self.get_emission_word(node_layer, pos)
            if next_word is not None:
                # TODO - Play with this a little bit to learn about porter's comment
                # Account for integrated pos tags
                if next_word != pos: 
                    if include_pos_tags:
                        sentence += f"{next_word}: {''.join(pos)} "
                    else: sentence += f"{next_word} "
                else:
                    sentence += next_word + " "

        return sentence.rstrip()

    def get_pos(self, node_layer: int, pos):
        """

        :param node_layer:
        :return:
        """
        rand = get_rand_num()
        count = 0
        emission_probs = self.NHHMM.constrained_transition_probabilities[node_layer].get(pos)
        if emission_probs is None:
            return None
        for key in emission_probs.keys():
            count += emission_probs.get(key)
            if rand < count:
                if key is not None:
                    self.initial_pos = key
                    return key[-1]

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
                    return key[-1]

    def get_emission_word(self, node_layer: int, pos: list) -> str:
        """

        :param node_layer:
        :param pos:
        :return: word from the emission probability
        """
        rand = get_rand_num()
        sum = 0
        if len(pos) == 1:
            emission_probs = self.NHHMM.constrained_observed_emission_probabilities[node_layer][pos[0]]
        elif isinstance(pos, str):
            emission_probs = self.NHHMM.constrained_observed_emission_probabilities[node_layer][pos]
        # TODO - Figure out how to generate sentences on markov order > 1
        else:
            emission_probs = None
        if emission_probs is None:
            return None
        for key in emission_probs.keys():
            sum += emission_probs.get(key)
            if rand < sum:
                return key

    def create_all_sentences(self, num_sentences=100):
        sentences = []
        for _ in range(num_sentences):
            sentence = self.create_sentence()
            if sentence not in sentences and len(sentence.split(" ")) == self.length:
                sentences.append(sentence)
        return sentences

    def create_possible_sentence_structure(self) -> list:
        """
        # TODO - This still has bugs, but it's not used
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
                    for key in self.NHHMM.constrained_transition_probabilities[
                        layer
                    ].get(pos):
                        if (
                            self.NHHMM.constrained_transition_probabilities[layer]
                            .get(pos)
                            .get(key)
                            != 0
                        ):
                            pos_list.append(key)
                            sentence_structure.append([layer, key])
            previous_pos.clear()
            previous_pos = copy.deepcopy(pos_list)
        # print("Sentence Structure:", sentence_structure)
        return sentence_structure
