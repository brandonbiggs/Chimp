import random


def get_rand_num(first=0, second=1):
    """
    By default returns a number between 0 and 1
    Wanted to put this in it's own function in case we decide to change
    how randoms are created in the future.
    :param first:
    :param second:
    :return: Number between first and second provided numbers
    """
    return random.uniform(first, second)
