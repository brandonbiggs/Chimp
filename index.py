from json.tool import main
from operator import mod
import pickle
import time
import re
from constraints.ConstraintContainsSyllables import ConstraintContainsSyllables
from constraints.ConstraintPhraseRhymesWith import ConstraintPhraseRhymesWith
from constraints.ConstraintPhraseEndsWithString import ConstraintPhraseEndsWithString
from constraints.ConstraintMatchesPoetryScheme import ConstraintMatchesPoetryScheme

from utility.Train import train
from utility.Utility import *
from utility.print import *
from utility.ChimpSentenceGenerator import *
from models.CHiMP import *

def load_model(file_to_load):
    with open(file_to_load, "rb") as handle:
        model = pickle.load(handle)
    return model

def process_mm(length, model):
    hidden_constraints = []
    observed_constraints = []
    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)
    
    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    return NHHMM

def process_Chimp(length, model):
    hidden_constraints = []
    observed_constraints = []
    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)

    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    return NHHMM

def process_Chimp_haiku(length, model):
    hidden_constraints = []
    observed_constraints = []
    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)
    # ["NP", "VP", "ADVP"]
    hidden_constraints[0] = [ConstraintIsPartOfSpeech("NP", True)]
    hidden_constraints[1] = [ConstraintIsPartOfSpeech("VP", True)]
    hidden_constraints[2] = [ConstraintIsPartOfSpeech("ADVP", True)]
    # Haiku
    observed_constraints[0] = [ConstraintContainsSyllables(5)]
    observed_constraints[1] = [ConstraintContainsSyllables(7)]
    observed_constraints[2] = [ConstraintContainsSyllables(5)]


    # hidden_constraints = [[ConstraintIsPartOfSpeech("NP", True)], [ConstraintIsPartOfSpeech("VP", True)], None]
    # hidden_constraints = [[ConstraintIsPartOfSpeech("NNP", True)], None, None, None, None, None, None]

    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    return NHHMM

def process_Chimp_limerick(length, model):
    """A limerick is a five-line poem that consists of a single stanza, an AABBA rhyme scheme,

    Args:
        model ([type]): [description]

    Returns:
        [type]: Chimp processed model
    """
    print("CHiMP 2.0 - Limerick")
    hidden_constraints = []
    observed_constraints = []

    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)
    
    hidden_constraints[0] = [ConstraintIsPartOfSpeech("NP", True)]
    a_stresses = ConstraintMatchesPoetryScheme(False, False, 1, -1)
    b_stresses = ConstraintMatchesPoetryScheme(False, False, 1, -1)
    # 8 syllables
    # nantucket = 010 
    # sentence = "there once was a man from nantucket"
    observed_constraints[0] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True)]
    observed_constraints[1] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseEndsWithString("bake")]
    observed_constraints[2] = [b_stresses, ConstraintContainsSyllables(5), ConstraintPhraseRhymesWith(word="ring", position_of_rhyme=-1, must_rhyme=True)]
    observed_constraints[3] = [b_stresses, ConstraintContainsSyllables(5), ConstraintPhraseEndsWithString("ring")]
    observed_constraints[4] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseEndsWithString("cake")]

    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    # print(scheme_A.rhyme_list)
    return NHHMM

def process_Chimp_1_limerick(length, model):
    """A limerick is a five-line poem that consists of a single stanza, an AABBA rhyme scheme,

    Args:
        model ([type]): [description]

    Returns:
        [type]: Chimp processed model
    """
    print("CHiMP 1.0 - Limerick")
    hidden_constraints = []
    observed_constraints = []

    for _ in range(length):
        # if _+1 == 5 or _+1 == 10 or _+1 == 25:
        #     observed_constraints.append(scheme_A)
        # elif _+1 == 15 or _+1 == 20:
        #     observed_constraints.append(scheme_B)
        # else:
        observed_constraints.append(None)
        hidden_constraints.append(None)

    hidden_constraints[0] = [ConstraintIsPartOfSpeech("NNP", True)]

    observed_constraints[4] = [ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True)]
    observed_constraints[9] = [ConstraintMatchesString("bake")]
    observed_constraints[14] = [ConstraintPhraseRhymesWith(word="ring", position_of_rhyme=-1, must_rhyme=True)]
    observed_constraints[19] = [ConstraintMatchesString("ring")]
    observed_constraints[24] = [ConstraintMatchesString("cake")]


    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    # print(scheme_A.rhyme_list)
    return NHHMM

