from constraints.Constraint import Constraint
import pronouncing


class ConstraintRhymesWith(Constraint):
    """
    TODO - I used a package that I found online for this, but a better solution
        is probably needed as I'm sure this isn't perfect.
    """
    rhymes = []
    must_rhyme = True

    def __init__(self, word: str, must_rhyme: bool):
        """

        :param word:
        :param must_rhyme:
        """
        Constraint.__init__(self)
        self.rhymes = pronouncing.rhymes(word)
        self.must_rhyme = must_rhyme

    def is_satisfied_by_state(self, word: str) -> bool:
        if word.lower() in self.rhymes:
            return True
        else:
            return False
