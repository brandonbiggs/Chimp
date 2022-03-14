from constraints.ConstraintMatchesPoetryScheme import ConstraintMatchesPoetryScheme
import re
import pronouncing

scheme = ".?1.?.?1.?.?"
phrase = "there was an old man with a beard"
phrase_2 = "who said it was just as I feared"
phrase_3 = "have all built their nests in my beard"

phones_list = pronouncing.phones_for_word(phrase.split(" ")[-1])
stresses_string = pronouncing.stresses(phones_list[0])
stresses_string = stresses_string.replace("2", "1")
scheme = scheme + stresses_string
print(scheme)

test = ConstraintMatchesPoetryScheme(scheme, "beard")
print(test.is_satisfied_by_state(phrase_2))
print(test.is_satisfied_by_state(phrase_3))