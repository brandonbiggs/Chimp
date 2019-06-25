import numpy as np
words = 6
x = np.arange(words*words)
x.shape = (words,words)
print(x)
# x = np.ones_like(x)
# print(x)
print(x[:,0])