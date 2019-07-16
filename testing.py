# from utility.SendEmail import SendEmail
#
# email = SendEmail("Let's try out another test! I think this will go great!")
# email.send_email()
# from string import ascii_lowercase
# for c in ascii_lowercase:
#     print(c)
from utility.CountSentences import CountSentences
test = CountSentences("data/test.txt")
test.shuffle_sentences(1)
# print(test.num_sentences)
# print(test.get_sentences(10))
print(test.sentence_list_as_string(test.get_sentences(10)))
