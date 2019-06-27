import random
import pickle
from utility.ProcessDataForChimp import ProcessDataForChimp
from markovs.HiddenMarkovModel import HiddenMarkovModel


def get_rand_num(first=0, second=1):
    """
    By default returns a number between 0 and 1
    Wanted to put this in it's own function in case we decide to change
    how randoms are created in the future.
    :param first:
    :param second:
    :return: Number between first and second provided numbers
    """
    return random.uniform(first, second)


def train(text_file="data/book_tiny.txt",
          pickle_file="pickle_files/new_file.pickle") -> None:
    """
    Create the hidden markov model and store it for use later
    """
    print("Starting training on:", text_file)
    pickle_file_name = input("Enter a name for your trained model: ")
    if pickle_file_name == "":
        print("No name provided. Going with the default: ", pickle_file)
    else:
        pickle_file_name = pickle_file_name.strip()
        pickle_file = "pickle_files/" + pickle_file_name + ".pickle"
        print("Your file will be saved to: ", pickle_file)
    # Process the text file
    data = ProcessDataForChimp(text_file)

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(data.hidden_nodes, data.observed_nodes)
    hidden_markov_model.initial_probs = data.initial_probs
    hidden_markov_model.transition_probs = data.transition_probs
    hidden_markov_model.emission_probs = data.emission_probs

    # Store the hidden Markov Model that we just created
    with open(pickle_file, 'wb') as handle:
        pickle.dump(hidden_markov_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("Finished training. Saved Hidden Markov Model to pickle file.")


def read_text_file(file_name) -> str:
    """
    Reads the text file
    :return: None
    """
    file = open(file_name, "r")
    words_from_file = file.read()
    file.close()
    return words_from_file
