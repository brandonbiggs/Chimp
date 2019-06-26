from utility.interactive import *
from examples.RedRhyme import red_rhyme
from examples.RedRhymeMM import red_rhyme_markov_model
from examples.FirstDog import first_dog
from examples.RedRhymeDynamic import red_rhyme_dynamic
from examples.RedRhymeMatrix import red_rhyme_matrix
from examples.RedRhymeParallel import red_rhyme_parallel
from examples.ThousandNodes import one_thousand_nodes
from examples.ThousandNodesParallel import one_thousand_nodes_parallel

if __name__ == '__main__':
    # red_rhyme_matrix()
    print("CHIMP")
    red_rhyme()
    print("Markov Model")
    red_rhyme_markov_model()
    # length = 1000
    # print("Not parallel.")
    # one_thousand_nodes(length)
    # print("Parallel.")
    # one_thousand_nodes_parallel(length)
    # red_rhyme_parallel()

    # print("\n\n\n")
    # print("Red Rhyme Parallel.")
    # start = time.time()
    # red_rhyme_parallel()
    # end = time.time()
    # print("Execution time:", end - start)

    # first_dog()
    # red_rhyme_dynamic()
    # print("Red Rhyme Not Parallel.")
    # start = time.time()
    # red_rhyme()
    # end = time.time()
    # print("Execution time:", end - start)
    # InteractiveNHHMarkov().argument_parser()


