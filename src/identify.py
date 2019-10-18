"""
function identify from algorithm 2
"""
from utils import printts
from approximate_isomorphism import approx_isomorphism, ham_dist
from mark import label_index2node

def get_ori_graph_key_edges(key, graph, hi_thres, med_thres, labels):
    """
    returns the potential edges of the original graph which are part of
    the key
    """
    edges = [None for _ in key]
    for i, (label_index1, label_index2) in enumerate(key):
        #indices used in the mark function:
        index1 = label_index2node(label_index1, labels)
        index2 = label_index2node(label_index2, labels)
        edges[i] = (index1, index2)
    return edges

def get_mod_graph_key_edges(key, ori_graph, mod_graph, hi_thres, med_thres, ori_labels):
    """
    returns the poteintial edges of the modified graph which are part of the key

    """
    edges = [None for _ in key]
    ori_edges = get_ori_graph_key_edges(key, ori_graph, hi_thres, med_thres, ori_labels)
    matching = approx_isomorphism(ori_graph, mod_graph, hi_thres, med_thres, ori_labels)
    for i, (ori_index1, ori_index2) in enumerate(ori_edges):
        #corresponding indices in the modified graph:
        mod_index1 = matching[ori_index1]
        mod_index2 = matching[ori_index2]
        edges[i] = (mod_index1, mod_index2)
    return edges

def get_id(graph, edges):
    """
    returns the id of a graph according to whether
    it contains an edge in certain places specified by 'edges'
    """
    res = [0 for _ in edges]
    for i, (node1, node2) in enumerate(edges):
        if graph.has_edge(node1, node2):
            res[i] = 1
    return res

def min_indices(elems):
    """
    returns the indices of the smallest element in elems
    """
    indices = []
    smallest_value = elems[0]
    for i, elem in enumerate(elems):
        if elem < smallest_value:
            smallest_value = elem
            indices = [i]
        elif elem == smallest_value:
            indices += [i]

    return indices

def identify(key, ori_graph, mod_graph, ids, hi_thres, med_thres, labels, dbg=False):
    """
    returns the indices of the id in ids closest to mod_graph's id
    (as opposed to the id itself, as in the paper)
    """
    edges = get_mod_graph_key_edges(key, ori_graph, mod_graph, hi_thres, med_thres, labels)
    mod_id = get_id(mod_graph, edges)
    dists = [ham_dist(mod_id, bv) for bv in ids]
    inds = min_indices(dists)

    if dbg:
        printts('hamming distances between the ids of the modified graph '+\
                'and marked graphs:\n'+str(dists))
        printts('closest indices: '+str(inds))

    if len(inds) > 1:
        printts("identify error: there are "+str(len(inds))+" closest bitvectors: "+str(inds))
        printts("at hamming distance "+str(ham_dist(mod_id, ids[inds[0]])))
    return inds

