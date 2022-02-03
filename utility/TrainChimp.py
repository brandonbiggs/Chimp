from re import sub
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.data import find
from bllipparser import RerankingParser
from progress.bar import Bar

# from utility.Utility import read_text_file
import utility.Utility as ut
import utility.CountSentences as countSentences


# nltk.download("tagsets", quiet=True)
# nltk.download("averaged_perceptron_tagger", quiet=True)


class TrainChimp():
    def __init__(self, file: str, number_of_sentences, progress_bar=True, file_contents=False, markov_order=1) -> None:
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
        # List of every word that's possible
        self.observed_nodes = [] 
        
        # Dictionary (key: pos, value: probability of pos/count of pos)
        self.initial_probs = ({})  
        self.emission_probs = {}
        
        # This is a list of dictionaries for each POS
        self.hidden_nodes = [] 
        self.transition_probs = {}
        self.markov_order = markov_order
        self.number_of_sentences = number_of_sentences
        self.file_contents_bool = file_contents

        # Sentence parser
        self.part_of_sentence_labels = ["NP", "VP", "ADVP"]
        while True:
            try:
                self.parser = RerankingParser.from_unified_model_dir('nltk_data/models/WSJ-PTB3')
                break
            except:
                pass
        
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
            contents = countSentences.CountSentences(self.file_name)
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
        # sentences = self.file_contents.split(".")
        sentences = nltk.sent_tokenize(self.file_contents)
        for sentence in sentences:
            sentence = sentence.lstrip().rstrip()
            if sentence == "":
                continue

            tokenizer = RegexpTokenizer(r"\w+")
            tokens = tokenizer.tokenize(sentence)
            # [('mary', 'NN'), ('now', 'RB'), ('loves', 'VBZ'), ('red', 'JJ')]
            # [('fred', 'VBN'), ('sees', 'NNS'), ('mary', 'JJ'), ('sometimes', 'RB')]
            # [('mary', 'JJ'), ('likes', 'NNS'), ('red', 'VBD')]
            # [('ted', 'VBN'), ('now', 'RB'), ('likes', 'VBZ'), ('green', 'JJ')]
            tokenized_text = nltk.pos_tag(tokens)
            
            # TODO - Add the parts of sentence tags here!
            try:
                tree_string = self.parser.simple_parse(sentence)
                sentence_tree = nltk.Tree.fromstring(tree_string)
                for sub_tree in sentence_tree.subtrees():
                    if sub_tree.label() in self.part_of_sentence_labels:
                        token = (" ".join(sub_tree.leaves()), sub_tree.label())
                        self.tokenized_text.append(token)            
                self.tokens.extend(tokens)
            except IndexError:
                pass
            
            # Not sure if we need the start tokens in there yet.
            # self.tokenized_text.append((ut.START, ut.START))
            self.tokenized_text.extend(tokenized_text)
            self.tokenized_text.append((ut.END, ut.END))
            
            # Count first word pos into initial probabilities
            if len(self.tokenized_text) > 0:
                first_word_key_list = []
                for _ in range(self.markov_order-1):
                    first_word_key_list.append(ut.START)
                # first part of speech
                try:
                    first_word_key_list.append(tokenized_text[0][1])
                except IndexError:
                    pass
                # First part of sentence (should probably add to the other function for part of sentence..)
                try:
                    first_word_key_list.append(self.tokenized_text[0][1])
                except IndexError:
                    pass

                # Need to figure out why tuple and set default..Maybe text can be multiple? idk
                #       I think this is there if the markov order > 1
                if self.markov_order == 1:
                    for word in first_word_key_list:
                        self.initial_probs.setdefault(word, 0.0)
                        self.initial_probs[word] += 1.0
                # Not sure here yet, but this doesn't work for part of speech and part of sentence..
                else:
                    first_word_key = tuple(first_word_key_list)
                    self.initial_probs.setdefault(first_word_key, 0.0)
                    self.initial_probs[first_word_key] += 1.0
    
    def create_pos_dictionaries(self) -> None:
        """
        Iterates through the tokens and draws out their parts of speech
            into dictionaries, that can be used later
        :return: None
        """
        for token in self.tokenized_text:
            if token[0] is ut.END:
                continue
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
        #
        #     transition_probs = {"DT": {"NN": 1.0, "DT": 0.0, "NNS": 0.0},
        #                  "NN": {"NN": 0.1, "DT": 0.2, "NNS": 0.7},
        #                  "NNS": {"NN": 0.4, "DT": 0.5, "NNS": 0.1}}

        # We look at the transitions between a current token and the previous
        #   token. Then we add that transition to the transition dictionary
        skip_token = True
        previous_token = (ut.END, ut.END)
        for i in range(len(self.tokenized_text)):
            token = self.tokenized_text[i]
            if token[1] not in self.parts_of_speech and not ut.END:
                self.parts_of_speech.append(token[1])

            if token[0] is ut.END or previous_token[0] is ut.END:
                skip_token = True
            # If first token or end of sentence, we set previous token then skip to the next token
            if skip_token:
                previous_token = token
                skip_token = False
            # If not first token, get the keys, add them to the transition dict
            else:
                previous_key = self.__get_hidden_state(i-1)
                current_key = self.__get_hidden_state(i)

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

    def __get_hidden_state(self, token_position) -> list:
        """
        Finds the hidden state given the markov order of the model
        """
        hidden_state = []
        is_start_token = False  # True if before first token of sequence
        for i in range(self.markov_order):
            # Check if the lookback should be (and continue to be) a start token
            if token_position-i < 0:
                is_start_token = True
            elif self.tokenized_text[token_position-i][1] is ut.END:
                is_start_token = True

            if is_start_token:
                hidden_state.append(ut.START)
            else:
                hidden_state.append(self.tokenized_text[token_position-i][1])

        hidden_state.reverse()
        return tuple(hidden_state) # cast list as a tuple to make hashable
