from json.tool import main
from operator import mod
import pickle
import time
import re
from constraints.ConstraintContainsSyllables import ConstraintContainsSyllables
from constraints.ConstraintPhraseRhymesWith import ConstraintPhraseRhymesWith
from constraints.ConstraintPhraseEndsWithString import ConstraintPhraseEndsWithString
from constraints.ConstraintMatchesPoetryScheme import ConstraintMatchesPoetryScheme
from constraints.ConstraintSimilarSemanticMeaning import ConstraintSimilarSemanticMeaning

from utility.Train import train
from utility.Utility import *
from utility.print import *
from utility.ChimpSentenceGenerator import *
from models.CHiMP import *
import pronouncing

import nltk
from nltk.corpus import cmudict
from rich import print

import pronouncing


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

def process_chimp2_limerick_themes(length, model):
    print("CHiMP 2.0 - Limerick - Themes")
    themes = [
      "flower", 
      "puppy", 
      "rain", 
      "lake", 
      "mountain"
    ]
    similarity_threshholds = [
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        0.95
    ]

    scheme_a = "^.?1.?.?1.?.?"
    scheme_b = "^.?1.?.?"
    rhyme_a = "back"
    rhyme_b = "beat"
    phones_list = pronouncing.phones_for_word(rhyme_a)
    stresses_string = pronouncing.stresses(phones_list[0])
    stresses_string = stresses_string.replace("2", "1")
    scheme_a = scheme_a + stresses_string + "$"

    phones_list = pronouncing.phones_for_word(rhyme_b)
    stresses_string = pronouncing.stresses(phones_list[0])
    stresses_string = stresses_string.replace("2", "1")
    scheme_b = scheme_b + stresses_string + "$"

    hidden_constraints = []
    observed_constraints = []

    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)
    
    hidden_constraints[0] = [ConstraintIsPartOfSpeech("NP", True)]
    a_max_syllables = 7
    b_max_syllables = 4
    a_stresses = ConstraintMatchesPoetryScheme(scheme_a, rhyme_a, a_max_syllables, min_syllables=8)
    b_stresses = ConstraintMatchesPoetryScheme(scheme_b, rhyme_b, b_max_syllables, min_syllables=5)

    # Similarities
    # theme_constrant = ConstraintSimilarSemanticMeaning(theme="sports",  similarity_threshhold=0.7)
    
    output_file = "logs/chimp2-themes.txt"
    total_startTime = time.time()
    for theme in themes:
        for threshhold in similarity_threshholds:
            theme_constraint = ConstraintSimilarSemanticMeaning(theme=theme,  similarity_threshhold=threshhold, verbose=True)

            observed_constraints[0] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True), a_stresses, theme_constraint]
            observed_constraints[1] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True), a_stresses]
            observed_constraints[2] = [ConstraintPhraseRhymesWith(word=rhyme_b, position_of_rhyme=-1, must_rhyme=True), b_stresses]
            observed_constraints[3] = [ConstraintPhraseRhymesWith(word=rhyme_b, position_of_rhyme=-1, must_rhyme=True), b_stresses]
            observed_constraints[4] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True), a_stresses]

            startTime = time.time()
            NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
            NHHMM.process()

            sentence_generator = ChimpSentenceGenerator(NHHMM, length)
            sentences = sentence_generator.count_all_sentences(num_try=1000)

            executionTime = (time.time() - startTime)

            print(f'Execution time in seconds: {str(executionTime)}')
            print(f"NHHMM Finished in {str(executionTime)} seconds with theme: {theme} and threshhold: {threshhold}.")
            print(f"NHHMM Finished in {str(executionTime)} seconds with theme: {theme} and threshhold: {threshhold}.", file=open(output_file, "a"))
            print(f"Number of sentences: {sentences}.", file=open(output_file, "a"))
            print_sentences(length, NHHMM, poem_type=None, count = 5, output_file=output_file)
            print("", file=open(output_file, "a"))

    print("Finished.")
    executionTime = (time.time() - total_startTime)
    print(f'Execution time in seconds: {str(executionTime)}')

