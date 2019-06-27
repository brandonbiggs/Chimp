# import numpy as np
# words = 6
# x = np.arange(words*words)
# x.shape = (words,words)
# print(x)
# # x = np.ones_like(x)
# # print(x)
# print(x[:,0])

file = open("data/book_tiny.txt", "r")
words_from_file = file.read()
file.close()
newstring = ""
for character in words_from_file:
    if character not in ";\n":
        newstring += character
    else:
        newstring += " "
print(words_from_file)
print(newstring)
# return words_from_file

# from constraints.ConstraintStartsWithLetter import *
# test = ConstraintStartsWithLetter("ta", True, 2)
# print(test.is_satisfied_by_state("taeapple"))
# word = "hello"
# print(word[0:2])
