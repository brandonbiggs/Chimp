from utility.interactive import *
from utility.Utility import *
from utility.ProcessDataForMM import *
# from utility.SendEmail import SendEmail
from examples.TongueTwisterChimp import *
from examples.TongueTwisterMarkovModel import *
from string import ascii_lowercase
import time


def graph(iterations: int, number_of_sentences: int, sentence_length: int,
          data_file: str, results_file: str, pickle_file: str, pickle_mm_file: str):
    """

    :param iterations:
    :param number_of_sentences:
    :param sentence_length:
    :param data_file:
    :param results_file:
    :param pickle_file:
    :param pickle_mm_file:
    :return:
    """
    results = ""
    chimp_sentences_total = []
    markov_sentences_total = []
    meta_info = "\nData File: " + str(data_file) + " Length: " + str(sentence_length) + " Number of sentences: " + \
                str(number_of_sentences) + "\n"

    for letter in ascii_lowercase:
        chimp_sentences = tongue_twister_chimp(letter, pickle_file, sentence_length, iterations)
        markov_sentences = tongue_twister_markov_model(letter, pickle_mm_file, sentence_length, iterations)
        chimp_sentences_total.append(chimp_sentences)
        markov_sentences_total.append(markov_sentences)

        results += "\nLetter:" + str(letter) + "\nChimp: " + str(chimp_sentences) + \
                   "\nMarkov Sentences: " + str(markov_sentences) + "\n"

    counts = "Total Chimp Counts: " + str(chimp_sentences_total) + \
             "\nTotal Markov Counts: " + str(markov_sentences_total) + \
             "\nChimp Average: " + str(array_average(chimp_sentences_total)) + \
             "\nMarkov Average: " + str(array_average(markov_sentences_total))
    f = open(results_file, "a")
    f.write(meta_info)
    f.write(counts)
    f.write(str(results))
    f.close()


def graph_two():
    iterations = 100000
    number_of_sentences = [25, 250, 2500, 25000, 250000, 2500000]
    sentence_length = [
        2,
        4,
        6,
        8,
        10,
        12,
        14,
        16
    ]
    data_file = "data/book.txt"
    results_file = "results/test_graph3.txt"

    pickle_file = "pickle_files/test_graph2.pickle"
    pickle_mm_file = "pickle_files/test_graph2_mm.pickle"

    for number in number_of_sentences:
        train(number, data_file, pickle_file, "chimp", False)
        train(number, data_file, pickle_mm_file, "markovmodel", False)
        # print("Training finished")
        for length in sentence_length:
            results = ""
            chimp_sentences_total = []
            markov_sentences_total = []
            meta_info = "\nData File: " + str(data_file) + " Length: " + str(length) + " Number of sentences: " + \
                        str(number) + "\n"

            for letter in ascii_lowercase:
                chimp_sentences = tongue_twister_chimp(letter, pickle_file, length, iterations)
                markov_sentences = tongue_twister_markov_model(letter, pickle_mm_file, length, iterations)
                chimp_sentences_total.append(chimp_sentences)
                markov_sentences_total.append(markov_sentences)

                results += "\nLetter:" + str(letter) + "\nChimp: " + str(chimp_sentences) + \
                           "\nMarkov Sentences: " + str(markov_sentences) + "\n"

            counts = "Total Chimp Counts: " + str(chimp_sentences_total) + \
                     "\nTotal Markov Counts: " + str(markov_sentences_total) + \
                     "\nChimp Average: " + str(array_average(chimp_sentences_total)) + \
                     "\nMarkov Average: " + str(array_average(markov_sentences_total))
            f = open(results_file, "a")
            f.write(meta_info)
            f.write(counts)
            # f.write(str(results))
            # f.write(counts)
            f.close()


def graph_one():
    iterations = 10000
    sentence_length = [4, 6, 8, 10]
    data_files = [
                  # "one_sentence.txt",
                  # "four_sentences.txt",
                  # "ten_sentences.txt",
                  # "twenty_five_sentences.txt",
                  # "fifty_sentences.txt",
                  # "one_hundred_sentences.txt",
                  "five_hundred_sentences.txt",
                  # "one_thousand_sentences.txt"
                  ]
    result_file = "results/graph1.txt"
    # data_file = "data/expressive_graph.txt"
    # pickle_file = "pickle_files/test_graph.pickle"
    # pickle_mm_file = "pickle_files/test_graph_mm.pickle"

    for file in data_files:
        data_file = "data/" + file
        pickle_file = "pickle_files/" + str(file).split(".")[0] + ".pickle"
        pickle_mm_file = "pickle_files/" + str(file).split(".")[0] + "_mm.pickle"

        train(data_file, pickle_file, "chimp", False)
        train(data_file, pickle_mm_file, "markovmodel", False)
        for length in sentence_length:
            results = ""
            chimp_sentences_total = []
            markov_sentences_total = []
            meta_info = "\nData File: " + str(file) + " Length: " + str(length) + "\n"

            for letter in ascii_lowercase:
                chimp_sentences = tongue_twister_chimp(letter, pickle_file, length, iterations)
                markov_sentences = tongue_twister_markov_model(letter, pickle_mm_file, length, iterations)
                chimp_sentences_total.append(chimp_sentences)
                markov_sentences_total.append(markov_sentences)

                results += "\nLetter:" + str(letter) + "\nChimp: " + str(chimp_sentences) + \
                          "\nMarkov Sentences: " + str(markov_sentences) + "\n"

            counts = "Total Chimp Counts: " + str(chimp_sentences_total) + \
                "\nTotal Markov Counts: " + str(markov_sentences_total) + \
                "\nChimp Average: " + str(array_average(chimp_sentences_total)) + \
                "\nMarkov Average: " + str(array_average(markov_sentences_total))
            f = open(result_file, "a")
            f.write(meta_info)
            f.write(counts)
            # f.write(str(results))
        # f.write(counts)
            f.close()

if __name__ == '__main__':
    start = time.time()
    # graph_one()
    graph_two()
    message = "Test complete. It took " + str(time.time() - start) + " seconds"
    print(message)
    # email = SendEmail(message)
    # email.send_email()