def process_chimp2_limerick_series(length, model):
    """_summary_

    Args:
        length (_type_): _description_
        model (_type_): _description_
    """
    print("CHiMP 2.0 - Limerick - Series")
    # https://www.thoughtco.com/simple-guide-to-word-families-2081410#:~:text=According%20to%20researchers%20Wylie%20and,%2Cug%2C%20ump%2C%20unk.
    # Source: Richard E. Wylie and Donald D. Durrell, 1970. "Teaching Vowels Through Phonograms." Elementary English 47, 787-791.
    rhyme_words = [
        "back", # ack
        "brain", # ain
        "bake", # ake
        "beat", # eat
        "bell", # ell
        "best", # est
        "dice", # ice
        "brick", # ick
        "hide", # ide
        "bump", # ump
    ]
    a_max_syllables = 7
    b_max_syllables = 4

    scheme_a = "^.?1.?.?1.?.?"
    scheme_b = "^.?1.?.?"
    output_file = "logs/long_run.txt"
    total_startTime = time.time()
    for a_word in rhyme_words:
        phones_list = pronouncing.phones_for_word(a_word)
        stresses_string = pronouncing.stresses(phones_list[0])
        stresses_string = stresses_string.replace("2", "1")
        scheme_a_new = scheme_a + stresses_string + "$"
        for b_word in rhyme_words:
            if a_word != b_word:
                startTime = time.time()
                phones_list = pronouncing.phones_for_word(b_word)
                stresses_string = pronouncing.stresses(phones_list[0])
                stresses_string = stresses_string.replace("2", "1")
                scheme_b_new = scheme_b + stresses_string + "$"
                hidden_constraints = []
                observed_constraints = []

                for _ in range(length):
                    observed_constraints.append(None)
                    hidden_constraints.append(None)

                hidden_constraints[0] = [ConstraintIsPartOfSpeech("NP", True)]
                a_stresses = ConstraintMatchesPoetryScheme(scheme_a_new, a_word, a_max_syllables, min_syllables=8)
                b_stresses = ConstraintMatchesPoetryScheme(scheme_b_new, b_word, b_max_syllables, min_syllables=5)

                observed_constraints[0] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), a_stresses]
                observed_constraints[1] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), a_stresses]
                observed_constraints[2] = [ConstraintPhraseRhymesWith(word=b_word, position_of_rhyme=-1, must_rhyme=True), b_stresses]
                observed_constraints[3] = [ConstraintPhraseRhymesWith(word=b_word, position_of_rhyme=-1, must_rhyme=True), b_stresses]
                observed_constraints[4] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), a_stresses]

                NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
                NHHMM.process()
                executionTime = (time.time() - startTime)
                print(f'Execution time in seconds: {str(executionTime)}')
                print(f"NHHMM Finished in {str(executionTime)} seconds with rhyme words A: {a_word}, B: {b_word}.")
                print(f"NHHMM Finished in {str(executionTime)} seconds with rhyme words A: {a_word}, B: {b_word}.", file=open(output_file, "a"))
                print_sentences(length, NHHMM, poem_type=None, count = 5, output_file=output_file)
                print("", file=open(output_file, "a"))
    print("Finished.")
    executionTime = (time.time() - total_startTime)
    print(f'Execution time in seconds: {str(executionTime)}')              

