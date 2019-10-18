'''
mark function from algorithm 2
'''
import random

def rand_zero_or_one(one_prob):
    """ returns 1 with probability 'one_prob' and 0 otherwise """
    if random.random() < one_prob:
        return 1
    return 0

def edge_prob(graph, edge, print_prob=False):
    """ returns the probability of an edge in the graph """
    deg1 = graph.deg(edge[0])
    deg2 = graph.deg(edge[1])
    degsum = graph.deg_sum()
    prob = deg1*deg2/(graph.deg_sum()-deg1-deg2)
    if print_prob:
        print("Edge probability: "+str(deg1)+"*"+str(deg2)+"/("+
              str(degsum)+"-"+str(deg1)+"-"+str(deg2)+") = "+str(prob))
    return prob

def rand_flip_graph(graph, edge):
    """ returns whether an edge should be there
    according to the graph topology
    """
    return rand_zero_or_one(0.5)
    # return rand_zero_or_one(edge_prob(graph, edge))

def label_index2node(label_index, labels):
    """
    returns the high or medium degree node with a given label index
    labels contains the output of the label function:
    the sorted list of high degree nodes with their labels, and
    the sorted list of medium degree nodes with their labels
    note that label indices are 0-indexed too
    """
    hi_pairs, med_pairs = labels
    if label_index < len(hi_pairs):
        return hi_pairs[label_index][0]
    else:
        error_msg = "there is no node with label "+str(label_index)
        assert label_index-len(hi_pairs) < len(med_pairs), error_msg
        return med_pairs[label_index-len(hi_pairs)][0]

def prob_sum(graph, key):
    """ returns the sum of the probabilities of all the edges in the key """
    return sum(edge_prob(graph, edge, True) for edge in key)

def mark(key, graph, labels):
    """
    returns a 2-tuple with first the bit string containing the resamplings
    applied to 'graph' at the positions determined by 'key',
    and second the corresponding modified graph.
    the original graph is not modified
    Note: the indices in the key are not regular indices, but
    indices when the nodes are sorted by label
    """
    resample_id = [rand_flip_graph(graph, edge) for edge in key]
    mod_graph = graph.copy()
    for i, (label_index1, label_index2) in enumerate(key):
        index1 = label_index2node(label_index1, labels)
        index2 = label_index2node(label_index2, labels)
        if resample_id[i]:
            mod_graph.add_edge(index1, index2)
        else:
            mod_graph.remove_edge(index1, index2)
    return (resample_id, mod_graph)

