"""
approximate isomorphism function from algorithm 2
"""
from label import label

def ham_dist(bv1, bv2):
    """
    returns the hamming distance between two bit vectors
    represented as lists
    """
    if len(bv1) != len(bv2):
        raise Exception("fail: bitvectors of different length "+\
                        str(len(bv1))+", "+str(len(bv2)))
    total = 0
    for i, bit in enumerate(bv1):
        if bit != bv2[i]:
            total += 1
    return total

def approx_isomorphism(graph1, graph2, hi_thres, med_thres, graph1_labels,
                       allow_repeated_matches=True):
    """
    returns a matching of the nodes in graph1 to nodes in graph2
    high degree nodes are matched to the high degree nodes in graph2
    (there must be the same number in graph1 and graph2)
    medium degree nodes are matched to medium degree nodes in graph2
    (there must be at least as many medium degree nodes in graph2 as in graph1)
    low degree nodes are matched to None
    """
    assert graph1.num_nodes() == graph2.num_nodes(), "both graphs must have the same size"

    hi_pairs1, med_pairs1 = graph1_labels
    hi_pairs2, med_pairs2 = label(graph2, hi_thres, med_thres)

    #matching stores in matching[i] a tuple with the node in graph2
    #matched to the node i in graph1 and the hamming distance between
    #their bitvectors in the case of medium degree nodes, or None
    #otherwise
    #for low-degree nodes, the node in graph2 matched to them is None
    matching = [(None, None) for i in range(graph1.num_nodes())]

    for i, (node, _) in enumerate(hi_pairs1):
        matching[node] = (hi_pairs2[i][0], None)

    for node1, bv1 in med_pairs1:
        min_dist = 9999999999
        for node2, bv2 in med_pairs2:
            dist = ham_dist(bv1, bv2)
            if dist < min_dist:
                min_dist = dist
                matching[node1] = (node2, dist)

    error_msg = "Approximate isomorphism error:\n"
    same_match_count = 0
    max_error_msg_lines = 20
    for i, (match1, dist1) in enumerate(matching):
        if match1 is not None:
            for j in range(i+1, len(matching)):
                match2, dist2 = matching[j]
                if match1 == match2:
                    same_match_count += 1
                    if same_match_count < max_error_msg_lines:
                        error_msg += "nodes "+str(i)+" and "+str(j)
                        error_msg += " both matched with "+str(match1)
                        error_msg += " (distances "+str(dist1)
                        error_msg += " and "+str(dist2)+")\n"
    if same_match_count > 0:
        if same_match_count >= max_error_msg_lines:
            error_msg += "... (total " + str(same_match_count) + ")\n"
        if allow_repeated_matches:
            print(error_msg)
        else:
            raise Exception(error_msg)

    matching_without_dists = [x[0] for x in matching]
    return matching_without_dists