def process_Chimp_limerick(length, model):
    """A limerick is a five-line poem that consists of a single stanza, an AABBA rhyme scheme,

    Args:
        model ([type]): [description]

    Returns:
        [type]: Chimp processed model
    """
    print("CHiMP 2.0 - Limerick")

    scheme_a = "^.?1.?.?1.?.?"
    scheme_b = "^.?1.?.?"
    rhyme_a = "lake"
    rhyme_b = "ring"
    phones_list = pronouncing.phones_for_word(rhyme_a)
    stresses_string = pronouncing.stresses(phones_list[0])
    stresses_string = stresses_string.replace("2", "1")
    scheme_a = scheme_a + stresses_string + "$"

    phones_list = pronouncing.phones_for_word(rhyme_b)
    stresses_string = pronouncing.stresses(phones_list[0])
    stresses_string = stresses_string.replace("2", "1")
    scheme_b = scheme_b + stresses_string + "$"

    hidden_constraints = []
    observed_constraints = []

    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)
    
    hidden_constraints[0] = [ConstraintIsPartOfSpeech("NP", True)]
    a_max_syllables = 7
    b_max_syllables = 4
    a_stresses = ConstraintMatchesPoetryScheme(scheme_a, rhyme_a, a_max_syllables, min_syllables=8)
    b_stresses = ConstraintMatchesPoetryScheme(scheme_b, rhyme_b, b_max_syllables, min_syllables=5)

    # Similarities
    # theme_constrant = ConstraintSimilarSemanticMeaning(theme="sports",  similarity_threshhold=0.7)
    theme_constraint = ConstraintSimilarSemanticMeaning(theme="health",  similarity_threshhold=0.7, verbose=True)

    observed_constraints[0] = [ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True), a_stresses, theme_constraint]
    observed_constraints[1] = [ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True), a_stresses, theme_constraint]
    observed_constraints[2] = [ConstraintPhraseRhymesWith(word="ring", position_of_rhyme=-1, must_rhyme=True), b_stresses]
    observed_constraints[3] = [ConstraintPhraseRhymesWith(word="ring", position_of_rhyme=-1, must_rhyme=True), b_stresses]
    observed_constraints[4] = [ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True), a_stresses, theme_constraint]

    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
    # print(scheme_A.rhyme_list)
    return NHHMM

def process_CoMP_limerick_series(length, model):
    print("CoMP - Limerick - Series")
    output_file = "logs/long_comp_run.txt"
    rhyme_words = [
        "back", # ack
        "brain", # ain
        "bake", # ake
        "beat", # eat
        "bell", # ell
        "best", # est
        "dice", # ice
        "brick", # ick
        "hide", # ide
        "bump", # ump
    ]
    total_startTime = time.time()
    for a_word in rhyme_words:
        for b_word in rhyme_words:
            observed_constraints = []
            hidden_constraints = []
            for _ in range(length):
                hidden_constraints.append(None)
                observed_constraints.append(None)
            if a_word != b_word:
                startTime = time.time()

                observed_constraints[0] = [ConstraintContainsSyllables(1)]
                observed_constraints[1] = [ConstraintContainsSyllables(2)]
                observed_constraints[2] = [ConstraintContainsSyllables(2)]
                observed_constraints[3] = [ConstraintContainsSyllables(2)]
                observed_constraints[4] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), 
                                            ConstraintContainsSyllables(1),
                                        ]
                
                observed_constraints[5] = [ConstraintContainsSyllables(1)]
                observed_constraints[6] = [ConstraintContainsSyllables(2)]
                observed_constraints[7] = [ConstraintContainsSyllables(2)]
                observed_constraints[8] = [ConstraintContainsSyllables(2)]
                observed_constraints[9] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), 
                                            ConstraintContainsSyllables(1),
                                        ]
                
                observed_constraints[10] = [ConstraintContainsSyllables(1)]
                observed_constraints[11] = [ConstraintContainsSyllables(1)]
                observed_constraints[12] = [ConstraintContainsSyllables(1)]
                observed_constraints[13] = [ConstraintContainsSyllables(1)]
                observed_constraints[14] = [ConstraintPhraseRhymesWith(word=b_word, position_of_rhyme=-1, must_rhyme=True), 
                                                ConstraintContainsSyllables(1)
                                        ]
                
                observed_constraints[15] = [ConstraintContainsSyllables(1)]
                observed_constraints[16] = [ConstraintContainsSyllables(1)]
                observed_constraints[17] = [ConstraintContainsSyllables(1)]
                observed_constraints[18] = [ConstraintContainsSyllables(1)]
                observed_constraints[19] = [ConstraintPhraseRhymesWith(word=b_word, position_of_rhyme=-1, must_rhyme=True), 
                                                ConstraintContainsSyllables(1)
                                        ]
                
                observed_constraints[20] = [ConstraintContainsSyllables(1)]
                observed_constraints[21] = [ConstraintContainsSyllables(2)]
                observed_constraints[22] = [ConstraintContainsSyllables(2)]
                observed_constraints[23] = [ConstraintContainsSyllables(2)]
                observed_constraints[24] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), 
                                            ConstraintContainsSyllables(1),
                                        ]

                CoMP = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
                CoMP.process()
                executionTime = (time.time() - startTime)
                print("CoMP Finished")
                print(f'Execution time in seconds: {str(executionTime)}')
                print(f"CoMP Finished in {str(executionTime)} seconds with rhyme words A: {a_word}, B: {b_word}.")
                print(f"CoMP Finished in {str(executionTime)} seconds with rhyme words A: {a_word}, B: {b_word}.", file=open(output_file, "a"))
                print_sentences(length, CoMP, poem_type=None, count = 5, output_file=output_file)
                print("", file=open(output_file, "a"))
    print("Finished.")
    executionTime = (time.time() - total_startTime)
    print(f'Execution time in seconds: {str(executionTime)}')   

