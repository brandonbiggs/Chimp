from markovs.HiddenMarkovModel import *
from markovs_parallel.ChimpParallel import *
from utility.ProcessDataForChimp import *
import time
import pickle


def one_thousand_nodes_parallel(length) -> None:
    """

    :return: None
    """
    with open("pickle_files/hidden_markov.pickle", "rb") as handle:
        data = pickle.load(handle)
    # data = ProcessTextFile("data/book.txt")

    # length = 50

    # Constraints for hidden and observed nodes
    hidden_constraints = []
    observed_constraints = []
    for x in range(length):
        if x % 4 == 0:
            observed_constraints.append(ConstraintContainsString("s", False))
        else:
            observed_constraints.append(None)
        hidden_constraints.append(None)

    # Define our hidden markov model
    hidden_markov_model = HiddenMarkovModel(data.hidden_nodes, data.observed_nodes)
    hidden_markov_model.initial_probs = data.initial_probs
    hidden_markov_model.transition_probs = data.transition_probs
    hidden_markov_model.emission_probs = data.emission_probs
    # print("HMM Finished")

    start = time.time()
    NHHMM = parallel_nhmm(
        length, hidden_markov_model, hidden_constraints, observed_constraints
    )
    NHHMM.process()
    # print("NHHMM Finished")
    end = time.time()
    print("Execution time:", end - start)
