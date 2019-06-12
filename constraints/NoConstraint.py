from constraints.Constraint import Constraint


class NoConstraint(Constraint):
    def __init__(self):
        Constraint.__init__(self)

    @staticmethod
    def is_satisfied_by_state(word: any) -> bool:
        return True
