import random
import re
import pickle

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
    return text

def cleanup_text_file(text: str) -> str:
    newstring = ""
    text = re.sub(r" (?='|\.|\,|\?| |\!)", "", text)
    text = re.sub(r"(<p>)", "", text)

    word = ""
    
    for character in text:
        # if character not in '?!.\ ;\n"<>[]@#$%^&*()-_+={}/\\' and not character.isdigit():
        if character not in '\ ;\n"<>[]@#$%^&*()-_+={}/\\':
            word += character
        elif character == " ":
            # Check if word isn't a random single character
            #       Sometimes the text gets very messy and is just random letters. This checks for that
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

def pickle_model(pickle_file: str, model, verbose:str = False,):
    with open(pickle_file, "wb") as handle:
        pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if verbose:
        print("Finished training. Saved model to pickle file.")