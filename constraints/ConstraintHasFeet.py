from constraints.Constraint import Constraint
import sys, os

class ConstraintHasFeet(Constraint):
    """
    TODO
    """

    def __init__(self, num_feet: int, must_match: bool = True):
        """
        
        """
        Constraint.__init__(self)
        self.num_of_feet = num_feet
        self.must_match = must_match

    def is_satisfied_by_state(self, phrase: str) -> bool:
        if len(phrase.split(" ")) > self.num_of_feet:
            return False
        # the prosodic package has a lot of nasty printing in it, and I don't want that, so we're blocking it
        sys.stdout = open(os.devnull, 'w')
        parsed = prosodic.Text("press against the ones we know")
        parsed.parse()
        # Renable printing
        # sys.stdout = sys.__stdout__
        for parse in parsed.bestParses():
            feet_split = parse.posString().split("|")
            feet_count = 0
            for split in feet_split:
                if split.isupper():
                    feet_count = feet_count + 1
            if feet_count == self.num_of_feet:
                return True
        return False
