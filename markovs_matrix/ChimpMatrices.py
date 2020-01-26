import copy
from constraints.ConstraintContainsString import *
from constraints.ConstraintIsPartOfSpeech import *
from constraints.ConstraintMatchesString import *
from constraints.ConstraintRhymesWith import *
from constraints.NoConstraint import *
import numpy


class NonHomogeneousHMMMatrix:
    """
    This is a hidden markov model that we are applying constraints to. You're
        currently able to apply ONE constraint per node to any node in the graph.
    """

    hidden_markov_model = None
    layers = 0
    hidden_constraints = []
    observed_constraints = []
    beginning_alpha = numpy.array([])
    # observed_node_betas = numpy.array([])
    # constrained_observed_emission_probabilities = numpy.array([])
    # constrained_transition_probabilities = numpy.array([])
    observed_node_betas = []
    constrained_observed_emission_probabilities = []
    constrained_transition_probabilities = []

    def __init__(
        self,
        layers: int,
        hidden_markov_model,
        hidden_constraints: list,
        observed_constraints: list,
        num_pos: int,
        num_words: int,
    ):
        """
        :param layers: Defines number of hidden/observed nodes in graph
        :param hidden_markov_model: the hmm we're applying constraints to
        :param hidden_constraints: list of constraints in the hidden nodes
        :param observed_constraints: list of constraints in the observed nodes
        """
        self.layers = layers
        self.hidden_markov_model = hidden_markov_model
        self.hidden_constraints = hidden_constraints
        self.observed_constraints = observed_constraints

        # Create the default value of 1 for alpha
        self.beginning_alpha = numpy.arange(num_pos * num_pos).reshape(num_pos, num_pos)
        self.beginning_alpha = numpy.ones_like(self.beginning_alpha)

        #
        # for key in hidden_markov_model.transition_probs.keys():
        #     self.beginning_alpha[key] = 1

        # TODO - Figure out if these are actually doing anything. They seem a little
        #       weird. I thought there should be more of them than there are... We'll
        #       see what happens as I progress.
        # Setting default values for beta, emission probabilities, transitions
        for layer in range(layers):
            self.observed_node_betas.append(0)
            self.constrained_observed_emission_probabilities.append(0)
            self.constrained_transition_probabilities.append(0)

    def print_new_markov_probabilities(self) -> None:
        """
        Debugging function to print out info about the NHHMM
        """
        for node_layer in range(self.layers):
            print("\nObserved layer", node_layer, "of the NHHMM")
            print("Beta list:", self.observed_node_betas[node_layer])
            print(
                "Emission Probabilities:",
                self.constrained_observed_emission_probabilities[node_layer],
            )

            print("Hidden Layer:", node_layer)
            if node_layer != 0:
                print(
                    "Transition Probabilities:",
                    self.constrained_transition_probabilities[node_layer],
                )
            else:
                print(
                    "Initial Probabilities:",
                    self.constrained_transition_probabilities[node_layer],
                )

    def process(self) -> None:
        """
        Iterate through the hidden and observed nodes starting with the last
            observed node, then moving to the last hidden and working in reverse
        """
        # We need to deep copy this as we'll be editing it throughout to create
        #       a new set of transition probabilities at each node
        transition_probs = copy.deepcopy(self.hidden_markov_model.transition_probs)

        # We can calculate all of the betas for the observed layers before we
        #       have to worry about calculating the new probabilities in the
        #       hidden layers. This can also be done in parallel. Doesn't have to
        #       happen in reverse. Order of calculation doesn't matter for these
        # 1. Update and normalize probabilities in observed node
        # 2. Prune the empty values in the observed node
        # 3. Store new emission probabilities and calculated beta values
        for node_layer in range(self.layers - 1, -1, -1):
            print("LAYER:", node_layer)
            observed_output = self.process_observed_node(node_layer)
        #     output = self.prune_empty_dictionary_keys(observed_output[0])
        #     self.constrained_observed_emission_probabilities[node_layer] = output
        #     self.observed_node_betas[node_layer] = observed_output[1]
        #
        # # After we've calculated all of the betas for the observed nodes, we can
        # #       now calculate the hidden nodes. This cannot be done in parallel
        # #       as the node at i-1 depends on node at i up to the last node that
        # #       has a constraint. Because of this, we must start at the last node.
        # for node_layer in range(self.layers - 1, -1, -1):
        #
        #     # If it's the initial node, we use the initial probabilities instead
        #     #       of the transition probabilities
        #     if node_layer == 0:
        #         hidden_output = \
        #             self.process_hidden_node(node_layer,
        #                                      self.observed_node_betas[node_layer],
        #                                      self.beginning_alpha,
        #                                      self.hidden_markov_model.initial_probs)
        #     # If not initial node, use transition probabilities
        #     else:
        #         hidden_output = \
        #             self.process_hidden_node(node_layer,
        #                                      self.observed_node_betas[node_layer],
        #                                      self.beginning_alpha,
        #                                      transition_probs)
        #     # Update the alpha values
        #     self.beginning_alpha = hidden_output[0]
        #
        #     # Update the transition probabilities
        #     transition_probs = \
        #         self.prune_transition_probabilities(hidden_output[1], node_layer)
        #     self.constrained_transition_probabilities[node_layer] = transition_probs

    def process_hidden_node(
        self,
        node_position: int,
        beta_dict: dict,
        previous_alpha: dict,
        transition_probs: dict,
    ) -> (dict, dict):
        """
        Processes the hidden layer at the given node_position layer
        :param node_position: the node layer we're calculating
        :param beta_dict: dictionary of beta values, one for each POS
        :param previous_alpha: dictionary of previous alpha values
        :param transition_probs: transition probabilities for each POS -> every
                    other part of speech
        :return: two dictionaries. First is the dictionary of alphas that this
                    node calculated. Second is the new normalized transition
                    probabilities
        """

        # Check constraints
        constraint = self.hidden_constraints[node_position]
        if constraint is None:
            constraint = NoConstraint

        # Make a deep copy of the previous alpha dictionary
        alpha_copy = copy.deepcopy(previous_alpha)
        new_transition_probs = {}

        # Use Initial probabilities instead of transition probabilities
        if node_position == 0:
            m_tilde = self.calculate_m_tilde(
                transition_probs, constraint, beta_dict, alpha_copy
            )
            return previous_alpha, m_tilde[0]
        else:
            # Iterate over the remaining keys from transition probabilities
            for key in self.hidden_markov_model.transition_probs.keys():
                # Calculate new M value
                m_tilde = self.calculate_m_tilde(
                    self.hidden_markov_model.transition_probs.get(key),
                    constraint,
                    beta_dict,
                    alpha_copy,
                )
                previous_alpha[key] = m_tilde[1]

                # Formulate the new transition probabilities
                new_transition_probs = self.update_new_transition_probs(
                    key, m_tilde[0], new_transition_probs
                )

        return previous_alpha, new_transition_probs

    def process_observed_node(self, node_position: int) -> (dict, dict):
        """
        Calculates the new probabilities of observed nodes if a constraint exists
        :param node_position: layer in the graph
        :return: dictionary of new probabilities
        """

        # Keeps track of the calculated beta values
        beta_dict = numpy.array([])

        # Gets the constraint if one exists
        constraint = self.observed_constraints[node_position]

        # If constraint does exist, we need to calculate the new probabilities
        if constraint:
            new_emission_probs = numpy.array([])
            # Iterate through each value in the emissions probability at node position
            for value in range(
                numpy.size(self.hidden_markov_model.emission_probs[node_position], 1)
            ):
                print(value, end=" ")
                print(self.hidden_markov_model.emission_probs[node_position][:, value])
                # e_tilde = self.calculate_e_tilde(value, constraint)
                # print(e_tilde)
            # Iterate over each key to calculate new emission probabilities
        #     for key in self.hidden_markov_model.emission_probs.keys():
        #         e_tilde = self.calculate_e_tilde(
        #             self.hidden_markov_model.emission_probs.get(key), constraint)
        #         new_emission_probs[key] = e_tilde[0]
        #         beta_dict[key] = e_tilde[1]
        #     return new_emission_probs, beta_dict
        #
        # # If no constraint exists, we return unaltered beta values
        # else:
        #     for key in self.hidden_markov_model.emission_probs.keys():
        #         beta_dict[key] = 1
        #     return self.hidden_markov_model.emission_probs, beta_dict

    @staticmethod
    def calculate_beta(dictionary: dict) -> int:
        """
        The sum of all probabilities of an observed node.
        :param dictionary:
        :return: sum that will be used for normalizing
        """
        summation = 0
        for key in dictionary.keys():
            summation += dictionary.get(key)
        return summation

    def calculate_e_tilde(
        self, values: numpy.array([]), constraint: Constraint
    ) -> (numpy.array([]), int):
        """
        Calculates the new emission probabilities based on constraints
            Potential ways to make faster - write check for constraint if it's
            no constraint, don't even iterate over the dictionary.
        :param values: numpy array. This is the part of speech column in the emission
            probability multidimensional array
        :param constraint: constraint that placed on the node layer
        :return: new list of emission probabilitiy
        """
        # Make a copy so we can delete values that aren't satisfied by constraint
        new_normalized_probabilities = copy.deepcopy(values)
        for key in dictionary:
            status = constraint.is_satisfied_by_state(key)
            if not status:
                del new_normalized_probabilities[key]

        # Get the sum value for normalizing
        beta = self.calculate_beta(new_normalized_probabilities)

        # Normalize values
        for key in new_normalized_probabilities.keys():
            new_normalized_probabilities[key] = (
                new_normalized_probabilities.get(key) / beta
            )

        # Return the new normalized emission probabilities and the beta value
        return new_normalized_probabilities, beta

    def calculate_m_tilde(
        self, dictionary: dict, constraint, beta_dict: dict, previous_alpha_dict: dict
    ) -> (dict, int):
        """
        Calculates the new transition probabilities between the hidden nodes
            given any constraints in either/both the hidden and observed nodes
        :param dictionary:
        :param constraint:
        :param beta_dict:
        :param previous_alpha_dict:
        :return: (dict, int)
        """
        normalized_transition_probabilities = copy.deepcopy(dictionary)

        # Apply the constraint to a new dictionary
        for key in dictionary:
            status = constraint.is_satisfied_by_state(key)
            if not status:
                del normalized_transition_probabilities[key]

        # Calculate the alpha value
        alpha = self.calculate_alpha(
            normalized_transition_probabilities, beta_dict, previous_alpha_dict
        )

        # Calculate the m_j_k values
        for key in normalized_transition_probabilities.keys():
            if alpha == 0:
                normalized_transition_probabilities[key] = 0
            else:
                previous_alpha = previous_alpha_dict.get(key)
                beta = beta_dict.get(key)
                z = normalized_transition_probabilities.get(key)
                normalized_transition_probabilities[key] = (
                    beta * z * previous_alpha
                ) / alpha
        return normalized_transition_probabilities, alpha

    @staticmethod
    def calculate_alpha(dictionary: dict, beta_dict: dict, previous_alpha: dict) -> int:
        """
        Calculates the alpha value for the hidden nodes
        :param dictionary:
        :param beta_dict:
        :param previous_alpha:
        :return: int
        """
        summation = 0
        for key in dictionary.keys():
            if type(previous_alpha.get(key)) is None or previous_alpha.get(key) is None:
                previous_alpha[key] = 0
                alpha = 0
            else:
                alpha = previous_alpha.get(key)
            if not beta_dict.get(key):
                beta = 0
            else:
                beta = beta_dict.get(key)
            z = dictionary.get(key)
            # print("Z", z, "beta", beta, "alpha", alpha)
            summation += z * beta * alpha
        return summation

    @staticmethod
    def update_new_transition_probs(
        key: str, dictionary: dict, new_transition_dict: dict
    ) -> dict:
        """
        Create a new set of transition probabilities from one hidden node layer
        to the previous hidden node layer
        :param key:
        :param dictionary:
        :param new_transition_dict:
        :return: dict
        """
        new_transition_dict[key] = dictionary
        return new_transition_dict

    @staticmethod
    def prune_empty_dictionary_keys(output: dict) -> dict:
        """
        This iterates through a dictionary and deletes any keys that do not have
            values
        :param output:
        :return:
        """
        new_output = copy.deepcopy(output)
        for key in output.keys():
            if not output.get(key):
                del new_output[key]
        return new_output

    def prune_transition_probabilities(self, output: dict, node_layer: int) -> dict:
        """
        Iterates over dictionary to check for blank values and removed them
        Once it removes all of that values that are zero, prune any empty dictionary
            keys as well
        :param output:
        :param node_layer:
        :return: dict
        """
        if node_layer != 0:
            new_output = copy.deepcopy(output)
            for key in output.keys():
                for inner_key in output.get(key).keys():
                    if output.get(key).get(inner_key) == 0:
                        del new_output.get(key)[inner_key]
            new_output = self.prune_empty_dictionary_keys(new_output)
            return new_output
        # Don't prune initial probabilities
        else:
            return output
