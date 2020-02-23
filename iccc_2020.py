from markovs.ConstrainedHiddenMarkovProcess import *
from markovs.ChimpSentenceGenerator import *
from constraints.ConstraintStartsWithLetter import *
import pickle
import time


def mnemonics_chimp(
    hidden_markov_model, size_of_model: int, sentence_iterations: int,
        observed_constraints: list, result_file_name: str
) -> int:
    """

    :param hidden_markov_model: trained hidden markov model
    :param size_of_model: The number of layers in our model
    :param sentence_iterations
    :param observed_constraints: list of observed constraints
    :return: int: Returns the number of unique generated sentences

    """
    start = time.time()

    # length of the markov model
    length = size_of_model
    hidden_constraints = []
    for x in range(length):
        hidden_constraints.append(None)
        # observed_constraints.append(ConstraintStartsWithLetter(letter, True, 1))

    # Process the constrained hidden markov model
    chimp = ConstrainedHiddenMarkovProcess(
        length, hidden_markov_model, hidden_constraints, observed_constraints
    )
    chimp.process()
    # chimp.print_new_markov_probabilities()

    sentence_generator = ChimpSentenceGenerator(chimp, length)
    sentences = sentence_generator.create_all_sentences(sentence_iterations)
    message = "Test complete. It took " + str(time.time() - start) + " seconds"
    with open(f"results/iccc2020_{result_file_name}.txt", "a") as f:
        print(f"{message}. \nNumber of sentences: {len(sentences)}", file=f)
        for sentence in sentences:
            print(sentence, file=f)

    return len(sentences)


if __name__ == '__main__':

    pickle_file = "pickle_files/iccc_2020.pickle"
    # sentence_iterations = 100000
    sentence_iterations = 100

    # Load our Hidden Markov Model from the pickle file
    with open(pickle_file, "rb") as handle:
        hidden_markov_model = pickle.load(handle)

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
    mnemonics_chimp(hidden_markov_model, size_of_model=size_of_model, sentence_iterations=sentence_iterations,
                    observed_constraints=observed_contraints, result_file_name="dante")