# These used to be in models/CHiMP.py but they weren't being used anywhere so I removed them, but wanted
#       to keep the code..

def get_total_solution_count(self) -> int:
    """
    Counts the total solutions possible using a depth first search via
    recursive functions
    """
    count = [0]  # total solution count
    
    # Find possible initial hidden states (non-zero probabilities)
    initial_hidden_states = self.constrained_transition_probabilities[0]

    # Count layer 0 initials for progress indicator
    total_initials = 0
    for hidden_state in initial_hidden_states.keys():
        if initial_hidden_states[hidden_state] > 0.0:
            total_initials += 1


    i = 0 # used for progress
    for hidden_state in initial_hidden_states.keys():
        if initial_hidden_states[hidden_state] > 0.0:
            i += 1
            print("- progress \033[33m%s\033[0m, %d/%d, %s" % (datetime.datetime.now().strftime("%H:%M:%S"), i, total_initials, hidden_state))
            # Call recursive counting function on each non-zero hidden state
            self.get_total_solution_count_emission_impl(hidden_state, 0, count, [])
    
    return count[0]

def get_total_solution_count_hidden_impl(self, previous_hidden_state: dict, layer_index: int,
                                            count: List[int], solution: List[str]):
    """
    Finds hidden states based on the previous hidden state

    Forms a recursive function pair with it's emission counterpart function:
    get_total_solution_count_emission_impl()

    :param previous_hidden_state: the hidden state from the previous layer
    :param layer_index: indicates the current layer
    :param count: total solution count (is an array as a way to passed by reference)
    """
    transition_probs = self.constrained_transition_probabilities[layer_index]

    # Find possible hidden states transitioning from previous hidden state
    for hidden_state in transition_probs[previous_hidden_state]:
        # Call recursive emission function for each hidden state
        self.get_total_solution_count_emission_impl(hidden_state,
                                                    layer_index,
                                                    count,
                                                    solution)

def get_total_solution_count_emission_impl(self,
                                            hidden_state: dict,
                                            layer_index: int,
                                            count: List[int],
                                            solution: List[str]):
    """
    Finds emission states based on the given hidden state and counts them
    towards total solutions if on the last layer

    Forms a recursive function pair with it's hidden counterpart function:
    get_total_solution_count_hidden_impl()

    :param hidden_state: the hidden state by which the emission should be chosen
    :param layer_index: indicates the current layer
    :param count: total solution count (is an array as a way to passed by reference)
    """
    emission_probs = self.constrained_observed_emission_probabilities[layer_index]

    for emission in emission_probs[hidden_state[-1]]:
        # Print emission for testing
        # self.print_emission(emission, hidden_state, layer_index);
        # solution.append(emission)

        # If at last layer, increment for each possible emission
        if layer_index == self.layers-1:
            count[0] += 1

        else:
            self.get_total_solution_count_hidden_impl(hidden_state,
                                                        layer_index+1,
                                                        count,
                                                        solution + [emission])

def print_emission(self, emission: str, hidden_state: str, layer_index: int):
    """
    Prints emission string indented according to it's layer
    
    This function is for testing and visualizing the
    recursive total solution count functions

    :param emission: emission string
    :param hidden_state: hidden state string
    :param layer_index: layer the emission occurs at
    """
    for _ in range(layer_index):
        print('   ', end='')
    print('\033[34m%d \033[33m%s\033[0m %s' % (layer_index+1, hidden_state, emission))
