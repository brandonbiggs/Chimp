from rich.pretty import pprint
from rich.json import JSON
from rich import print_json
import json
from bllipparser import RerankingParser
import nltk

def print_sentence_tree(sentence: str) -> None:
    # Sentence parser
    part_of_sentence_labels = ["NP", "VP", "ADVP"]
    while True:
        try:
            parser = RerankingParser.from_unified_model_dir('nltk_data/models/WSJ-PTB3')
            break
        except:
            pass
    try:
        tree_string = parser.simple_parse(sentence)
        sentence_tree = nltk.Tree.fromstring(tree_string)
        print(sentence_tree)
        # for sub_tree in sentence_tree.subtrees():
        #     if sub_tree.label() in part_of_sentence_labels:
        #         token = (" ".join(sub_tree.leaves()), sub_tree.label())
        #         tokenized_text.append(token)            
        # tokens.extend(tokens)
    except IndexError:
        pass

def print_model(model) -> None:
    print("Hidden Markov Model")
    
    print(f"Hidden State Alphabet:")
    # print(model.hidden_nodes)
    # pprint(model.hidden_nodes)
    # print(model.emission_probs.keys())
    pprint(list(model.emission_probs.keys()))
    
    print(f"Emission State Alphabet: ")
    pprint(model.observed_nodes)
    
    print(f"Initial Probabilities: ")
    pprint(model.initial_probs)
    
    print(f"Transition Probabilities:")
    pprint(model.transition_probs)
    
    print(f"Emission Probabilities")
    pprint(model.emission_probs)
    
    print(f"Markov Order: {model.markov_order}")

def model_to_json(model, markov_order: int = 1, output_file: str = None) -> None:
    data = None
    if markov_order != 1:
        print("Printing for Markov order != 1 is not yet implemented.")
    elif markov_order == 1:
        initial_probs = {}
        transition_probs = {}
        for key, value in model.initial_probs.items():
            initial_probs[key[0]] = value
        for key, value in model.transition_probs.items():
            probs = {}
            for key_2, value_2 in value.items():
                probs[key_2[0]] = value_2
            transition_probs[key[0]] = probs
        data = {
            "Observed Nodes": model.observed_nodes, 
            "Hidden Nodes": model.hidden_nodes, 
            "Initial Probabilities": initial_probs,
            "Transition Probabilities": transition_probs,
            "Emission Probabilities": model.emission_probs, 
            "Markov Order": model.markov_order
        }
    if data and output_file:
        with open(output_file, "w") as report_file:
            json.dump(data, report_file, indent=4)
    elif data:   
        print_json(data=data)

def print_chimp_markov_probabilities(model) -> None:
    """
    Debugging function to print out info about the NHHMM
    :return: None
    """
    for node_layer in range(model.layers):
        print(f"\nObserved layer {node_layer} of the NHHMM")
        print("Beta list: ")
        pprint(model.observed_node_betas[node_layer])
        
        print(f"Emission Probabilities:")
        pprint(model.constrained_observed_emission_probabilities[node_layer])

        print("Hidden Layer:", node_layer)
        if node_layer != 0:
            print("Transition Probabilities:")
            pprint(model.constrained_transition_probabilities[node_layer])
        else:
            print("Initial Probabilities:")
            pprint(model.constrained_transition_probabilities[node_layer])