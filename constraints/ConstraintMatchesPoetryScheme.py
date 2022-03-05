from constraints.Constraint import Constraint
import pronouncing
import re, string

class ConstraintMatchesPoetryScheme(Constraint):
    """
    TODO
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
