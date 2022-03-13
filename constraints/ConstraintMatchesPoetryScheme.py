from constraints.Constraint import Constraint
import pronouncing
import re, string

class ConstraintMatchesPoetryScheme(Constraint):
    """
    Thinking of regex for stress patterns..
    typically a preposition shouldn't be a stressed word
    phrase doesn't have to have a min or max of 8 syllables
    any word that is a preposition and is single syllable, change it's stress to 0

    SP = sentence_phrase
    if SP.syllables >= (7+rhymeword.syllables.count) or < 3 syllables, return False
    if SP.lastword ! rhyme with rhyme word, return false
    if stresses.count < 3 return false (after disregarding single syllable prepositions)
    treat 1 and 2 stresses the same
    if SP.stress_pattern is ! subsequence of ?1??1??1?? > can be 0 or 1, return false 
    anything that comes after the 8th position has to match the rhyming word stress pattern
    Change ?1??1??1?? to ?1??1??1XX where the X are specific to the rhyming word
    """

    def __init__(self, must_match_stress_pattern: bool, check_stress_pattern: bool, stress_pattern: str, stress_pattern_position: int):
        """
        
        """
        Constraint.__init__(self)
        self.must_match = must_match_stress_pattern
        self.check_pattern = check_stress_pattern
        self.stress_pattern = stress_pattern
        self.stress_pattern_word_position = stress_pattern_position

    def is_satisfied_by_state(self, phrase: str) -> bool:
        phrase = re.sub(rf"[{string.punctuation}]", "", phrase)
        
        stress_pattern_dict = {}
        try:
            for word in phrase.split(" "):
                output = pronouncing.stresses(pronouncing.phones_for_word(word)[0])
                stress_pattern_dict[word] = output
        except:
            return False

        if self.must_match:
            matching_word = phrase.split(" ")[self.stress_pattern_word_position]
            matching_pattern = pronouncing.stresses(pronouncing.phones_for_word(matching_word)[0])
            # print(f"{self.stress_pattern} - {matching_pattern}")
            if matching_pattern != self.stress_pattern:
                return False
        if self.check_pattern:
            # print(stress_pattern_dict)
            previous_stress = None
            for key,value in stress_pattern_dict.items():
                if previous_stress is None:
                    previous_stress = value
                else:
                    if previous_stress == 0 and value == 0:
                        return False
        return True
