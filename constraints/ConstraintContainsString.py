from constraints.Constraint import Constraint


class ConstraintContainsString(Constraint):
    """

    """

    constraint = ""
    must_contain = ""

    def __init__(self, string: str, must_contain: bool):
        """

        :param string: string we are using to constrain
        :param must_contain: This is the concept of "match this" or "match the opposite of this"
            True means that if the word has the given string, it will be satisfied
            False means that if the word does NOT have the given string, it will be satisfied
        """
        Constraint.__init__(self)
        self.constraint = string
        self.must_contain = must_contain

    def is_satisfied_by_state(self, word: str) -> bool:
        """

        :param word:
        :return: bool
        """
        if self.must_contain:
            if self.constraint in word:
                return True
            else:
                return False
        else:
            if self.constraint not in word:
                return True
            else:
                return False

    def print(self):
        print("Constraint String:", self.constraint)
        print("Must contain? ", self.must_contain)
