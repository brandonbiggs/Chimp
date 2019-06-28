from markovs.HiddenMarkovModel import *
from markovs.ConstrainedHiddenMarkovProcess import *
from markovs.ChimpSentenceGenerator import *
from utility.ProcessDataForChimp import *
from constraints.ConstraintStartsWithLetter import *
import pickle


def tongue_twister_chimp(letter: str, file_name: str, size_of_model: int,
                         sentence_iterations: int) -> int:
    """

    :param letter: the letter of the alphabet that we'll use to generate sentences
    :param file_name: the name of the pickle file to read in. We're not going to
        train the dataset every time. We should only need to do that once and then
        load it in.
    :param size_of_model: The number of layers in our model
    :return: int: Returns the number of unique generated sentences
    """
    # Load our Hidden Markov Model
    with open(file_name, 'rb') as handle:
        hidden_markov_model = pickle.load(handle)

    length = size_of_model
    hidden_constraints = []
    observed_constraints = []
    for x in range(length):
        hidden_constraints.append(None)
        observed_constraints.append(ConstraintStartsWithLetter(letter, True, 1))

    # Process the constrained hidden markov model
    chimp = ConstrainedHiddenMarkovProcess(length, hidden_markov_model, hidden_constraints, observed_constraints)
    chimp.process()
    # chimp.print_new_markov_probabilities()

    sentence_generator = ChimpSentenceGenerator(chimp, length)
    sentences = sentence_generator.create_all_sentences(sentence_iterations)
    for sentence in sentences:
        print(sentence)
    # print("Number of sentences:", len(sentences))
    return len(sentences)