def process_Chimp_1_limerick_series(length, model):
    """_summary_

    Args:
        length (_type_): _description_
        model (_type_): _description_
    """
    print("CHiMP 1.0 - Limerick - Series")
    output_file = "logs/long_chimp_1_run.txt"
    rhyme_words = [
        "back", # ack
        "brain", # ain
        "bake", # ake
        "beat", # eat
        "bell", # ell
        "best", # est
        "dice", # ice
        "brick", # ick
        "hide", # ide
        "bump", # ump
    ]
    total_startTime = time.time()
    for a_word in rhyme_words:
        for b_word in rhyme_words:
            hidden_constraints = []
            observed_constraints = []
            for _ in range(length):
                observed_constraints.append(None)
                hidden_constraints.append(None)
            if a_word != b_word:
                startTime = time.time()
                hidden_constraints[0] = [ConstraintIsPartOfSpeech("NNP", True)]

                observed_constraints[0] = [ConstraintContainsSyllables(1)]
                observed_constraints[1] = [ConstraintContainsSyllables(2)]
                observed_constraints[2] = [ConstraintContainsSyllables(2)]
                observed_constraints[3] = [ConstraintContainsSyllables(2)]
                observed_constraints[4] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), 
                                            ConstraintContainsSyllables(1),
                                        ]
                
                observed_constraints[5] = [ConstraintContainsSyllables(1)]
                observed_constraints[6] = [ConstraintContainsSyllables(2)]
                observed_constraints[7] = [ConstraintContainsSyllables(2)]
                observed_constraints[8] = [ConstraintContainsSyllables(2)]
                observed_constraints[9] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), 
                                            ConstraintContainsSyllables(1),
                                        ]
                
                observed_constraints[10] = [ConstraintContainsSyllables(1)]
                observed_constraints[11] = [ConstraintContainsSyllables(1)]
                observed_constraints[12] = [ConstraintContainsSyllables(1)]
                observed_constraints[13] = [ConstraintContainsSyllables(1)]
                observed_constraints[14] = [ConstraintPhraseRhymesWith(word=b_word, position_of_rhyme=-1, must_rhyme=True), 
                                                ConstraintContainsSyllables(1)
                                        ]
                
                observed_constraints[15] = [ConstraintContainsSyllables(1)]
                observed_constraints[16] = [ConstraintContainsSyllables(1)]
                observed_constraints[17] = [ConstraintContainsSyllables(1)]
                observed_constraints[18] = [ConstraintContainsSyllables(1)]
                observed_constraints[19] = [ConstraintPhraseRhymesWith(word=b_word, position_of_rhyme=-1, must_rhyme=True), 
                                                ConstraintContainsSyllables(1)
                                        ]
                
                observed_constraints[20] = [ConstraintContainsSyllables(1)]
                observed_constraints[21] = [ConstraintContainsSyllables(2)]
                observed_constraints[22] = [ConstraintContainsSyllables(2)]
                observed_constraints[23] = [ConstraintContainsSyllables(2)]
                observed_constraints[24] = [ConstraintPhraseRhymesWith(word=a_word, position_of_rhyme=-1, must_rhyme=True), 
                                            ConstraintContainsSyllables(1),
                                        ]

                NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
                NHHMM.process()
                executionTime = (time.time() - startTime)
                print("NHHMM Finished")
                print(f'Execution time in seconds: {str(executionTime)}')
                print(f"NHHMM Finished in {str(executionTime)} seconds with rhyme words A: {a_word}, B: {b_word}.")
                print(f"NHHMM Finished in {str(executionTime)} seconds with rhyme words A: {a_word}, B: {b_word}.", file=open(output_file, "a"))
                print_sentences(length, NHHMM, poem_type=None, count = 5, output_file=output_file)
                print("", file=open(output_file, "a"))
    print("Finished.")
    executionTime = (time.time() - total_startTime)
    print(f'Execution time in seconds: {str(executionTime)}')   

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

    theme_constraint = ConstraintSimilarSemanticMeaning(theme="fruit",  similarity_threshhold=0.7)

    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)

    hidden_constraints[0] = [ConstraintIsPartOfSpeech("NNP", True)]

    observed_constraints[0] = [ConstraintContainsSyllables(1)]
    observed_constraints[1] = [ConstraintContainsSyllables(2)]
    observed_constraints[2] = [ConstraintContainsSyllables(2)]
    observed_constraints[3] = [ConstraintContainsSyllables(2)]
    observed_constraints[4] = [ConstraintPhraseRhymesWith(word="lake", position_of_rhyme=-1, must_rhyme=True), 
                                theme_constraint,
                                ConstraintContainsSyllables(1),
                            ]
    
    observed_constraints[5] = [ConstraintContainsSyllables(1)]
    observed_constraints[6] = [ConstraintContainsSyllables(2)]
    observed_constraints[7] = [ConstraintContainsSyllables(2)]
    observed_constraints[8] = [ConstraintContainsSyllables(2)]
    observed_constraints[9] = [ConstraintMatchesString("bake"),
                            ]
    
    observed_constraints[10] = [ConstraintContainsSyllables(1)]
    observed_constraints[11] = [ConstraintContainsSyllables(1)]
    observed_constraints[12] = [ConstraintContainsSyllables(1)]
    observed_constraints[13] = [ConstraintContainsSyllables(1)]
    observed_constraints[14] = [ConstraintPhraseRhymesWith(word="ring", position_of_rhyme=-1, must_rhyme=True), 
                                    ConstraintContainsSyllables(1)
                            ]
    
    observed_constraints[15] = [ConstraintContainsSyllables(1)]
    observed_constraints[16] = [ConstraintContainsSyllables(1)]
    observed_constraints[17] = [ConstraintContainsSyllables(1)]
    observed_constraints[18] = [ConstraintContainsSyllables(1)]
    observed_constraints[19] = [ConstraintMatchesString("ring")
                            ]
    
    observed_constraints[20] = [ConstraintContainsSyllables(1)]
    observed_constraints[21] = [ConstraintContainsSyllables(2)]
    observed_constraints[22] = [ConstraintContainsSyllables(2)]
    observed_constraints[23] = [ConstraintContainsSyllables(2)]
    observed_constraints[24] = [ConstraintMatchesString("cake")]

    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()
    print("NHHMM Finished")
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
    # sub_phrases = count_syllables([8, 8, 5, 5, 8], sentence)
    print(sentence)
    # if sub_phrases is None:
    #     print(sentence)
    # else:
    #     print(sub_phrases)
    #     for phrase in sub_phrases:
    #         new_phrase = ""
    #         for word in phrase.split(" "):
    #             test = pronouncing.phones_for_word(word)
    #             output = pronouncing.stresses(test[0])
    #             if output == "1":
    #                 new_phrase += f"[bold]{word}[/bold] "
    #                 # print(f"[bold]{word}[/bold] - {test[0]} - {output}")
    #             elif output == "0":
    #                 new_phrase += f"{word} "
    #                 # print(f"{word} - {test[0]} - {output}")
    #             else:
    #                 new_phrase += f"[bold red]{word}[/bold red] "
    #                 # print(f"[bold red]{word}[/bold red] - {test[0]} - {output}")
    #         print(new_phrase)
    return None

