from os import symlink
from constraints.Constraint import Constraint
import pronouncing
import re, string
import nltk
# try:
#     nltk.data.find("~/nltk_data/tokenizers/punkt")
# except LookupError:
#     nltk.download('cmudict', quiet=True)
from nltk.corpus import cmudict

class ConstraintMatchesPoetryScheme(Constraint):
    """
    Thinking of regex for stress patterns..
    typically a preposition shouldn't be a stressed word
    phrase doesn't have to have a min or max of 8 syllables
    any word that is a preposition and is single syllable, change it's stress to 0

    SP = sentence_phrase
    [x] if SP.syllables >= (7+rhymeword.syllables.count) or < 3 syllables, return False
    [x] if SP.lastword ! rhyme with rhyme word, return false
    if stresses.count < 3 return false (after disregarding single syllable prepositions)
    treat 1 and 2 stresses the same
    if SP.stress_pattern is ! subsequence of ?1??1??1?? > can be 0 or 1, return false 
    anything that comes after the 8th position has to match the rhyming word stress pattern
    Change ?1??1??1?? to ?1??1??1XX where the X are specific to the rhyming word
    """

    def __init__(self, stress_pattern: str, rhymeword: str, stresses: int, min_syllables: int = 6):
        """
        
        """
        Constraint.__init__(self)
        self.bad_pos = ["IN"]
        self.stress_pattern = re.compile(stress_pattern)
        self.cmu_dict = cmudict.dict()        
        self.rhymeword = rhymeword
        self.stresses = stresses
        self.min_syllables = min_syllables

    def is_satisfied_by_state(self, phrase: str) -> bool:
        phrase = re.sub(rf"[{string.punctuation}]", "", phrase)
        phrase_syllables = self.count_syllables(phrase)
        rhymeword_syllables = self.count_syllables(self.rhymeword)
        # if SP.syllables >= (7+rhymeword.syllables.count) or < 3 syllables, return False
        # print(f"phrase_syllables: {phrase_syllables}")
        if phrase_syllables > self.stresses + rhymeword_syllables or phrase_syllables < self.min_syllables:
            return False
        # if SP.lastword ! rhyme with rhyme word, return false
        # This is taken care of with the other constraint...

        # if stresses.count < 3 return false (after disregarding single syllable prepositions)
        #   treat 1 and 2 stresses the same
        num_stresses = self.count_stresses(phrase)
        if num_stresses is None:
            return False
        # print(f"num_stresses: {num_stresses}")
        if num_stresses < 3:
            return False

        # Get stress sequence for the entire phrase, disregarding single syllable prepositions
        stress_sequence = ""
        for word in phrase.split(" "):
            if self.count_syllables(word) > 1 or not self.check_for_preposition(word):
                new_stresses = self.get_stresses(word)
                if new_stresses is None:
                    return False
                stress_sequence = stress_sequence + new_stresses
            else:
                stress_sequence = stress_sequence + "0"
        # print(stress_sequence)

        # Check if it's a subsequence
        match = self.stress_pattern.match(stress_sequence)
        # print(f"is_subsequence: {match}")
        if match:
            return True
        else:
            return False

    def count_syllables(self, phrase: str) -> int:
        num_of_syllables = 0
        # print(f"phrase: {phrase}")
        for word in phrase.split(" "):
            word = word.lower()
            try:
                syllables = [len(list(y for y in x if y[-1].isdigit())) for x in self.cmu_dict[word]][0]
                # print(f"word: {word} syllables: {syllables}")
                num_of_syllables = num_of_syllables + syllables
            except:
                return 0
        return num_of_syllables

    def check_for_preposition(self, word: str) -> bool:
        tagged = nltk.pos_tag(word.split(" "))
        # print(tagged)
        if tagged[0][1] in self.bad_pos:
            # print(tagged[0][1])
            return True
        else:
            return False

    @staticmethod
    def get_stresses(word: str) -> int:
        try:
            phones_list = pronouncing.phones_for_word(word)
            stresses_string = pronouncing.stresses(phones_list[0])
            stresses_string = stresses_string.replace("2", "1")
            return stresses_string
        except:
            return None

    def count_stresses(self, phrase: str) -> int:
        count = 0
        for word in phrase.split(" "):
            if self.count_syllables(word) > 1 or not self.check_for_preposition(word):
                stress_string = self.get_stresses(word)
                if stress_string is None:
                    return None
                stress_count = stress_string.count("1")
                count += stress_count
        return count
