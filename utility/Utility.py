import random
import pickle
from utility.ProcessDataForChimp import ProcessDataForChimp
from utility.ProcessDataForMM import ProcessDataForMM
from markovs.HiddenMarkovModel import HiddenMarkovModel
import re


def get_rand_num(first=0, second=1):
    # TODO - Replace with numpy random
    """
    By default returns a number between 0 and 1
    Wanted to put this in it's own function in case we decide to change
    how randoms are created in the future.
    :param first:
    :param second:
    :return: Number between first and second provided numbers
    """
    return random.uniform(first, second)


def train(
    number_of_sentences: int,
    text_file="data/book_tiny.txt",
    pickle_file="pickle_files/new_file.pickle",
    model="chimp",
    verbose=True,
    text_contents=False,
) -> None:
    """
    Create the hidden markov model and store it for use later
    :param number_of_sentences
    :param text_file:
    :param pickle_file:
    :param model:
    :param verbose:
    :param text_contents: If this is set to true, text file is not the name of a file,
        but it's actually the contents of a file. The purpose of this is to make sure
        chimp and markov model are using the same exact sentences. Verbose and text_contents
        should not both be set to True
    :return: None
    """
    if verbose and not text_contents:
        print("Starting training on:", text_file)
    pickle_file_name = pickle_file
    if pickle_file_name == "" and verbose:
        print("No name provided. Going with the default: ", pickle_file)
    else:
        # pickle_file_name = pickle_file_name.strip()
        # pickle_file = "pickle_files/" + pickle_file_name + ".pickle"
        if verbose:
            print("Your file will be saved to: ", pickle_file)
    # Process the text file
    if model == "chimp":
        data = ProcessDataForChimp(
            text_file, number_of_sentences, False, file_contents=text_contents
        )
    elif model == "markovmodel":
        data = ProcessDataForMM(
            text_file, number_of_sentences, False, file_contents_bool=text_contents
        )
    else:
        raise Exception("Unknown model. Please use either 'chimp' or 'markovmodel'")

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(data.hidden_nodes, data.observed_nodes)
    hidden_markov_model.initial_probs = data.initial_probs
    hidden_markov_model.transition_probs = data.transition_probs
    hidden_markov_model.emission_probs = data.emission_probs

    # Store the hidden Markov Model that we just created
    with open(pickle_file, "wb") as handle:
        pickle.dump(hidden_markov_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    if verbose:
        print("Finished training. Saved Hidden Markov Model to pickle file.")


def array_average(array: []) -> float:
    #  TODO - Replace with numpy.mean()
    total = 0
    for value in array:
        total += value
    return total / len(array)


def read_text_file(file_name) -> str:
    """
    Reads the text file
    :return: file contents
    """
    file = open(file_name, "r")
    words_from_file = file.read()
    file.close()
    newstring = ""
    words_from_file = re.sub(r" (?='|\.|\,|\?| |\!)", "", words_from_file)
    words_from_file = re.sub(r"(<p>)", "", words_from_file)

    word = ""
    for character in words_from_file.lower():
        if character not in '?!.\ ;\n"<>[]@#$%^&*()-_+={}/\\' and not character.isdigit():
            word += character
        elif character == "?" or character == "!":
            word += "."
        elif character == " ":
            # Check if word isn't a random single character
            if len(word) <= 1:
                if word == "a" or word == "i":
                    newstring += word + " "
            else:
                newstring += word + " "

            word = ""
            
    return newstring
