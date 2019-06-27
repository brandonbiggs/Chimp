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
print(type(words_from_file))
# return words_from_file