from utility.interactive import *
from utility.ProcessDataForMM import *
from examples.RedRhyme import red_rhyme
from examples.RedRhymeMM import red_rhyme_markov_model
from examples.FirstDog import first_dog
from examples.RedRhymeMMDynamic import red_rhyme_mm_dynamic
from examples.RedRhymeDynamic import red_rhyme_dynamic
from examples.RedRhymeMatrix import red_rhyme_matrix
from examples.RedRhymeParallel import red_rhyme_parallel
from examples.ThousandNodes import one_thousand_nodes
from examples.ThousandNodesParallel import one_thousand_nodes_parallel

if __name__ == '__main__':
    # test = ProcessDataForMM("data/ccil.txt", False)
    # test.debug_print()
    print("Markov Model Dynamic:")
    red_rhyme_mm_dynamic()
    print("CHIMP")
    red_rhyme()
    # print("Markov Model")
    # red_rhyme_markov_model()




