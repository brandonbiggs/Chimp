import nltk
from nltk.tokenize import WhitespaceTokenizer
import utility.Utility as ut
from progress.bar import Bar
import utility.CountSentences as countSentences


class TrainMarkovModel:
    def __init__(self, file_name: str, number_of_sentences: int, initial_prob_extensive: bool = True,
        file_contents_bool: bool = False, should_tag_pos: bool = False, markov_order: int = 1,) -> None:
        """[summary]

        Args:
            file_name (str): [description]
            number_of_sentences (int): [description]
            initial_prob_extensive (bool, optional): True means use only the first word of the sentence to
                set the initial probabilities. False means use all words except last word of
                sentence for initial probabilities. Defaults to True.
            file_contents_bool (bool, optional): If this is set to true, file is not the name of a file,
                but it's actually the contents of a file. The purpose of this is to make sure
                chimp and markov model are using the same exact sentences. Verbose and text_contents
                should not both be set to True. Defaults to False.
            should_tag_pos (bool, optional): [description]. Defaults to False.
            markov_order (int, optional): [description]. Defaults to 1.
        """

        self.file_name = ""
        self.file_contents = ""
        self.hidden_nodes = []
        self.observed_nodes = []
        self.emission_probs = {}
        self.first_word_of_sentence = []
        self.initial_probs = {}

        self.transition_probs = {}
        self.initial_prob_extensive = initial_prob_extensive
        self.number_of_sentences = number_of_sentences
        self.markov_order = markov_order
        self.file_name = file_name

        if file_contents_bool:
            self.file_contents = self.file_name
        else:
            contents = countSentences.CountSentences(self.file_name)
            contents.shuffle_sentences(10)
            self.file_contents = contents.sentence_list_as_string(
                contents.get_sentences(self.number_of_sentences)
            )

        self.__step_through_sentences(should_tag_pos)
        self.__setup_initial_probability()
        self.__setup_emission_probabilities()
        self.__setup_transition_probabilities()

    def __step_through_sentences(self, should_tag_pos: bool):
        """[summary]

        Args:
            should_tag_pos (bool): bool to tag pos to string or not
        """
        sentences = self.file_contents.split(".")
        for sentence in sentences:
            sentence = sentence.lstrip().rstrip()
            # Gets rid of any words that are empty.
            if sentence == "":
                continue
            
            if should_tag_pos:
                tokenizer = WhitespaceTokenizer()
                tokens = tokenizer.tokenize(sentence)
                tokenized_text = nltk.pos_tag(tokens)

                words = [token[0] + ':' + token[1] for token in tokenized_text]
            else:
                words = sentence.split(" ")

            # Setup for the initial probabilities as the first word of the sentence
            if self.initial_prob_extensive and len(words) > 0:
                self.first_word_of_sentence.append(words[0])

            # Iterate over each word in the sentence
            for i in range(len(words)):
                word = self.__get_hidden_state(words, i)

                # Start the checking for setting up the transition probabilities
                # If the word has not been added to the transition probabilities, add it
                if not self.transition_probs.get(word):
                    # If the word isn't the last word, get the next word and add it to
                    #   the value of the previous dictionary
                    if not words[i] == words[-1]:
                        # Adds all words except last word of sentence to initial probs
                        if not self.initial_prob_extensive:
                            # TODO - Making some changes here...
                            # self.first_word_of_sentence.append(word)
                            self.first_word_of_sentence.append(word[0])

                        next_word = self.__get_hidden_state(words, i+1)
                        self.transition_probs.update({word: {next_word: 1.0}})
                # If the word has been added to the transition probabilities, we need
                # to update it's score, unless it's still the last word.
                else:
                    # If it's not the last word, we'll update it. Otherwise move on
                    if i != len(words)-1:
                        next_word = self.__get_hidden_state(words, i+1)
                        # Check the current value of the dictionary value for the next word
                        current_score = self.transition_probs.get(word).get(next_word)
                        # If the value is None, that means it's an empty dictionary for the key
                        #   We'll add the next word to it and give it a value of one, because
                        #   this is the first time it has shown up.
                        if current_score is None:
                            self.transition_probs.get(word).update({next_word: 1.0})
                        # If it's shown up before, we want to add one to it's current score as this will
                        #   help us create the probabilities later
                        else:
                            self.transition_probs.get(word).update(
                                {next_word: (current_score + 1)}
                            )
                        # Test case on our text didn't get to this point, but it might with a bigger
                        #   text
                        # else:
                            # print("BUG ProcessDataForMM.py DEBUG:", word)
                            # print(self.transition_probs.get(word))

                # Add the unique word to the hidden nodes list.
                if words[i] not in self.hidden_nodes:
                    self.hidden_nodes.append(words[i])

        self.observed_nodes = self.hidden_nodes

    def __setup_transition_probabilities(self):
        for key, value in self.transition_probs.items():
            if len(value) > 1:
                total = 0
                for sub_key, sub_value in value.items():
                    total += sub_value
                for sub_key, sub_value in value.items():
                    self.transition_probs.get(key)[sub_key] = sub_value / total

    def __setup_emission_probabilities(self):
        """
        Emission probabilities are every node going to themselves
        :return:
        """
        for word in self.hidden_nodes:
            self.emission_probs.update({word: {word: 1.0}})

    def __setup_initial_probability(self):
        """
        This will use self.first_word_of_sentence to create probabilities

        :return:
        """
        for word in self.first_word_of_sentence:
            first_word_key_list = []
            for _ in range(self.markov_order-1):
                first_word_key_list.append(ut.START)
            first_word_key_list.append(word)
            # TODO - check this
            # first_word_key = tuple(first_word_key_list)
            first_word_key = word

            if not self.initial_probs.get(first_word_key):

                percent = self.first_word_of_sentence.count(word) / len(
                    self.first_word_of_sentence
                )
                self.initial_probs.update({first_word_key: percent})

    def __get_hidden_state(self, tokens, token_position):
        """
        Finds the hidden state given the markov order of the model
        """
        hidden_state = []
        i = token_position
        for j in range(self.markov_order-1, -1, -1):
            if i-j < 0:
                hidden_state.append(ut.START)
            else:
                hidden_state.append(tokens[i-j])

        # return hidden_state
        return tuple(hidden_state) # cast list as a tuple to make hashable

    def debug_print(self):
        print("Hidden nodes:")
        print(self.hidden_nodes)
        print("Initial probs:", self.initial_probs)
        print("Emission Probability")
        print(self.emission_probs)
