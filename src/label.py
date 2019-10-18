"""
Function label from algorithm 2 in the paper
"""
from utils import printts, list_head_to_string

def highest_deg_nodes(graph, count, extended_deg_size):
    """
    returns a list with the nodes with highest degree
    in no particular order
    in case of tie return arbitrary node
    (ties should be avoided by setting appropriate thresholds
    when labeling the original graph, but they can't be avoided
    when labeling the modified graph)
    """
    num_nodes = graph.num_nodes()
    extended_degs = [graph.extended_deg(i, extended_deg_size) for i in range(num_nodes)]
    sorted_extended_degs = sorted(extended_degs, reverse=True)
    cutoff_extended_degs = sorted_extended_degs[count-1]
    res = []
    for i in range(num_nodes):
        if extended_degs[i] >= cutoff_extended_degs:
            res.append(i)
    return res

def sort_hi_pairs(hi_pairs):
    """
    given the list of 2-tuples containing the indices of the
    high-degree nodes and their degrees
    returns the list in decreasing order of degree
    """
    hi_pairs.sort(key=lambda x: x[1], reverse=True)

def degree_cutoffs(graph, med_thres, hi_thres):
    """
    returns the degrees that separate high and
    medium and medium and low degree vertices
    """
    degs = [graph.deg(i) for i in range(graph.num_nodes())]
    sorted_degs = sorted(degs, reverse=True)
    hi_cutoff = sorted_degs[hi_thres]
    med_cutoff = sorted_degs[med_thres-1]
    return hi_cutoff, med_cutoff

def med_deg_nodes(graph, med_thres, hi_thres, dbg=False):
    """
    returns the list of medium degree nodes,
    according to the thresholds,
    in no particular order
    in case of tie, return arbitrary node
    (ties should be avoided by setting appropriate thresholds
    when labeling the original graph, but they can't be avoided
    when labeling the modified graph)
    """
    cutoff_above, cutoff_below = degree_cutoffs(graph, med_thres, hi_thres)
    res = []
    for i in range(graph.num_nodes()):
        if graph.deg(i) <= cutoff_above and graph.deg(i) >= cutoff_below:
            res.append(i)

    if dbg:
        printts('High-degree cutoff:'+str(cutoff_above))
        printts('Medium-degree cutoff:'+str(cutoff_below))
        printts('Num medium-degree nodes:'+str(len(res)))

    return res

def med_node_bitvector(graph, node, sorted_hi_nodes):
    """
    returns the bitvector with the adjacencies of a
    medium-degree node to all the high-degree nodes,
    in order of labeling (i.e. in decreasing order of degree)
    """
    are_adj = lambda u, v: 1 if graph.has_edge(u, v) else 0
    return [are_adj(node, hi_node) for hi_node in sorted_hi_nodes]

def sort_med_pairs(pairs):
    """
    given the list of 2-tuples containing the indices of the
    medium-degree nodes and their labels (i.e., their bitvectors)
    returns the list in lexicographical order of the bitvectors
    """
    pairs.sort(key=lambda x: x[1])

def get_hi_pairs(graph, hi_thres, extended_deg_size, allow_repeated_degs=True, dbg=True):
    """
    returns the list of 2-tuples containing the indices of the
    high-degree nodes and their labels, sorted in decreasing
    order of degree
    """
    nodes = highest_deg_nodes(graph, hi_thres, extended_deg_size)
    extended_degs = [graph.extended_deg(node, extended_deg_size) for node in nodes]
    node_deg_pairs = list(zip(nodes, extended_degs))
    sort_hi_pairs(node_deg_pairs)
    found_warning = False
    for i in range(len(nodes)-1):
        extended_deg_i = node_deg_pairs[i][1]
        next_extended_deg = node_deg_pairs[i+1][1]
        if extended_deg_i == next_extended_deg:
            found_warning = True
            node1 = node_deg_pairs[i][0]
            node2 = node_deg_pairs[i+1][0]
            msg = "the " + str(i+1) + "-th and " + str(i+2) + "-th"
            msg += " high-degree nodes " + str(node1) + ", " + str(node2)
            msg += " have extended degree " + str(extended_deg_i)
            if allow_repeated_degs:
                if dbg:
                    print('labeling warning:', msg)
            else:
                raise Exception(msg)
    if dbg and found_warning:
        print()

    #the label is the index in the sequence, not the degree
    hi_pairs = []
    for i, (node, _) in enumerate(node_deg_pairs):
        hi_pairs.append((node, i))

    return hi_pairs

def get_med_pairs(graph, med_thres, hi_thres, sorted_hi_nodes, dbg=False):
    """
    returns the list of 2-tuples containing the indices of the
    medium-degree nodes and their labels, sorted lexicographically
    """
    if dbg:
        print('med_thres: '+str(med_thres))
        print('hi_thres: '+str(hi_thres))
        print('sorted_hi_nodes:')
        print(sorted_hi_nodes)

    nodes = med_deg_nodes(graph, med_thres, hi_thres)

    if dbg:
        print('med nodes:')
        print(nodes)

    med_node_label = lambda node: med_node_bitvector(graph, node, sorted_hi_nodes)
    labels = [med_node_label(node) for node in nodes]

    if dbg:
        print('labels:')
        print(labels)

    pairs = list(zip(nodes, labels))

    if dbg:
        print('pairs:')
        print(pairs)

    sort_med_pairs(pairs)

    if dbg:
        print('sorted pairs:')
        print(pairs)

    error_msg = "labeling error: medium-degree node pairs with same bitvector:\n"
    repeated_bv_count = 0
    max_count = 5
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            if pairs[i][1] == pairs[j][1]:
                repeated_bv_count += 1
                if repeated_bv_count < max_count:
                    error_msg += str(pairs[i][0]) + ", " + str(pairs[j][0])
                    error_msg += ": " + list_head_to_string(pairs[i][1], max_items=10) + "\n"
    if repeated_bv_count > 0:
        if repeated_bv_count >= max_count:
            error_msg += "... (total " + str(repeated_bv_count) + ")\n"
        print(error_msg)
        # raise Exception(error_msg)

    return pairs

def label(graph, hi_thres, med_thres):
    """
    returns two lists with pairs (index,label),
    one for high deg and one for med deg
    lists are sorted by labels:
    for high degree vectors, decreasing by degree
    for medium degree vectors, lexicographically
    """

    extended_deg_size = hi_thres
    hi_pairs = get_hi_pairs(graph, hi_thres, extended_deg_size)
    sorted_hi_nodes = [x[0] for x in hi_pairs]
    med_pairs = get_med_pairs(graph, med_thres, hi_thres, sorted_hi_nodes)
    return (hi_pairs, med_pairs)

def max_med_deg_node(graph, hi_thres):
    hi_pairs = get_hi_pairs(graph, hi_thres, 40, dbg=False)
    sorted_hi_nodes = [x[0] for x in hi_pairs]

    bitvectors = []
    node = hi_thres+1
    bitvector = med_node_bitvector(graph, node, sorted_hi_nodes)
    bitvectors.append(bitvector)
    while node < graph.num_nodes():
        node += 1
        bitvector = med_node_bitvector(graph, node, sorted_hi_nodes)
        if bitvector in bitvectors:
            return node-1
        bitvectors.append(bitvector)