def prettify_sentence(sentence: str) -> str:
    sentence = sentence.capitalize()
    sentence = sentence + "."
    sentence = re.sub(r'\s+([?.!"])', r'\1', sentence)
    return sentence

def print_sentences(length, NHHMM, poem_type, count: int = 10, output_file: str = None):
    sentence_generator = ChimpSentenceGenerator(NHHMM, length)
    for _ in range(count):
        sentence = sentence_generator.create_sentence()
        if poem_type == "limerick":
            prettify_and_print_limericks(sentence)
            print("")
        else:
            if output_file is None:
                print(prettify_sentence(sentence))
            else:
                print(prettify_sentence(sentence), file=open(output_file, "a"))

if __name__ == '__main__':
    # This is only for the long run - 
    text_file_name = "2016_fic.txt"
    # pickle_file = f"pickle_files/{text_file_name}_hmm.pickle"
    pickle_file = f"pickle_files/{text_file_name}_chimp.pickle"
    model = load_model(pickle_file)
    # Series
    # process_chimp2_limerick_series(5, model)
    # process_Chimp_1_limerick_series(25, model)
    # process_CoMP_limerick_series(25, model)

    # Themes
    process_chimp2_limerick_themes(5, model)
    quit(0)

    # very specific words,
    # flower, roses, puppies, green, rabbits, dew, raindrop, treetop, photosynthesis, chlorofil??, puddle, lake, mountaintop, snow?, 
    # As long as the other meanings of the words are useful
    # Five or so themes, with 5 generated limericks, one for each theme
    # multiple choice

    # floating constraints, coherence within the phrase
    # Survey does #2
    # Chimp 2.5 with a higher semantic threshhold, the floating constraint is the only way to get results
    # Apply semantic constraints to each line and compare to chimp 1 and 2 but chimp 1 the constraint is at a specific position
    # chimp 2 is floating constraints
    # x is the threshold
    # y is the # of solutions or a yes/no about being able to generate solutions
    # could do the average over several semantic constraints

    # Then in the survey show a semanticly constrained limerick from both chimp 1 and 2 that is the result of the highest threshhold from each model
    # both would have the same theme, rate as to how well it achives that theme.

    # 2 sections
    # Section 1 - semantics
    # section 2 - syntactic

    # With the phrases, Vanilla markov model, to increase the cohesiveness, you have to increase the markov order. In this model, you can very the cohesiveness throughout
    # by increasing the phrase length. Like a minimum cohesiveness level. At least X or at most Y. There's a range. Upper range avoids plagarism
    # while the lower limit is a minimum cohesion level. A regular markov model is very set by the markov order.Future work - exploring these lengths
    # as you can set different constraints additionally within that level. All sorts of floating constraints that you can put on these varying length phrases that can be generated via the model.
    # Variable Order Markov Models - Check into those. Might want to mention those if they're similar/related in thesis

    # Like "The United state of __" with a regular markov model, you wouldn't want variablility because it's more than likely "America", whereas a specific Markov order would provide any
    # word that comes after "of" or the part of speech that is "of".

    # https://transactions.ismir.net/articles/10.5334/tismir.97/
    # https://www2.cose.isu.edu/~bodipaul/writing/
    # Everything below is for a normal run
    prod = True
    linux = True
    model_name = "chimp"
    # model_name = "markovmodel"
    length = 3
    # poem_type = "limerick-chimp1"
    poem_type = "limerick-chimp2"
    # poem_type = "limerick-comp"

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
            elif poem_type == "limerick-chimp2":
                length = 5
                NHHMM = process_Chimp_limerick(length=length, model=model)
            elif poem_type == "limerick-chimp1":
                length = 25
                NHHMM = process_Chimp_1_limerick(length=length, model=model)
            else:
                NHHMM = process_Chimp(length=length, model=model)
        else:
            if poem_type == "limerick-comp":
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
