from markovs.ConstrainedHiddenMarkovProcess import *
from markovs.ChimpSentenceGenerator import *
from constraints.ConstraintStartsWithLetter import *
import pickle
import time

from utility.Utility import *
from utility.CountSentences import *


def mnemonics_chimp(
    hidden_markov_model, size_of_model: int, sentence_iterations: int,
        observed_constraints: list, hidden_constraints: list, result_file_name: str):
    """

    :param hidden_markov_model:
    :param size_of_model:
    :param sentence_iterations:
    :param observed_constraints:
    :param hidden_constraints:
    :param result_file_name:
    :return:
    """
    start = time.time()

    # Process the constrained hidden markov model - This is the CHIMP algorithm
    chimp = ConstrainedHiddenMarkovProcess(
        size_of_model, hidden_markov_model, hidden_constraints, observed_constraints
    )
    chimp.process()

    # Can print out the probabilities if you'd like
    # chimp.print_new_markov_probabilities()

    # TIME CONSUMING PORTION RIGHT BELOW
    sentence_generator = ChimpSentenceGenerator(chimp, size_of_model)
    sentences = sentence_generator.create_all_sentences(sentence_iterations)

    # Print out results to a file
    message = "Test complete. It took " + str(time.time() - start) + " seconds"
    with open(f"results/iccc2020_{result_file_name}.txt", "a") as f:
        print(f"{message}. \nNumber of sentences: {len(sentences)}", file=f)
        # Comment in the below two lines if you want all of the generated sentences to be printed
        # for sentence in sentences:
        #     print(sentence, file=f)


def create_new_pickle():
    # How many sentences do we want to train the base HMM on?
    sentences_count = 100000

    # This is where we get the sentences from
    data_file = "data/w_fic_2012.txt"

    # Replace the name for the name of the pickle file
    pickle_file = "pickle_files/iccc_2020.pickle"

    # Pulls in the sentences and cleans the data. Isn't perfect
    contents = utility.CountSentences.CountSentences(data_file)

    # Narrows down the number of sentences we want
    file_contents = contents.sentence_list_as_string(
        contents.get_sentences(sentences_count)
    )

    # Trains the HMM and stores it in pickle_file
    train(number_of_sentences=sentences_count,
          text_file=file_contents,
          pickle_file=pickle_file,
          model="chimp",
          text_contents=True)


if __name__ == '__main__':
    # Name of the pickle file to reduce train time. If you run the train function above,
    # make sure you change the below pickle file to match the new trained pickle file :)
    pickle_file = "pickle_files/iccc_2020.pickle"

    # Number of unique solutions to look for because DFS doesn't work yet. Can go up as many as you want. This is where
    # the time consuming part takes.
    # sentence_iterations = 100000
    sentence_iterations = 100

    # Load our Hidden Markov Model from the pickle file
    with open(pickle_file, "rb") as handle:
        hidden_markov_model = pickle.load(handle)

    # You shouldn't need to alter the above, just need to copy and paste the below 20 times, one for each mnemonic

    # Dante’s 9 circles of hell - LLGGAHVFT
    size_of_model = 9
    observed_contraints = [ConstraintStartsWithLetter("l", True, 1),
                           ConstraintStartsWithLetter("l", True, 1),
                           ConstraintStartsWithLetter("g", True, 1),
                           ConstraintStartsWithLetter("g", True, 1),
                           ConstraintStartsWithLetter("a", True, 1),
                           ConstraintStartsWithLetter("h", True, 1),
                           ConstraintStartsWithLetter("v", True, 1),
                           ConstraintStartsWithLetter("f", True, 1),
                           ConstraintStartsWithLetter("t", True, 1),
    ]

    # Create a blank hidden constraint list
    hidden_constraints = []
    for x in range(size_of_model):
        hidden_constraints.append(None)

    mnemonics_chimp(hidden_markov_model, size_of_model=size_of_model, sentence_iterations=sentence_iterations,
                    observed_constraints=observed_contraints, hidden_constraints=hidden_constraints,
                    result_file_name="dante")
