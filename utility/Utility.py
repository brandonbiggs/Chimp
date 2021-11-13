import random
import re

START = '<<START>>'
END = '<<END>>'

def get_rand_num(first: int = 0, second: int = 1) -> float:
    """By default returns a number between 0 and 1
    Wanted to put this in it's own function in case we decide to change
    how randoms are created in the future.

    Returns:
        [type]: Number between first and second provided numbers
    """
    return random.uniform(first, second)

def array_average(array: list) -> float:
    total = 0
    for value in array:
        total += value
    return total / len(array)


def remove_pos_tags(sentence: str) -> str:
    new_sentence = ''
    words = sentence.split(' ')
    for word in words:
        word_split = word.split(':')
        if len(word_split) > 0:
            new_sentence += word_split[0] + ' '

    return new_sentence.rstrip()

# TODO - Probably need to refactor this
def read_text_file(file_name: str) -> str:
    """
    Reads the text file
    :return: file contents
    """
    file = open(file_name, "r")
    text = file.read()
    file.close()

    newstring = ""
    text = re.sub(r" (?='|\.|\,|\?| |\!)", "", text)
    text = re.sub(r"(<p>)", "", text)

    word = ""
    for character in text.lower():
        if character not in '?!.\ ;\n"<>[]@#$%^&*()-_+={}/\\' and not character.isdigit():
            word += character
        elif character == "?" or character == "!" or character == ".":
            word += "."
        elif character == " ":
            # Check if word isn't a random single character
            if len(word) <= 1:
                if word == "a" or word == "i":
                    newstring += word + " "
                if word == "." or word == ",":
                    newstring += word
            else:
                newstring += word + " "

            word = ""
    newstring += word
            
    return newstring
