import pickle
import time
from gensim import models
import argparse

from constraints.ConstraintContainsSyllables import ConstraintContainsSyllables
from constraints.ConstraintPhraseRhymesWith import ConstraintPhraseRhymesWith
from constraints.ConstraintSimilarSemanticMeaning import ConstraintSimilarSemanticMeaning
from constraints.ConstraintMatchesPoetryScheme import ConstraintMatchesPoetryScheme

from utility.Utility import *
from utility.print import *
from utility.ChimpSentenceGenerator import *
from models.CHiMP import *

def load_model(file_to_load):
    with open(file_to_load, "rb") as handle:
        model = pickle.load(handle)
    return model

def process_chimp1_limerick_themes(length, model, output_file, num_sentences_to_try: int, theme: str, word2vec, threshhold):
    rhyme_a = "back"
    rhyme_b = "beat"

    # Constraints -------------------------------------------------------------
    hidden_constraints = []
    observed_constraints = []

    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)

    theme_constraint = ConstraintSimilarSemanticMeaning(
        theme=theme,  
        similarity_threshhold=threshhold, 
        model=word2vec, 
        verbose=False
    )
    
    # hidden_constraints[0] = [ConstraintIsPartOfSpeech("NNP", True)]

    observed_constraints[0] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1), theme_constraint]
    observed_constraints[1] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme("1.", None, 2, min_syllables=2)]
    observed_constraints[2] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme(".1", None, 2, min_syllables=2)]
    observed_constraints[3] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme("..", None, 1, min_syllables=1)]
    observed_constraints[4] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True), 
                                ConstraintContainsSyllables(1),
                                ConstraintMatchesPoetryScheme("1", None, 1, min_syllables=1)
                            ]
    
    observed_constraints[5] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[6] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme("1.", None, 2, min_syllables=2)]
    observed_constraints[7] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme(".1", None, 2, min_syllables=2)]
    observed_constraints[8] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme("..", None, 1, min_syllables=1)]
    observed_constraints[9] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True),
                                ConstraintContainsSyllables(1),
                                ConstraintMatchesPoetryScheme("1", None, 1, min_syllables=1)
                            ]
    
    observed_constraints[10] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[11] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme("1", None, 1, min_syllables=1)]
    observed_constraints[12] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[13] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[14] = [ConstraintPhraseRhymesWith(word=rhyme_b, position_of_rhyme=-1, must_rhyme=True), 
                                ConstraintContainsSyllables(1),
                                ConstraintMatchesPoetryScheme("1", None, 1, min_syllables=1)
                            ]
    
    observed_constraints[15] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[16] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme("1", None, 1, min_syllables=1)]
    observed_constraints[17] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[18] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[19] = [ConstraintMatchesString(rhyme_b),
                                ConstraintContainsSyllables(1),
                                ConstraintMatchesPoetryScheme("1", None, 1, min_syllables=1)
                            ]
    
    observed_constraints[20] = [ConstraintContainsSyllables(1), ConstraintMatchesPoetryScheme(".", None, 1, min_syllables=1)]
    observed_constraints[21] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme("1.", None, 2, min_syllables=2)]
    observed_constraints[22] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme(".1", None, 2, min_syllables=2)]
    observed_constraints[23] = [ConstraintContainsSyllables(2), ConstraintMatchesPoetryScheme("..", None, 1, min_syllables=1)]
    observed_constraints[24] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True),
                                ConstraintContainsSyllables(1),
                                ConstraintMatchesPoetryScheme("1", None, 1, min_syllables=1)
                            ] 

    # Start -------------------------------------------------------------
    # print("CHiMP 1.0 - Limerick - Themes")
    # sentence_output_file = f"output/chimp1-theme-{theme}-{threshhold}.txt"
    sentence_output_file = None

    startTime = time.time()
    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()

    sentence_generator = ChimpSentenceGenerator(NHHMM, length)
    sentences = sentence_generator.count_all_sentences(num_try=num_sentences_to_try, sentence_output_file=sentence_output_file)

    executionTime = (time.time() - startTime)

    # print(f"NHHMM Finished in {str(executionTime)} seconds with theme: {theme} and threshhold: {threshhold}.")
    print(f"Chimp 1 Finished. Seconds: {str(executionTime)}. Theme: {theme}. Threshhold: {threshhold}. Number of sentences: {sentences}.\n", file=open(output_file, "a"))
    # print(f"Number of sentences: {sentences}.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--theme', help='the theme')
    parser.add_argument('--threshhold', help='threshhold percentage')

    args = parser.parse_args()
    theme = args.theme
    threshhold = float(args.threshhold)
    if theme == "" or threshhold == "":
        quit(1)

    # This is only for the long run - 
    text_file_name = "2016_fic.txt"
    pickle_file = f"pickle_files/{text_file_name}_chimp.pickle"
    model = load_model(pickle_file)
    output_file = f"logs/chimp1-themes-{theme}.txt"

    word2vec = models.KeyedVectors.load_word2vec_format('/home/biggbs/gensim-data/glove-twitter-25/glove-twitter-25')
    # word2vec = models.KeyedVectors.load_word2vec_format('/Users/biggbs/gensim-data/glove-twitter-25/glove-twitter-25')
    num_sentences_to_try = 10000
    # num_sentences_to_try = 100

    process_chimp1_limerick_themes(25, model, output_file, num_sentences_to_try, theme, word2vec, threshhold)
