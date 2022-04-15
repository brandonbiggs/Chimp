from constraints.Constraint import Constraint
import nltk
#try:
#    nltk.data.find("~/nltk_data/tokenizers/punkt")
#except LookupError:
#    nltk.download('cmudict', quiet=True)
from nltk.corpus import cmudict


class ConstraintContainsSyllables(Constraint):
    """

    """

    def __init__(self, num_of_syllables: int):
        """

        :param word:
        :param must_rhyme:
        """
        Constraint.__init__(self)
        self.num_of_syllables = num_of_syllables
        self.cmu_dict = cmudict.dict()
        

    def is_satisfied_by_state(self, phrase: str) -> bool:
        num_of_syllables = 0
        for word in phrase.split(" "):
            word = word.lower()
            try:
                num_of_syllables = num_of_syllables + [len(list(y for y in x if y[-1].isdigit())) for x in self.cmu_dict[word]][0]
            except:
                return False
        if num_of_syllables == self.num_of_syllables:
            return True
        else: 
            return False
