import pronouncing

# sentence = "and they might have gone on growing" # should be 3
# sentence = "All the things we hide in water" # should be 4
# sentence = "press against the ones we know" # should be 4
# sentence = "if music be the food of love play on" # should be 5
sentence = "there once was a man from nantucket"

# There once was a man from Nantucket
# Who kept all his cash in a bucket.
#     But his daughter, named Nan,
#     Ran away with a man
# And as for the bucket, Nantucket.
print(sentence)
# constraint = ConstraintMatchesPoetryScheme()
# print(f"Foot count: {count_feet(feet)}")

# word = "if music"
# print(pronouncing.stresses(pronouncing.phones_for_word(word)[0]))
            
# Chimp 1.0
# length 13 phrase has 3 syllables, middle one has to be stressed

# Chimp 2.0
# Other option
# model of length 5
# sentence phrase that has 
# 1. observed state no more than 8/9 syllables that have to be a certain pattern. 
#   At least 3 stressed syllables and can't have 2 unstressed between any pairs
# 2. Still have to rhyme in AABBA
# 3. The word we rhyme with determines how many syllables. If last word has only a stressed syllable, limited to 8 syllables
#  the last foot has to have the same stress pattern as whatever you're rhyming with

#  Take the nantucket limerick and work backwards then try to generalize