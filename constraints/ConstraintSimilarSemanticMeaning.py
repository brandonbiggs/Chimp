from constraints.Constraint import Constraint
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim.downloader as api
from gensim.models import Word2Vec
import nltk

class ConstraintSimilarSemanticMeaning(Constraint):
    """
    
    """

    def __init__(self, 
            model: str = "glove-twitter-25", 
            similarity_threshhold: float = 0.5, 
            theme: str = "weather",
            verbose: bool = False,
            position_of_theme: int = None):
        """_summary_

        Args:
            model (str, optional): _description_. Defaults to "glove-twitter-25".
            similarity_threshhold (float, optional): _description_. Defaults to 0.5.
            theme (str, optional): _description_. Defaults to "weather".
            verbose (bool, optional): _description_. Defaults to False.
        """
        Constraint.__init__(self)
        # self.model = api.load(model)
        # self.model = api.load("/home/biggbs/gensim-data/glove-twitter-25/glove-twitter-25.gz")
        self.model = model
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
        if position_of_theme is None:
            self.position_of_theme = None
        else:
            self.position_of_theme = position_of_theme

    def is_satisfied_by_state(self, phrase: str) -> bool:
        sentence = []
        if len(phrase.split(" ")) == 1:
            sentence.append(phrase)
        else:
            sentence = phrase.split(" ")
        if self.position_of_theme is not None:
            word = phrase[self.position_of_theme]
            similarity = self.model.similarity(word, self.theme)
            if similarity >= self.similarity_threshhold:
                if self.verbose:
                    print(f"Similarity between {self.theme} and {word} is: {similarity}")
                return True
        else:
            for word in sentence:
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
