import utility.Utility as ut
import random
import re


class CountSentences:
    def __init__(self, text_file: str) -> None:
        """[summary]

        Args:
            text_file (str): path to text file
        """
        file = ut.read_text_file(text_file)
        text = ut.cleanup_text_file(file)
        self.num_sentences = 0
        self.sentences = re.split("\.|\?|\!", text)
        
        # Remove empty strings
        self.sentences = [i for i in self.sentences if i]
        
        self.num_sentences = len(self.sentences)

    def shuffle_sentences(self, amount_of_shuffles: int = 1) -> None:
        for _ in range(amount_of_shuffles):
            random.shuffle(self.sentences)

    def get_sentences(self, number_to_get: int) -> list:
        if number_to_get > self.num_sentences:
            raise Exception(
                "The number of requested sentences do not exist. Please choose"
                "a smaller number of sentences or load in a bigger file."
            )
        else:
            return self.sentences[:number_to_get]

    @staticmethod
    def sentence_list_as_string(sentences):
        text = ""
        for sentence in sentences:
            text += sentence + ". "
        return text
