import utility.Utility
import random


class CountSentences:

    def __init__(self, text_file):
        file = utility.Utility.read_text_file(text_file)
        filtered = filter(None, file.split("."))
        self.num_sentences = 0
        self.sentences = []
        self.sentences = list(filtered)
        self.num_sentences = len(self.sentences)

    def shuffle_sentences(self, amount_of_shuffles=1) -> None:
        for i in range(amount_of_shuffles):
            random.shuffle(self.sentences)

    def get_sentences(self, number_to_get: int) -> list:
        if number_to_get > self.num_sentences:
            raise Exception("The number of requested sentences do not exist. Please choose"
                            "a smaller number of sentences or load in a bigger file.")
        else:
            return self.sentences[:number_to_get]

    @staticmethod
    def sentence_list_as_string(sentences):
        text = ""
        for sentence in sentences:
            text += sentence + ". "
        return text

