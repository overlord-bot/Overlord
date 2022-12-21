from time import time
from random import randrange


def generate_semi_rand_id():
    '''
    TODO maybe use a generator class to control the last portion
    just in case of the unlikely case of two ids generated at the same time
    that chooses the same random number.

    Returns
    -------
    Returns a string that is the semi-random id.
      The first 8 characters are the seconds from epoch
      and the last 1-8 characters are a random number.

    '''
    return f"{hex(int(time()))[2:]}={hex(randrange(0, 4294967295))[2:]}"
