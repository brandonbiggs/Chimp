import nltk
from nltk.tokenize import RegexpTokenizer
from progress.bar import Bar
# from utility.Utility import read_text_file
import utility.Utility
import utility.CountSentences


nltk.download('tagsets', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)


class ProcessDataForChimp:
    file_name = ""
    file_contents = ""
    processed_output = []
    tokenized_text = ""
    tokens = []
    parts_of_speech = []

    number_of_sentences = 0

    # # DONE - Wouldn't be a bad idea to verify that these are working correctly however
    # observed_nodes = []  # List of every word that's possible
    # initial_probs = {}  # Dictionary (key: pos, value: probability of pos/count of pos)
    # emission_probs = {}
    # hidden_nodes = []  # This is a list of dictionaries for each POS
    # transition_probs = {}

    def __init__(self, file_name: str, number_of_sentences, progress_bar=True) -> None:
        """

        :param file_name: Name of the file to read and create probabilities from
        :param progress_bar: boolean, True creates a progress bar to follow. False
            doesn't.
        """
        # DONE - Wouldn't be a bad idea to verify that these are working correctly however
        self.observed_nodes = []  # List of every word that's possible
        self.initial_probs = {}  # Dictionary (key: pos, value: probability of pos/count of pos)
        self.emission_probs = {}
        self.hidden_nodes = []  # This is a list of dictionaries for each POS
        self.transition_probs = {}
        self.number_of_sentences = number_of_sentences
        if progress_bar:
            self.__init_with_progress(file_name)
        else:
            self.__init_without_progress_bar(file_name)

    def __init_with_progress(self, file_name: str) -> None:
        self.file_name = file_name
        bar = Bar('Processing', max=6)
        contents = utility.CountSentences.CountSentences(self.file_name)
        contents.shuffle_sentences(10)
        self.file_contents = \
            contents.sentence_list_as_string(contents.get_sentences(self.number_of_sentences))
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
        contents = utility.CountSentences.CountSentences(self.file_name)
        contents.shuffle_sentences(10)
        self.file_contents = \
            contents.sentence_list_as_string(contents.get_sentences(self.number_of_sentences))

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
        tokenizer = RegexpTokenizer(r'\w+')
        self.tokens = tokenizer.tokenize(self.file_contents)
        self.tokenized_text = nltk.pos_tag(self.tokens)

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
            # print(token)
            self.initial_probs.setdefault(token[1], []).append(1)
            self.emission_probs.setdefault(token[1], []).append([token[0], 1.0])

    def __create_emission_probabilities(self) -> None:
        """

        :return: None
        """
        for key in self.emission_probs.keys():
            word_count = len(self.emission_probs.get(key))
            list_of_items = {}
            for item in self.emission_probs.get(key):
                item[1] = item[1]/word_count
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
        word_count = len(self.tokenized_text)
        for key in self.initial_probs.keys():
            self.initial_probs[key] = len(self.initial_probs.get(key)) / word_count

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
                self.transition_probs.setdefault(previous_key, {}).update({current_key: 1.0})
                previous_token = token

        # We now iterate over all keys and calculate their probabilities
        for key in self.transition_probs.keys():
            count = len(self.transition_probs.get(key))
            for inner_key in self.transition_probs.get(key):
                self.transition_probs.get(key)[inner_key] = (1 / count)

        for pos in self.parts_of_speech:
            for inner_pos in self.parts_of_speech:
                if self.transition_probs.get(pos) is not None:
                    if inner_pos not in self.transition_probs.get(pos).keys():
                        self.transition_probs.get(pos).update({inner_pos: 0.0})


