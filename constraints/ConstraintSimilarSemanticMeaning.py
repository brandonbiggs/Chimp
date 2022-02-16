from constraints.Constraint import Constraint

class ConstraintSimilarSemanticMeaning(Constraint):
    """
    
    """

    def __init__(self):
        """

        :param word:
        :param must_rhyme:
        """
        Constraint.__init__(self)
        

    def is_satisfied_by_state(self, word: str) -> bool:
        return True
