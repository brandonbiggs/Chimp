from __init__ import *
from examples.FirstDog import *
from examples.BusyLiving import *
from examples.BusyLivingDynamic import *
from examples.RedRhyme import *
from utility.Utility import *
from utility.ProcessDataForChimp import *
from markovs.HiddenMarkovModel import HiddenMarkovModel
from markovs.ConstrainedHiddenMarkovProcess import ConstrainedHiddenMarkovProcess
from markovs.ChimpSentenceGenerator import ChimpSentenceGenerator
import argparse
import time
import pickle
from pathlib import Path


class InteractiveChimp:
    def __init__(self):
        pass

    @staticmethod
    def interactive_graph(args):
        parameters = {}
        # print(args)
        for arg in args:
            item = arg.split(":")
            if item[1].isdigit():
                parameters.update({item[0]: int(item[1])})
            else:
                parameters.update({item[0]: item[1]})
        # print(parameters)
        return parameters

    @staticmethod
    def run_examples(example=1, size=7) -> None:
        """
        # TODO - Add more to these
        :param example:
        :param size:
        :return:
        """
        if example == 1:
            first_dog()
        elif example == 2:
            busy_living()
        elif example == 3:
            busy_living_dynamic(size)
        else:
            first_dog()

    @staticmethod
    def run_interactive(
        layers,
        hidden_constraints,
        observed_constraints,
        output_sentences,
        file_name="pickle_files/hmm.pickle",
    ) -> None:
        """
        TODO - Parse the constraint arrays
        :param layers:
        :param hidden_constraints:
        :param observed_constraints:
        :param output_sentences:
        :param file_name:
        :return:
        """

        # Load data (deserialize)
        with open(file_name, "rb") as handle:
            hidden_markov_model = pickle.load(handle)
        print("Loaded the hidden markov model.")

        # Parse Hidden Constraints
        for i in range(layers):
            try:
                if hidden_constraints[i] in nltk_tags.keys():
                    hidden_constraints[i] = ConstraintIsPartOfSpeech(
                        hidden_constraints[i], True
                    )
                else:
                    hidden_constraints[i] = None
            except:
                hidden_constraints.append(None)
        print("hidden constraints:", hidden_constraints)

        # Parse Observed Constraints
        # observed_constraints = []
        for i in range(layers):
            try:
                if observed_constraints[i].isalpha():
                    observed_constraints[i] = ConstraintContainsString(
                        observed_constraints[i], True
                    )
                else:
                    observed_constraints[i] = None
            except:
                observed_constraints.append(None)
        print("observed constraints:", observed_constraints)

        NHHMM = ConstrainedHiddenMarkovProcess(
            layers, hidden_markov_model, hidden_constraints, observed_constraints
        )
        NHHMM.process()
        print("NHHMM Finished.")

        print("Generated Sentences:")
        sentence_generator = ChimpSentenceGenerator(NHHMM, layers)
        for x in range(output_sentences):
            print(sentence_generator.create_sentence())

    def interactive(self) -> None:
        """
        TODO - Add option for selecting a new file to train on
        :return: None
        """
        print("Welcome to the interactive version of the NHHMM program!")

        # Training question
        train_again = input(
            "Would you like to retrain the model? Retraining "
            "the model will take some time. (y/n) "
        )
        train_again = train_again.lower()
        if train_again == "y":
            train_again = input("Would you like to train with a new input file? (y/n) ")
            if train_again == "y":
                enter_file = True
                while enter_file:
                    path = input("Please enter absolute path to the new input file: ")
                    config = Path(path)
                    if config.is_file():
                        print("Training on new file that was provided.")
                        enter_file = False
                        train(path)
                    else:
                        print("Error with the file.")
            else:
                # Keep presets
                train()

        # Node Size question
        size = True
        size_of_model = 1
        while size:
            size_of_model = input("How many nodes are in your model (1-15)? ")
            try:
                size_of_model = int(size_of_model)
                if 15 >= size_of_model > 0:
                    size = False
            except ValueError:
                print("Please enter a number between 1 and 15.")

        # Hidden Constraint Question
        hidden = input("Any hidden constraints? (y/n) ")
        hidden_constraints = ""
        if hidden == "y":
            print("See interactive.py --hidden for more information.")
            hidden_constraints = input("Hidden constraints: ")
            print(hidden_constraints.split(" "))

        # Observed constraint question
        observed = input("Any observed constraints? (y/n) ")
        observed_constraints = ""
        if observed == "y":
            print("See interactive.py --observed for more information.")
            observed_constraints = input("Observed constraints: ")
            print(observed_constraints.split(" "))

        # Number of sentences output
        sentences = True
        num_output_sentences = 5
        while sentences:
            num_output_sentences = input("How many sentences to output? ")
            try:
                num_output_sentences = int(num_output_sentences)
                if num_output_sentences > 0:
                    sentences = False
            except ValueError:
                print("Please enter a number greater than 0.")

        self.run_interactive(
            size_of_model,
            hidden_constraints.split(" "),
            observed_constraints.split(" "),
            num_output_sentences,
        )

    def argument_parser(self) -> None:
        """

        :return: None
        """
        parameter = False
        hidden_flag = (
            "This --hidden flag provides more information about "
            "the interactive command line utility for setting "
            "hidden nodes."
        )
        observed_flag = (
            "This --observed flag provides more information about "
            "the interactive command line utility for setting "
            "observed nodes."
        )
        description = (
            "Run a NHHMM model. The --help, --train, --example, "
            "--interactive parameters cannot be run at the same time."
        )

        parser = argparse.ArgumentParser(description=description)
        # Done
        parser.add_argument(
            "-c",
            "--clock",
            help="Time the execution of the program.",
            action="store_true",
        )
        parser.add_argument(
            "-e",
            "--example",
            nargs="?",
            const=1,
            help="Run a specific example.",
            type=int,
            metavar="1, 2, 3",
        )
        parser.add_argument(
            "-g", "--graph", nargs="+", help="Run a graph generating result"
        )
        parser.add_argument("--hidden", action="store_true", help=hidden_flag)
        parser.add_argument(
            "-i",
            "--interactive",
            help="run the model in an interactive mode. (Not yet ready)",
            action="store_true",
        )
        parser.add_argument("--observed", action="store_true", help=observed_flag)
        parser.add_argument(
            "-t",
            "--train",
            help="Train the Hidden Markov Model. "
            "A file may be passed. A default source"
            "will be trained otherwise.",
            type=str,
            metavar="file name",
            nargs="?",
            const="data/book_tiny.txt",
        )
        # Done
        parser.add_argument(
            "--tags", action="store_true", help="Print the NLTK POS tags and exit."
        )
        # Done
        parser.add_argument(
            "--tags-nice",
            action="store_true",
            help="Print nicely the NLTK POS tags and exit.",
        )
        # Done
        parser.add_argument(
            "-V", "--version", action="version", version="%(prog)s {}".format(version)
        )

        args = parser.parse_args()

        # -g --graph
        if args.graph:
            return self.interactive_graph(args.graph)

        # --tags Print the NLTK Tags
        if args.tags:
            print(nltk_tags)
            parameter = True

        # --tags-nice
        if args.tags_nice:
            for key in nltk_tags.keys():
                print(key, nltk_tags.get(key))
                parameter = True

        # --observed
        # TODO - Test more
        if args.observed:
            parameter = True
            # Print the observed node input info
            print(
                "The constraints you can put on observed nodes: "
                "constraint_must_contain_letter"
            )
            print(
                "Enter a letter(s) or 'None'. Enter the same number of observed"
                "constraints or 'None' as you entered for layers."
            )
            print("The following will put constraints on the 2nd and 4th node layers.")
            print("Example: None t None s None")

        # --hidden
        if args.hidden:
            parameter = True
            # Print the hidden node input info
            print(
                "The constraints you can put on hidden nodes: \n"
                "constraint_must_be_part_of_speech"
            )
            print(
                "Enter the NLTK part of speech tag or 'None'. "
                "Enter the same number of hidden constraints or 'None' as "
                "you entered for layers."
            )
            print("The following will put constraints on the 1st and 4th node layers.")
            print("Example: NN None None VB None")
            print("For a list of NLTK tags, use the parameter --tags")

        # --timer
        if args.clock:
            print("Starting timer.")
            start = time.time()

        # --interactive
        if args.interactive:
            # Run the model interactively
            self.interactive()

        # --example
        elif args.example is not None:
            example = args.example
            if example == 1:
                first_dog()
            elif example == 2:
                busy_living()
            else:
                print("Sorry, that example doesn't exist yet.")

        # --train
        elif args.train:
            file_name = args.train
            if file_name:
                # todo - update these functions
                train(file_name)
            else:
                train()

        # none
        else:
            if not parameter:
                # No parameters
                print("No run parameters!")

        # --timer
        if args.clock:
            end = time.time()
            print("Execution time:", end - start)

        return None

    @staticmethod
    def sanitize_inputs(self, question) -> str:
        """
        TODO
        Gets the input from the user and ensures that it doesn't have anything
            we don't want in it, such as symbols, etc.
        :param self:
        :param question:
        :return:
        """
        user_input = ""
        return user_input
