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
import pronouncing

import nltk
from nltk.corpus import cmudict
from rich import print


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
    a_stresses = ConstraintMatchesPoetryScheme(True, True, "1", -1)
    b_stresses = ConstraintMatchesPoetryScheme(True, True, "1", -1)
    # 8 syllables
    # nantucket = 010 
    # sentence = "there once was a man from nantucket"
    # observed_constraints[0] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True)]
    # observed_constraints[1] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True)]
    # observed_constraints[2] = [b_stresses, ConstraintContainsSyllables(5), ConstraintPhraseRhymesWith(word="ring", position_of_rhyme=-1, must_rhyme=True)]
    # observed_constraints[3] = [b_stresses, ConstraintContainsSyllables(5), ConstraintPhraseEndsWithString("ring")]
    # observed_constraints[4] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseEndsWithString("cake")]

    observed_constraints[0] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseRhymesWith(word="say", position_of_rhyme=-1, must_rhyme=True)]
    observed_constraints[1] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseRhymesWith(word="say", position_of_rhyme=-1, must_rhyme=True)]
    observed_constraints[2] = [b_stresses, ConstraintContainsSyllables(5), ConstraintPhraseRhymesWith(word="brave", position_of_rhyme=-1, must_rhyme=True)]
    observed_constraints[3] = [b_stresses, ConstraintContainsSyllables(5), ConstraintPhraseEndsWithString("brave")]
    observed_constraints[4] = [a_stresses, ConstraintContainsSyllables(8), ConstraintPhraseEndsWithString("say")]

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

def count_syllables(num_syllables: list, phrase: str) -> list:
    cmu_dict = cmudict.dict()
    num_of_syllables = 0
    index = 0
    sub_phrases = []
    sub_phrase = ""
    phrase = phrase.strip()
    phrase = re.sub(' +', ' ', phrase)
    for word in phrase.split(" "):
        word = word.lower()
        sub_phrase += word + " "
        try:
            num_of_syllables = num_of_syllables + [len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word]][0]
        except KeyError:
            return None
        if num_of_syllables == num_syllables[index]:
            index += 1
            num_of_syllables = 0 
            sub_phrases.append(sub_phrase.strip())
            sub_phrase = ""
    # print(sub_phrases)
    return sub_phrases

def prettify_and_print_limericks(sentence: str) -> str:
    sub_phrases = count_syllables([8, 8, 5, 5, 8], sentence)
    if sub_phrases is None:
        print(sentence)
    else:
        # print(sub_phrases)
        for phrase in sub_phrases:
            new_phrase = ""
            for word in phrase.split(" "):
                test = pronouncing.phones_for_word(word)
                output = pronouncing.stresses(test[0])
                if output == "1":
                    new_phrase += f"[bold]{word}[/bold] "
                    # print(f"[bold]{word}[/bold] - {test[0]} - {output}")
                elif output == "0":
                    new_phrase += f"{word} "
                    # print(f"{word} - {test[0]} - {output}")
                else:
                    new_phrase += f"[bold red]{word}[/bold red] "
                    # print(f"[bold red]{word}[/bold red] - {test[0]} - {output}")
            print(new_phrase)

def prettify_sentence(sentence: str) -> str:
    sentence = sentence.capitalize()
    sentence = sentence + "."
    sentence = re.sub(r'\s+([?.!"])', r'\1', sentence)
    return sentence

def print_sentences(length, NHHMM, poem_type):
    sentence_generator = ChimpSentenceGenerator(NHHMM, length)
    for _ in range(10):
        sentence = sentence_generator.create_sentence()
        if poem_type == "limerick":
            prettify_and_print_limericks(sentence)
            print("")
        else:
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
        print_sentences(length, NHHMM, poem_type)

    executionTime = (time.time() - startTime)
    print(f'Execution time in seconds: {str(executionTime)}')
