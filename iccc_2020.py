from markovs.ConstrainedHiddenMarkovProcess import *
from markovs.ChimpSentenceGenerator import *
from constraints.ConstraintStartsWithLetter import *
import pickle
import time
import datetime
import sys

from utility.Utility import *
from utility.CountSentences import *


def main():
    """
    Main function
    """

    # defaults
    should_create_pickle = False
    should_get_total_solutions = False
    should_use_comp = False
    sentence_count = 4

    data_file = 'data/red_rhyme.txt'
    pickle_file = 'pickle_files/red_rhyme.pickle'
    constraint = ''
    results_file = 'results/red_rhyme.txt'

    # Capture arugments
    if len(sys.argv) == 1:
        print("Usage: iccc_2020.py [--create-pickle, --perform-dfs, --comp] -n sentence_count -i data_file -p pickle_file -c constraint -o results_file")
        print("Example: iccc_2020.py --create-pickle --perform-dfs -n 100 -i data/2012_fic.txt -p pickle_files/iccc_2020_dante_100.pickle -c \"LLGGAHVFT\" -o results/icc_2020_dante.txt")
        exit(1)

    for i in range(1, len(sys.argv)):
        if sys.argv[i] == '--create-pickle':
            should_create_pickle = True
        elif sys.argv[i] == '--perform-dfs':
            should_get_total_solutions = True
        elif sys.argv[i] == '--comp':
            should_use_comp = True
        elif sys.argv[i] == '-n':
            sentence_count = int(sys.argv[i+1])
        elif sys.argv[i] == '-i':
            data_file = sys.argv[i+1]
        elif sys.argv[i] == '-p':
            pickle_file = sys.argv[i+1]
        elif sys.argv[i] == '-c':
            constraint = sys.argv[i+1]
        elif sys.argv[i] == '-o':
            results_file = sys.argv[i+1]

    if should_create_pickle:
        create_new_pickle(sentence_count=sentence_count,
                        data_file=data_file,
                        pickle_file=pickle_file,
                        model='chimp' if not should_use_comp else 'markovmodel')

    # Name of the pickle file to reduce train time. If you run the train function above,
    # make sure you change the below pickle file to match the new trained pickle file :)
    # pickle_file = "pickle_files/iccc_2020.pickle"

    # Number of unique solutions to look for
    # sentence_iterations = 100000
    sentence_iterations = 10

    # Load our Hidden Markov Model from the pickle file
    with open(pickle_file, "rb") as handle:
        hidden_markov_model = pickle.load(handle)

    # # Red rhyme
    # size_of_model = 4
    # observed_constraints = [
    #     ConstraintRhymesWith("red", True),
    #     None,
    #     None,
    #     ConstraintMatchesString("red", True),
    # ]

    # Create constraints
    if should_use_comp:  # for CoMP
        # Dynamically set problem
        size_of_model = len(constraint)
        hidden_constraints = []
        for letter in constraint:
            hidden_constraints.append(ConstraintStartsWithLetter(letter, True, 1))

        # Create a blank observed constraint list
        observed_constraints = []
        for x in range(size_of_model):
            observed_constraints.append(None)
    else:  # for CHiMP
        # Dynamically set problem
        size_of_model = len(constraint)
        observed_constraints = []
        for letter in constraint:
            observed_constraints.append(ConstraintStartsWithLetter(letter, True, 1))

        # Create a blank hidden constraint list
        hidden_constraints = []
        for x in range(size_of_model):
            hidden_constraints.append(None)

    mnemonics_chimp(hidden_markov_model, size_of_model=size_of_model, sentence_iterations=sentence_iterations,
                    observed_constraints=observed_constraints, hidden_constraints=hidden_constraints,
                    result_file_name=results_file, constraint_str=constraint,
                    should_get_total_solutions=should_get_total_solutions,
                    training_sentence_count=sentence_count)


def mnemonics_chimp(
    hidden_markov_model, size_of_model: int, sentence_iterations: int,
    observed_constraints: list, hidden_constraints: list, result_file_name: str,
    constraint_str: str, should_get_total_solutions: bool,
    training_sentence_count: int):
    """

    :param hidden_markov_model:
    :param size_of_model:
    :param sentence_iterations:
    :param observed_constraints:
    :param hidden_constraints:
    :param result_file_name:
    :return:
    """

    # Process the constrained hidden markov model - This is the CHIMP algorithm
    chimp = ConstrainedHiddenMarkovProcess(
        size_of_model, hidden_markov_model, hidden_constraints, observed_constraints
    )
    chimp.process()

    # Can print out the probabilities if you'd like
    # chimp.print_new_markov_probabilities()

    sentence_generator = ChimpSentenceGenerator(chimp, size_of_model)
    sentences = sentence_generator.create_all_sentences(sentence_iterations)

    # Print to results file
    if should_get_total_solutions:  # print <total solutions>, <training sentence count> to file
        # Print progress to std output
        print("Progress! Sample sentences(%d) for %s" % (len(sentences), constraint_str))
        for sentence in sentences:
            print("  %s" % (sentence))

        print("Starting DFS at \033[34m%s\033[0m" \
            % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        start = time.time()

        total_solutions = chimp.get_total_solution_count()  # Perform DFS

        print("Finished in \033[34m%s \033[0mminutes" % ((time.time() - start) / 60))
        print("\033[34m%d \033[0mtotal solutions for \033[34m%d \033[0mtraining sentences" \
            % (total_solutions, training_sentence_count))
        print("Writing to results/iccc2020_%s" % result_file_name)
        print()

        with open(f"{result_file_name}", "a") as f: 
            print("%s, %d" % (constraint_str, total_solutions), file=f)
    else:  # just print sentences to file
        print("Writing to results/iccc2020_%s" % result_file_name)
        print()
        with open(f"{result_file_name}", "a") as f:
            for sentence in sentences:
                print("  %s" % (sentence), file=f)


def create_new_pickle(sentence_count: int, data_file: str, pickle_file: str, model: str):
    """
    :param sentence_count: How many sentences to train on
    :param data_file: training data file path
    :param pickle_file: new pickle file path
    """

    # Pulls in the sentences and cleans the data. Isn't perfect
    contents = utility.CountSentences.CountSentences(data_file)

    # Narrows down the number of sentences we want
    file_contents = contents.sentence_list_as_string(
        contents.get_sentences(sentence_count)
    )

    # Trains the HMM and stores it in pickle_file
    train(number_of_sentences=sentence_count,
          text_file=file_contents,
          pickle_file=pickle_file,
          model=model,
          text_contents=True)


if __name__ == '__main__':
    main()
