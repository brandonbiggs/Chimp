# TODO - Annotate a result with the parts of speech
# How sentences phrases allow constraints to be met by the entire phrase

# from constraints.ConstraintMatchesPoetryScheme import ConstraintMatchesPoetryScheme
# import re
# import string
# import pronouncing

# scheme = ".?1.?.?1.?.?"
# phrase = "there was an old man with a beard"
# phrase_2 = "slight as a plucked string"
# # phrase_3 = "have all built their nests in my beard"

# scheme_a = ".?1.?.?1.?.?"
# scheme_b = ".?1.?.?"
# rhyme_a = "lake"
# rhyme_b = "ring"

# phones_list = pronouncing.phones_for_word(rhyme_b)
# stresses_string = pronouncing.stresses(phones_list[0])
# stresses_string = stresses_string.replace("2", "1")
# scheme_b = scheme_b + stresses_string

# test = ConstraintMatchesPoetryScheme(scheme_b, rhyme_b, 4, min_syllables=3)
# # print(test.is_satisfied_by_state(phrase_2))
# # print(test.is_satisfied_by_state(phrase_3))

# stress_sequence = "^.?1.?.?1$"
# stress_pattern = "10011"
# stress_pattern = re.compile(stress_pattern)
# print(stress_pattern.match(stress_sequence))

import gensim.downloader as api
model = api.load("glove-twitter-25")
print(model.most_similar("cat"))
print(model.similarity('france', 'spain'))

# from gensim.models import Word2Vec
# model = Word2Vec.load("/Users/biggbs/gensim-data/glove-twitter-25/glove-twitter-25.gz")
# model.wv.similarity('france', 'spain')
