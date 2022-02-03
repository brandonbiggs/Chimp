from utility.TrainChimp import TrainChimp
from utility.TrainMarkovModel import TrainMarkovModel
from models.HiddenMarkovModel import HiddenMarkovModel
from utility.Utility import pickle_model

def train(number_of_sentences: int, text_file: str = "data/book_tiny.txt", 
        pickle_file: str = "pickle_files/new_file.pickle", model: str = "chimp", verbose: bool = True,
        text_contents: bool = False, pickle_model_bool: bool = False, markov_order: int = 1) -> HiddenMarkovModel:
    """Create the hidden markov model and store it for use later

    Args:
        number_of_sentences (int): [description]
        text_file (str, optional): [description]. Defaults to "data/book_tiny.txt".
        pickle_file (str, optional): [description]. Defaults to "pickle_files/new_file.pickle".
        model (str, optional): [description]. Defaults to "chimp".
        verbose (bool, optional): [description]. Defaults to True.
        text_contents (bool, optional): If this is set to true, text file is not the name of a file,
        but it's actually the contents of a file. The purpose of this is to make sure
        chimp and markov model are using the same exact sentences. Verbose and text_contents
        should not both be set to True. Defaults to False.
        pickle_model (bool, optional): [description]. Defaults to False.
        markov_order (int, optional): [description]. Defaults to 1.

    Raises:
        Exception: [description]

    Returns:
        HiddenMarkovModel: [description]
    """
    if verbose and not text_contents:
        print("Starting training on:", text_file)
    if pickle_file == "" and verbose:
        print("No name provided. Going with the default: ", pickle_file)
    else:
        if verbose:
            print("Your file will be saved to: ", pickle_file)
    
    # Process the text file
    if model == "chimp":
        if verbose: print("Training CHiMP model.")
        data = TrainChimp(text_file, number_of_sentences, False, file_contents=text_contents, markov_order=markov_order)
    
    elif model == "markovmodel":
        if verbose: print("Training Markov model.")
        data = TrainMarkovModel(text_file, number_of_sentences, False, file_contents_bool=text_contents, should_tag_pos=True,
            markov_order=markov_order)
    else:
        raise Exception("Unknown model. Please use either 'chimp' or 'markovmodel'")

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(data.hidden_nodes, data.observed_nodes)
    hidden_markov_model.initial_probs = data.initial_probs
    hidden_markov_model.transition_probs = data.transition_probs
    hidden_markov_model.emission_probs = data.emission_probs
    hidden_markov_model.markov_order = data.markov_order

    # Store the hidden Markov Model that we just created
    if pickle_model_bool:
        pickle_model(pickle_file, hidden_markov_model, verbose)
        # with open(pickle_file, "wb") as handle:
        #     pickle.dump(hidden_markov_model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        # if verbose:
        #     print("Finished training. Saved model to pickle file.")
    return hidden_markov_model
