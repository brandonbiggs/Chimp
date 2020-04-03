import nltk
from nltk.tokenize import RegexpTokenizer
from progress.bar import Bar

# from utility.Utility import read_text_file
import utility.Utility
import utility.CountSentences


# nltk.download("tagsets", quiet=True)
# nltk.download("averaged_perceptron_tagger", quiet=True)


class ProcessDataForChimp:
    def __init__(
        self, file: str, number_of_sentences, progress_bar=True, file_contents=False
    ) -> None:
        """
        :param file: Name of the file to read and create probabilities from
        :param number_of_sentences:
        :param progress_bar: boolean, True creates a progress bar to follow. False
            doesn't.
        :param file_contents: If this is set to true, file is not the name of a file,
        but it's actually the contents of a file. The purpose of this is to make sure
        chimp and markov model are using the same exact sentences. Verbose and text_contents
        should not both be set to True
        """
        self.file_name = ""
        self.file_contents = ""
        self.processed_output = []
        self.tokenized_text = []
        self.tokens = []
        self.parts_of_speech = []
        # DONE - Wouldn't be a bad idea to verify that these are working correctly however
        self.observed_nodes = []  # List of every word that's possible
        self.initial_probs = (
            {}
        )  # Dictionary (key: pos, value: probability of pos/count of pos)
        self.emission_probs = {}
        self.hidden_nodes = []  # This is a list of dictionaries for each POS
        self.transition_probs = {}
        self.number_of_sentences = number_of_sentences
        self.file_contents_bool = file_contents
        if progress_bar:
            self.__init_with_progress(file)
        else:
            self.__init_without_progress_bar(file)

    def __init_with_progress(self, file_name: str) -> None:
        self.file_name = file_name
        bar = Bar("Processing", max=6)
        if self.file_contents_bool:
            self.file_contents = self.file_name
        else:
            contents = utility.CountSentences.CountSentences(self.file_name)
            contents.shuffle_sentences(10)
            self.file_contents = contents.sentence_list_as_string(
                contents.get_sentences(self.number_of_sentences)
            )
        # self.file_contents = utility.Utility.read_text_file(self.file_name)
        bar.next()
        self.tokenize_and_tag_text()
        bar.next()
        self.create_pos_dictionaries()
        bar.next()
        # Create each of the probability dictionaries
        self.__create_initial_probabilities()
        bar.next()
        self.__create_emission_probabilities()
        bar.next()
        self.__create_transition_probabilities()
        bar.next()
        bar.finish()

    def __init_without_progress_bar(self, file_name: str) -> None:
        self.file_name = file_name

        # self.file_contents = utility.Utility.read_text_file(self.file_name)
        if self.file_contents_bool:
            self.file_contents = self.file_name
        else:
            contents = utility.CountSentences.CountSentences(self.file_name)
            contents.shuffle_sentences(10)
            self.file_contents = contents.sentence_list_as_string(
                contents.get_sentences(self.number_of_sentences)
            )

        self.tokenize_and_tag_text()
        self.create_pos_dictionaries()

        # Create each of the probability dictionaries
        self.__create_initial_probabilities()
        self.__create_emission_probabilities()
        self.__create_transition_probabilities()

    def tokenize_and_tag_text(self) -> None:
        """
        Uses nltk to tokenize and tag each word with it's POS in the string
        :return: None
        """
        sentences = self.file_contents.split(".")
        for sentence in sentences:
            sentence = sentence.lstrip().rstrip()
            if sentence == "":
                continue

            tokenizer = RegexpTokenizer(r"\w+")
            tokens = tokenizer.tokenize(sentence)
            tokenized_text = nltk.pos_tag(tokens)

            self.tokens.extend(tokens)
            self.tokenized_text.extend(tokenized_text)

            # Count first word pos into initial probabilities
            if len(tokenized_text) > 0:
                self.initial_probs.setdefault(tokenized_text[0][1], 0.0)
                self.initial_probs[tokenized_text[0][1]] += 1.0

    def create_pos_dictionaries(self) -> None:
        """
        Iterates through the tokens and draws out their parts of speech
            into dictionaries, that can be used later
        :return: None
        """
        for token in self.tokenized_text:
            # Creating observed nodes
            if token[0] not in self.observed_nodes:
                self.observed_nodes.append(token[0])
            # Creating count of each token
            self.emission_probs.setdefault(token[1], []).append([token[0], 1.0])

    def __create_emission_probabilities(self) -> None:
        """

        :return: None
        """
        for key in self.emission_probs.keys():
            word_count = len(self.emission_probs.get(key))
            list_of_items = {}
            for item in self.emission_probs.get(key):
                item[1] = item[1] / word_count
                if item[0] not in list_of_items.keys():
                    list_of_items[item[0]] = item[1]
                else:
                    list_of_items[item[0]] += item[1]
            self.emission_probs[key] = list_of_items
            self.hidden_nodes.append(list_of_items)

    def __create_initial_probabilities(self) -> None:
        """

        :return: None
        """
        total_initial_nodes = sum(self.initial_probs.values())
        for key in self.initial_probs.keys():
            self.initial_probs[key] = self.initial_probs.get(key) / total_initial_nodes

    def __create_transition_probabilities(self):
        # TODO - Improvement - Maybe calculate transitions at the same time of
        #   putting them into the transition dictionary
        # This is the probabilities from one part of speech to another
        #       need to confirm that this is the right way we're doing this
        #  TODO - Ask, is this order one markov? Is there a specific order in this
        #       kind of model?
        #     transition_probs = {"DT": {"NN": 1.0, "DT": 0.0, "NNS": 0.0},
        #                  "NN": {"NN": 0.1, "DT": 0.2, "NNS": 0.7},
        #                  "NNS": {"NN": 0.4, "DT": 0.5, "NNS": 0.1}}

        # We look at the transitions between a current token and the previous
        #   token. Then we add that transition to the transition dictionary
        first_token = True
        previous_token = ""
        for token in self.tokenized_text:
            if token[1] not in self.parts_of_speech:
                self.parts_of_speech.append(token[1])
            # If first token, we set previous token then skip to the next token
            if first_token:
                previous_token = token
                first_token = False
            # If not first token, get the keys, add them to the transition dict
            else:
                previous_key = previous_token[1]
                current_key = token[1]
                # if we haven't created a dict yet for the previous key
                self.transition_probs.setdefault(previous_key, {current_key: 0.0})
                self.transition_probs[previous_key].setdefault(current_key, 0.0)
                self.transition_probs[previous_key][current_key] += 1
                previous_token = token

        # We now iterate over all keys and calculate their probabilities
        for key in self.transition_probs.keys():
            total_count = sum(self.transition_probs.get(key).values())
            for inner_key in self.transition_probs.get(key):
                value = self.transition_probs.get(key)[inner_key]
                self.transition_probs.get(key)[inner_key] = value / total_count

        for pos in self.parts_of_speech:
            for inner_pos in self.parts_of_speech:
                if self.transition_probs.get(pos) is not None:
                    if inner_pos not in self.transition_probs.get(pos).keys():
                        self.transition_probs.get(pos).update({inner_pos: 0.0})
