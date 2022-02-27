from constraints.Constraint import Constraint

class ConstraintPhraseEndsWithString(Constraint):
    """
    TODO
    """

    def __init__(self, string: str, must_contain: bool = True):
        """
        :param string: string we are using to constrain
        :param must_contain: This is the concept of "match this" or "match the opposite of this"
            True means that if the word is the given string, it will be satisfied
            False means that if the word does NOT match the given string, it will be satisfied
        """
        Constraint.__init__(self)
        self.constraint = string
        self.must_contain = must_contain

    def is_satisfied_by_state(self, phrase: str) -> bool:
        word = phrase.split(" ")[-1]
        if word.casefold() == self.constraint.casefold():
            return True
        else:
            return False
