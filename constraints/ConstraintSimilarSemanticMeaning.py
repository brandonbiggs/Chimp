from constraints.Constraint import Constraint
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim.downloader as api
import nltk

class ConstraintSimilarSemanticMeaning(Constraint):
    """
    
    """

    def __init__(self, 
            model: str = "glove-twitter-25", 
            similarity_threshhold: float = 0.5, 
            theme: str = "weather",
            verbose: bool = False):
        """_summary_

        Args:
            model (str, optional): _description_. Defaults to "glove-twitter-25".
            similarity_threshhold (float, optional): _description_. Defaults to 0.5.
            theme (str, optional): _description_. Defaults to "weather".
            verbose (bool, optional): _description_. Defaults to False.
        """
        Constraint.__init__(self)
        self.model = api.load(model)
        self.similarity_threshhold = similarity_threshhold
        self.theme = theme
        self.verbose = verbose
        # https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk
        self.acceptable_pos = [
            "JJ", # adjective or numeral, ordinal
            "NN", # noun, common, singular or mass
            "NNP", # noun, proper, singular
            "NNS", # noun, common, plural
            "VB", # verb, base form
            "VBZ", # verb, past tense
            "VBG", # verb, present participle or gerund
            "VBN", # verb, past participle
            "VBP", # verb, present tense, not 3rd person singular
            "VBZ", #  verb, present tense, 3rd person singular
        ]

    def is_satisfied_by_state(self, phrase: str) -> bool:
        for word in phrase.split(" "):
            word = word.lower()
            try:
                if self.__get_string_pos(word) in self.acceptable_pos:
                    similarity = self.model.similarity(word, self.theme)
                    if similarity >= self.similarity_threshhold:
                        if self.verbose:
                            print(f"Similarity between {self.theme} and {word} is: {similarity}")
                        return True
            except KeyError:
                pass
        return False

    @staticmethod
    def __get_string_pos(word: str) -> str:
        # Uses NLTK to get the part of speech of the word
        word = word.strip()
        token = nltk.word_tokenize(word)
        part_of_speech = nltk.pos_tag(token)[0][1]
        return str(part_of_speech)
