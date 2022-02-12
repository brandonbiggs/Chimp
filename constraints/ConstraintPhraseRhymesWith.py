from constraints.Constraint import Constraint
import pronouncing


class ConstraintPhraseRhymesWith(Constraint):
    rhymes = []
    position_of_rhyme = 0
    must_rhyme = True

    def __init__(self, word: str, position_of_rhyme: int = -1, must_rhyme: bool = True):
        """

        :param word:
        :param must_rhyme:
        """
        Constraint.__init__(self)
        self.rhymes = pronouncing.rhymes(word)
        self.must_rhyme = must_rhyme
        self.position_of_rhyme = position_of_rhyme

    def is_satisfied_by_state(self, phrase: str) -> bool:
        word = phrase.split(" ")[self.position_of_rhyme]
        if word.lower() in self.rhymes:
            return True
        else:
            return False
