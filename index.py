from json.tool import main
import pickle

from utility.Train import train
from utility.Utility import *
from utility.print import *
from utility.ChimpSentenceGenerator import *
from models.CHiMP import *

def load_model(file_to_load):
    with open(file_to_load, "rb") as handle:
        model = pickle.load(handle)
    return model

def process(length, model):
    hidden_constraints = []
    observed_constraints = []
    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)

    # hidden_constraints = [[ConstraintIsPartOfSpeech("NP", True)], [ConstraintIsPartOfSpeech("VP", True)], None]
    # hidden_constraints = [[ConstraintIsPartOfSpeech("NNP", True)], None, None, None, None, None, None]

    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    return NHHMM

def print_sentences(length, NHHMM):
    sentence_generator = ChimpSentenceGenerator(NHHMM, length)
    for _ in range(10):
        print(sentence_generator.create_sentence())

if __name__ == '__main__':
    prod = True
    model_name = "chimp"
    train_model_bool = True
    load_model_bool = False
    process_model_bool = False
    print_sentences_bool = False
    length = 7

    if prod:
        # 100K
        number_of_sentences = 100000
        text_file_path = "/home/biggbs/school/COCA-Dataset/CocaDataset-01"
        text_file_name = "2016_fic.txt"
        # text_file_name = "2016_acad.txt"
        verbose = True
        parser_path = "/home/biggbs/nltk_data/models/WSJ-PTB3"
    else:
        number_of_sentences = 100
        text_file_path = "data"
        text_file_name = "book_medium.txt"
        # text_file_name = "one_sentence.txt"
        verbose = True
        parser_path = "nltk_data/models/WSJ-PTB3"
    
    if model_name == "chimp":
        pickle_file = f"pickle_files/{text_file_name}_chimp.pickle"
    else:
        pickle_file = f"pickle_files/{text_file_name}_hmm.pickle"

    input_file = f"{text_file_path}/{text_file_name}"
    markov_order = 1
    pickle_model_bool = True

    if train_model_bool:
        model = train(number_of_sentences = number_of_sentences, text_file = input_file, pickle_file = pickle_file, model = model_name, 
            verbose=verbose, markov_order=markov_order, pickle_model_bool=pickle_model_bool, parser_path=parser_path)
    # print_model(model)

    if load_model_bool:
        model = load_model(pickle_file)
    # print_model(model)

    if process_model_bool:
        NHHMM = process(length=length, model=model)
    # print_chimp_markov_probabilities(NHHMM)

    if print_sentences_bool:
        print_sentences(length, NHHMM)
