from constraints.Constraint import Constraint

STOP_WORDS = [ "ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than" ]

class ConstraintStopWord(Constraint):
    """

    """

    __must_be_stopword = False

    def __init__(self, must_be_stopword: bool):
        """
        :param must_be_stopword: If False, then the constrained word must not be a stopword
        """
        Constraint.__init__(self)
        self.__must_be_stopword = must_be_stopword

    def is_satisfied_by_state(self, word: str) -> bool:
        """

        :param word:
        :return: bool
        """
        if self.__must_be_stopword:
            return word in STOP_WORDS
        else:
            return word not in STOP_WORDS

    def print(self):
        print("Must be stop word:", self.__must_be_stopword)
