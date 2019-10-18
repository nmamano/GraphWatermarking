"""
keygen function from algorithm 2
"""
import random
from utils import list_head_to_string

def key_to_string(key, max_items=10):
    """
    returns a string representing the key
    """
    return list_head_to_string(key, max_items)

def key_gen(key_size, max_flips_per_node, num_high_and_med):
    """
    num_high_and_med: the total number of high- and medium-degree vertices
    returns a lexicographically sorted list of 2-tuples,
    with the indices in the tuples in increasing order
    """
    assert (max_flips_per_node == 1 and num_high_and_med >= key_size*2) or \
           num_high_and_med*max_flips_per_node > key_size*2
    # if max_flips_per_node > 1 and num_high_and_med*max_flips_per_node == key_size*2,
    # the function could hang depending on the sampling order

    #sample pairs one by one until we have key_size of them
    key = set()
    incidencies = dict()
    while len(key) < key_size:
        ind1 = random.randint(0, num_high_and_med-1)
        ind2 = random.randint(0, num_high_and_med-1)

        #fix index order to avoid duplicates
        if ind2 < ind1:
            ind1, ind2 = ind2, ind1

        valid_pair = True
        if ind1 == ind2:
            valid_pair = False
        if (ind1, ind2) in key:
            valid_pair = False
        if ind1 in incidencies and incidencies[ind1] == max_flips_per_node:
            valid_pair = False
        if ind2 in incidencies and incidencies[ind2] == max_flips_per_node:
            valid_pair = False

        if valid_pair:
            key.add((ind1, ind2))
            for ind in ind1, ind2:
                if ind in incidencies:
                    incidencies[ind] += 1
                else:
                    incidencies[ind] = 1

    res = list(key)
    res.sort()
    return res

