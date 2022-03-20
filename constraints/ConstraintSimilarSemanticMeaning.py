from constraints.Constraint import Constraint
from nltk.tokenize import sent_tokenize, word_tokenize
import gensim.downloader as api

class ConstraintSimilarSemanticMeaning(Constraint):
    """
    
    """

    def __init__(self, model: str = "glove-twitter-25", similarity_threshhold: float = 0.5, theme: str = "weather"):
        """

        :param word:
        :param must_rhyme:
        """
        Constraint.__init__(self)
        self.model = api.load(model)
        self.similarity_threshhold = similarity_threshhold
        self.theme = theme

    def is_satisfied_by_state(self, phrase: str) -> bool:
        for word in phrase.split(" "):
            word = word.lower()
            try:
                similarity = self.model.similarity(word, self.theme)
                if similarity >= self.similarity_threshhold:
                    print(f"Similarity between {self.theme} and {word} is: {similarity}")
                    return True
            except KeyError:
                pass
        return False
