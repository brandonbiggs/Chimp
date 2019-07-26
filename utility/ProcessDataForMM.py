import utility.Utility
from progress.bar import Bar
import utility.CountSentences as countSentences


class ProcessDataForMM:

    def __init__(self, file_name: str, number_of_sentences, progress_bar = True, initial_prob_extensive = True,
                 file_contents_bool=False) -> \
            None:
        """

        :param file_name:
        :param number_of_sentences:
        :param progress_bar:
        :param initial_prob_extensive: True means use only the first word of the sentence to
            set the initial probabilities. False means use all words except last word of
            sentence for initial probabilities
        :param file_contents: If this is set to true, file is not the name of a file,
            but it's actually the contents of a file. The purpose of this is to make sure
            chimp and markov model are using the same exact sentences. Verbose and text_contents
            should not both be set to True
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
        # if progress_bar:
        #     self.__init_with_progress(file_name)
        # else:
        #     self.__init_without_progress_bar(file_name)
        self.__init_without_progress_bar(file_name, file_contents_bool)

    def __init_with_progress(self, file_name):
        self.file_name = file_name
        bar = Bar('Processing', max=6)
        # self.file_contents = util.read_text_file(self.file_name)
        contents = countSentences.CountSentences(self.file_name)
        contents.shuffle_sentences(10)
        self.file_contents = \
            contents.sentence_list_as_string(contents.get_sentences(self.number_of_sentences))

        bar.next()
        bar.finish()

    def __init_without_progress_bar(self, file_name, file_contents_bool):
        self.file_name = file_name
        # self.file_contents = util.read_text_file(self.file_name)
        if file_contents_bool:
            self.file_contents = self.file_name
        else:
            contents = countSentences.CountSentences(self.file_name)
            contents.shuffle_sentences(10)
            self.file_contents = \
                contents.sentence_list_as_string(contents.get_sentences(self.number_of_sentences))

        self.__step_through_sentences()
        self.__setup_initial_probability()
        self.__setup_emission_probabilities()
        self.__setup_transition_probabilities()

    def __step_through_sentences(self):
        """

        :return:
        """
        sentences = self.file_contents.split(".")
        for sentence in sentences:
            sentence = sentence.lstrip().rstrip()
            # Gets rid of any words that are empty.
            if sentence == "":
                continue
            words = sentence.split(" ")

            # Setup for the initial probabilities as the first word of the sentence
            if self.initial_prob_extensive:
                self.first_word_of_sentence.append(words[0])

            # Iterate over each word in the sentence
            for word in words:
                # Start the checking for setting up the transition probabilities
                # If the word has not been added to the transition probabilities, add it
                if not self.transition_probs.get(word):
                    # Check to see if the word is the last word in the list, if it is
                    #   add the word to the dictionary, but give it an empty value
                    if word == words[-1]:
                        self.transition_probs.update({word: {}})
                    # If the word isn't the last word, get the next word and add it to
                    #   the value of the previous dictionary
                    else:
                        # Adds all words except last word of sentence to initial probs
                        if not self.initial_prob_extensive:
                            self.first_word_of_sentence.append(word)
                        next_word_index = words.index(word) + 1
                        next_word = words[next_word_index]
                        self.transition_probs.update({word: {next_word: 1.0}})
                # If the word has been added to the transition probabilities, we need
                # to update it's score, unless it's still the last word.
                else:
                    # If it's not the last word, we'll update it. Otherwise move on
                    if word != words[-1]:
                        next_word_index = words.index(word) + 1
                        next_word = words[next_word_index]
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
                            self.transition_probs.get(word).update({next_word: (current_score+1)})
                        # Test case on our text didn't get to this point, but it might with a bigger
                        #   text
                        # else:
                        #     print("BUG ProcessDataForMM.py DEBUG:", word)
                        #     print(self.transition_probs.get(word))

                # Add the unique word to the hidden nodes list.
                if word not in self.hidden_nodes:
                    self.hidden_nodes.append(word)

        self.observed_nodes = self.hidden_nodes

    def __setup_transition_probabilities(self):
        for key, value in self.transition_probs.items():
            if len(value) > 1:
                total = 0
                for sub_key, sub_value in value.items():
                    total += sub_value
                for sub_key, sub_value in value.items():
                    self.transition_probs.get(key)[sub_key] = sub_value/total

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
            if not self.initial_probs.get(word):
                percent = self.first_word_of_sentence.count(word)/len(self.first_word_of_sentence)
                self.initial_probs.update({word: percent})

    def debug_print(self):
        print("Hidden nodes:")
        print(self.hidden_nodes)
        print("Initial probs:", self.initial_probs)
        print("Emission Probability")
        print(self.emission_probs)