from constraints.Constraint import Constraint

STOP_WORDS = [ "ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than" ]

class ConstraintStopWord(Constraint):
    """

    """

    __must_be_stopword = False
    __is_using_pos_tags = False

    def __init__(self, must_be_stopword: bool, is_using_pos_tags: bool):
        """
        :param must_be_stopword: If False, then the constrained word must not be a stopword
        :param is_using_pos_tags: words are tagged with POS (e.g. 'word:NN')
        """
        Constraint.__init__(self)
        self.__must_be_stopword = must_be_stopword
        self.__is_using_pos_tags = is_using_pos_tags

    def is_satisfied_by_state(self, word: str) -> bool:
        """

        :param word:
        :return: bool
        """
        if not self.__is_using_pos_tags:
            if self.__must_be_stopword:
                return word in STOP_WORDS
            else:
                return word not in STOP_WORDS
        else:
            if self.__must_be_stopword:
                return word.split(':')[0] in STOP_WORDS
            else:
                return word.split(':')[0] not in STOP_WORDS


    def print(self):
        print("Must be stop word:", self.__must_be_stopword)
