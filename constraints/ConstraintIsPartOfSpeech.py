from constraints.Constraint import Constraint

import nltk

try:
    nltk.data.find("/home/biggbran/research/markovs/nltk_data/tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)

try:
    nltk.data.find(
        "/home/biggbran/research/markovs/nltk_data/taggers/averaged_perceptron_tagger"
    )
except LookupError:
    nltk.download("averaged_perceptron_tagger", quiet=True)


class ConstraintIsPartOfSpeech(Constraint):
    """
    TODO - Need to rethink how this is working. Not working correctly.
    """

    part_of_speech = ""
    must_be_pos = ""

    def __init__(self, part_of_speech: str, must_be_pos: bool):
        """

        :param part_of_speech: part of speech that we care about
        :param must_be_pos: This is the concept of "match this" or "match the opposite of this"
            True means that if the word is the given part of speech, it will be satisfied
            False means that if the word is not the given part of speech, it will be satisfied
        """
        Constraint.__init__(self)
        self.part_of_speech = part_of_speech
        self.must_be_pos = must_be_pos

    def is_satisfied_by_state(self, word: str) -> bool:
        """
        TODO - This may have to be altered in the future. Hidden nodes may not be
            parts of speech in the future?
        :param word:
        :return:
        """
        part_of_speech = word
        # part_of_speech = self.__get_string_pos(word)
        if self.must_be_pos:
            if str(part_of_speech) == str(self.part_of_speech):
                return True
            else:
                return False
        else:
            if str(part_of_speech) != str(self.part_of_speech):
                return True
            else:
                return False

    @staticmethod
    def __get_string_pos(word: str) -> str:
        # Uses NLTK to get the part of speech of the word
        word = word.strip()
        token = nltk.word_tokenize(word)
        part_of_speech = nltk.pos_tag(token)[0][1]
        return str(part_of_speech)

    def print(self):
        print("Constraint part of speech:", self.part_of_speech)
        print("String must be part of speech?", self.must_be_pos)
