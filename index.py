from utility.interactive import *

# from examples.RedRhyme import red_rhyme
# from examples.RedRhymeMM import red_rhyme_markov_model
# from examples.FirstDog import first_dog
# from examples.RedRhymeMMDynamic import red_rhyme_mm_dynamic
# from examples.RedRhymeDynamic import red_rhyme_dynamic
# from examples.RedRhymeMatrix import red_rhyme_matrix
# from examples.RedRhymeParallel import red_rhyme_parallel
# from examples.ThousandNodes import one_thousand_nodes
# from examples.ThousandNodesParallel import one_thousand_nodes_parallel
# from utility.Utility import *
# from utility.ProcessDataForMM import *
from examples.TongueTwisterChimp import *
from examples.TongueTwisterMarkovModel import *
from result_generation import graph


def tongue_twisters():
    data_file = "data/expressive_graph.txt"
    pickle_file = "pickle_files/test_graph.pickle"
    pickle_mm_file = "pickle_files/test_graph_mm.pickle"
    model = "chimp"
    letter = "a"
    sentence_length = []
    iterations = 1000

    # train(data_file, pickle_file, model, False)
    num_sentences = tongue_twister_chimp(
        letter, pickle_file, sentence_length, iterations
    )
    print("Chimp")
    print(num_sentences)

    # train(data_file, pickle_mm_file, "markovmodel", False)
    num_sentences = tongue_twister_markov_model(
        letter, pickle_mm_file, sentence_length, iterations
    )
    print("Markov Model")
    print(num_sentences)


def graph_results(parameters):
    try:
        graph(
            parameters.get("iterations"),
            parameters.get("sentences"),
            parameters.get("length"),
            parameters.get("data_file"),
            parameters.get("results_file"),
            parameters.get("pickle_file"),
            parameters.get("pickle_mm_file"),
        )
    except:
        print("Error while running the python script! Potentially missing parameters.")


if __name__ == "__main__":
    interactive = InteractiveChimp()
    parameters = interactive.argument_parser()
    graph_results(parameters)

    # print(parameters)

    # print("Hello!")
    # red_rhyme()
    # print("Markov Model Dynamic:")
    # red_rhyme_mm_dynamic()
    # print("CHIMP")
    # red_rhyme_dynamic()
    # print("Markov Model")
    # red_rhyme_markov_model()
    # tongue_twisters()
