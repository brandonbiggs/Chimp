import pickle
import time
from gensim import models
import argparse

from constraints.ConstraintPhraseRhymesWith import ConstraintPhraseRhymesWith
from constraints.ConstraintMatchesPoetryScheme import ConstraintMatchesPoetryScheme
from constraints.ConstraintSimilarSemanticMeaning import ConstraintSimilarSemanticMeaning

from utility.Utility import *
from utility.print import *
from utility.ChimpSentenceGenerator import *
from models.CHiMP import *
import pronouncing

def load_model(file_to_load):
    with open(file_to_load, "rb") as handle:
        model = pickle.load(handle)
    return model

def process_chimp2_limerick_themes(length, model, output_file, num_sentences_to_try: int, theme: str, word2vec, threshhold):
    # Rhyme constraint -------------------------------------------------------------
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

    a_max_syllables = 7
    b_max_syllables = 4
    a_stresses = ConstraintMatchesPoetryScheme(scheme_a, rhyme_a, a_max_syllables, min_syllables=8)
    b_stresses = ConstraintMatchesPoetryScheme(scheme_b, rhyme_b, b_max_syllables, min_syllables=5)

    # Constraints -------------------------------------------------------------
    hidden_constraints = []
    observed_constraints = []

    for _ in range(length):
        observed_constraints.append(None)
        hidden_constraints.append(None)
    
    # hidden_constraints[0] = [ConstraintIsPartOfSpeech("NP", True)]
    observed_constraints[1] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True), a_stresses]
    observed_constraints[2] = [ConstraintPhraseRhymesWith(word=rhyme_b, position_of_rhyme=-1, must_rhyme=True), b_stresses]
    observed_constraints[3] = [ConstraintPhraseRhymesWith(word=rhyme_b, position_of_rhyme=-1, must_rhyme=True), b_stresses]
    observed_constraints[4] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True), a_stresses]

    # Start -------------------------------------------------------------
    # print("CHiMP 2.0 - Limerick - Themes")
    sentence_output_file = f"output/chimp2-theme-{theme}-{threshhold}-prod.txt"
    # sentence_output_file = None
    theme_constraint = ConstraintSimilarSemanticMeaning(
        theme=theme,  
        similarity_threshhold=threshhold, 
        model=word2vec, 
        verbose=False,
        position_of_theme=0
        # position_of_theme=None
    )

    observed_constraints[0] = [ConstraintPhraseRhymesWith(word=rhyme_a, position_of_rhyme=-1, must_rhyme=True), a_stresses, theme_constraint]

    startTime = time.time()
    NHHMM = ConstrainedHiddenMarkovProcess(length, model, hidden_constraints, observed_constraints)
    NHHMM.process()

    sentence_generator = ChimpSentenceGenerator(NHHMM, length)
    sentences = sentence_generator.count_all_sentences(num_try=num_sentences_to_try, sentence_output_file=sentence_output_file)

    executionTime = (time.time() - startTime)

    # print(f"NHHMM Finished in {str(executionTime)} seconds with theme: {theme} and threshhold: {threshhold}.")
    print(f"Chimp 2 Finished. Seconds: {str(executionTime)}. Theme: {theme}. Threshhold: {threshhold}. Number of sentences: {sentences}.\n", file=open(output_file, "a"))

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
    output_file = f"logs/chimp2-themes-{theme}.txt"

    # word2vec = models.KeyedVectors.load_word2vec_format('/home/biggbs/gensim-data/glove-twitter-25/glove-twitter-25')
    word2vec = models.KeyedVectors.load_word2vec_format('/Users/biggbs/gensim-data/glove-twitter-25/glove-twitter-25')
    # num_sentences_to_try = 10000
    num_sentences_to_try = 50

    # Themes
    process_chimp2_limerick_themes(5, model, output_file, num_sentences_to_try, theme, word2vec, threshhold)