def process_CoMP_limerick(length, model):
    """A limerick is a five-line poem that consists of a single stanza, an AABBA rhyme scheme,

    Args:
        model ([type]): [description]

    Returns:
        [type]: Chimp processed model
    """
    print("CoMP - Limerick")
    hidden_constraints = []
    observed_constraints = []

    scheme_A = [ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True)]
    scheme_B = [ConstraintPhraseRhymesWith(word="ring", position_of_rhyme=-1, must_rhyme=True)]

    for _ in range(length):
        # if _+1 == 5 or _+1 == 10 or _+1 == 25:
        #     observed_constraints.append(scheme_A)
        # elif _+1 == 15 or _+1 == 20:
        #     observed_constraints.append(scheme_B)
        # else:
        observed_constraints.append(None)
        hidden_constraints.append(None)

    observed_constraints[4] = scheme_A
    observed_constraints[9] = [ConstraintMatchesString("bake")]
    observed_constraints[14] = scheme_B
    observed_constraints[19] = [ConstraintMatchesString("ring")]
    observed_constraints[24] = [ConstraintMatchesString("cake")]


    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    # print(scheme_A.rhyme_list)
    return NHHMM

def prettify_sentence(sentence: str) -> str:
    sentence = sentence.capitalize()
    sentence = sentence + "."
    sentence = re.sub(r'\s+([?.!"])', r'\1', sentence)
    return sentence

def print_sentences(length, NHHMM):
    sentence_generator = ChimpSentenceGenerator(NHHMM, length)
    for _ in range(10):
        sentence = sentence_generator.create_sentence()
        print(prettify_sentence(sentence))

if __name__ == '__main__':
    prod = True
    linux = True
    model_name = "chimp"
    # model_name = "markovmodel"
    length = 3
    # poem_type = "limerick-chimp1"
    poem_type = "limerick"



    train_model_bool = False
    load_model_bool = True
    process_model_bool = True
    print_sentences_bool = True

    if prod:
        # 100K
        number_of_sentences = 100000
        text_file_path = "/home/biggbs/school/COCA-Dataset/CocaDataset-01"
        text_file_name = "2016_fic.txt"
        # text_file_name = "2016_acad.txt"
    else:
        number_of_sentences = 3
        text_file_path = "data"
        text_file_name = "fic_test.txt"
        # text_file_name = "one_sentence.txt"
    
    if model_name == "chimp":
        pickle_file = f"pickle_files/{text_file_name}_chimp.pickle"
    else:
        pickle_file = f"pickle_files/{text_file_name}_hmm.pickle"

    if linux:
        parser_path = "/home/biggbs/nltk_data/models/WSJ-PTB3"
    else:
        parser_path = "nltk_data/models/WSJ-PTB3"
    
    input_file = f"{text_file_path}/{text_file_name}"
    markov_order = 1
    pickle_model_bool = True
    verbose = True
    startTime = time.time()


    if train_model_bool:
        model = train(number_of_sentences = number_of_sentences, text_file = input_file, pickle_file = pickle_file, model = model_name, 
            verbose=verbose, markov_order=markov_order, pickle_model_bool=pickle_model_bool, parser_path=parser_path)
    # print_model(model)

    if load_model_bool:
        model = load_model(pickle_file)
    # print_model(model)

    if process_model_bool:
        if model_name == "chimp":
            if poem_type == "haiku":
                length = 3
                NHHMM = process_Chimp_haiku(length=length, model=model)
            elif poem_type == "limerick":
                length = 5
                NHHMM = process_Chimp_limerick(length=length, model=model)
            elif poem_type == "limerick-chimp1":
                length = 25
                NHHMM = process_Chimp_1_limerick(length=length, model=model)
            else:
                NHHMM = process_Chimp(length=length, model=model)
        else:
            if poem_type == "limerick":
                length = 25
                NHHMM = process_CoMP_limerick(length=length, model=model)
            else:
                NHHMM = process_mm(length=length, model=model)
    # print_chimp_markov_probabilities(NHHMM)

    if print_sentences_bool:
        # print(f"Model: {model}")
        print_sentences(length, NHHMM)

    executionTime = (time.time() - startTime)
    print(f'Execution time in seconds: {str(executionTime)}')
