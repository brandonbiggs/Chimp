import utility.Utility as util
from progress.bar import Bar
import re


class ProcessDataForMM:
    file_name = ""
    file_contents = ""
    hidden_nodes = []
    observed_nodes = []
    emission_probs = {}
    first_word_of_sentence = []
    initial_probs = {}

    transition_probs = {}

    def __init__(self, file_name: str, progress_bar=True) -> None:
        """

        :param file_name:
        :param progress_bar:
        """
        # if progress_bar:
        #     self.__init_with_progress(file_name)
        # else:
        #     self.__init_without_progress_bar(file_name)
        self.__init_without_progress_bar(file_name)

    def __init_with_progress(self, file_name):
        self.file_name = file_name
        bar = Bar('Processing', max=6)
        self.file_contents = util.read_text_file(self.file_name)
        bar.next()
        bar.finish()

    def __init_without_progress_bar(self, file_name):
        self.file_name = file_name
        self.file_contents = util.read_text_file(self.file_name)
        self.__step_through_sentences()
        self.__setup_initial_probability()
        self.__setup_emission_probabilities()
        self.__setup_transition_probabilities()

    def __step_through_sentences(self):
        sentences = self.file_contents.split(".")
        for sentence in sentences:
            sentence = sentence.lstrip().rstrip()
            # Gets rid of any words that are empty.
            if sentence == "":
                continue
            words = sentence.split(" ")
            # Setup for the initial probabilities
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
        # print("Transition Probs:", self.transition_probs)
        for key, value in self.transition_probs.items():
            if len(value) > 1:
                total = 0
                for sub_key, sub_value in value.items():
                    total += sub_value
                for sub_key, sub_value in value.items():
                    # print("Sub Value:", sub_value, "Sub key:", sub_key)
                    # print(self.transition_probs.get(key))
                    self.transition_probs.get(key)[sub_key] = sub_value/total
            # print("Key:", key, "Value:", value)

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