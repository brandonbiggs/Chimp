import pronouncing
import nltk
from nltk.corpus import cmudict
from rich import print


# sentence = "and they might have gone on growing" # should be 3
# sentence = "All the things we hide in water" # should be 4
# sentence = "press against the ones we know" # should be 4
# sentence = "if music be the food of love play on" # should be 5
sentence = "there once was a man from nantucket"

# There once was a man from Nantucket
# Who kept all his cash in a bucket.
#     But his daughter, named Nan,
#     Ran away with a man
# And as for the bucket, Nantucket.

def count_syllables(num_syllables: list, phrase: str) -> list:
    cmu_dict = cmudict.dict()
    num_of_syllables = 0
    index = 0
    sub_phrases = []
    sub_phrase = ""
    for word in phrase.split(" "):
        word = word.lower()
        sub_phrase += word + " "
        num_of_syllables = num_of_syllables + [len(list(y for y in x if y[-1].isdigit())) for x in cmu_dict[word]][0]
        if num_of_syllables == num_syllables[index]:
            index += 1
            num_of_syllables = 0 
            sub_phrases.append(sub_phrase.strip())
            sub_phrase = ""
    # print(sub_phrases)
    return sub_phrases

def prettify_and_print_limericks(sentence: str) -> str:
    sub_phrases = count_syllables([8, 8, 5, 5, 8], sentence)
    # print(sub_phrases)
    for phrase in sub_phrases:
        new_phrase = ""
        for word in phrase.split(" "):
            test = pronouncing.phones_for_word(word)
            output = pronouncing.stresses(test[0])
            if output == "1":
                new_phrase += f"[bold]{word}[/bold] "
                # print(f"[bold]{word}[/bold] - {test[0]} - {output}")
            elif output == "0":
                new_phrase += f"{word} "
                # print(f"{word} - {test[0]} - {output}")
            else:
                new_phrase += f"[bold red]{word}[/bold red] "
                # print(f"[bold red]{word}[/bold red] - {test[0]} - {output}")
        print(new_phrase)

sentence = "A matter of free will at stake waited for the cornbread to bake a a sudden spring a silver nose ring a word about the bride 's cake"
sentence = "There once was a man from Nantucket Who kept all his cash in a bucket But his daughter named Nan Ran away with a man And as for the bucket Nantucket"
prettify_and_print_limericks(sentence)