from constraints.Constraint import Constraint


class ConstraintStartsWithLetter(Constraint):
    """

    """

    constraint = ""
    __must_start_with = ""
    __num_of_letters = 1

    def __init__(self, letters: str, must_start_with: bool, num_of_letters: int = 1):
        """

        :param letters: string we are using to constrain
        :param must_start_with: This is the concept of "match this" or "match the opposite of this"
            True means that if the word starts with given string, it will be satisfied
            False means that if the word does NOT start with the given string, it will be satisfied
        :param num_of_letters: The number of letters that must match at the beginning of a string
            If you want just the first letter to match, then use 1, otherwise use more.
        """
        Constraint.__init__(self)
        self.constraint = letters
        self.__must_start_with = must_start_with
        self.__num_of_letters = num_of_letters
        if len(letters) != num_of_letters:
            raise Exception(
                "The length of your string does not match the amount of letters "
                "that you want matched. Please ensure that the length of the string "
                "is the same size as the number of letters you want matched."
            )

    def is_satisfied_by_state(self, word: str) -> bool:
        """

        :param word:
        :return: bool
        """
        if self.__must_start_with:
            if self.constraint.lower() == word[0 : self.__num_of_letters].lower():
                return True
            else:
                return False
        else:
            if self.constraint.lower() != word[0 : self.__num_of_letters].lower():
                return True
            else:
                return False

    def print(self):
        print("Constraint String:", self.constraint)
        print("Must start with? ", self.__must_start_with)
        print("Number of letters to match:", self.__num_of_letters)
