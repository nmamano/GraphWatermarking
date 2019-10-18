"""
adversary
"""
import random
from utils import printts, list_head_to_string

def random_edge_flip_adver(graph, prob):
    """
    flips each edge with probability prob
    the original graph is not modified
    """
    mod_graph = graph.copy()
    for i in range(graph.num_nodes()):
        for j in range(i+1, graph.num_nodes()):
            if random.random() < prob:
                mod_graph.flip_edge(i, j)
    return mod_graph

def approx_random_edge_flip_adver(graph, prob, key_edges=None, dbg=False):
    """
    approximately flips each edge with probability prob
    instead of considering each potential edge
    independently, it chooses "prob" edges
    and flips them
    instead of considering each potential edge

    if key_edges is set, then it is printed how many of
    those edges were flipped
    """
    mod_graph = graph.copy()
    num_nodes = graph.num_nodes()
    num_potential_edges = (num_nodes*(num_nodes-1))//2
    total_flips = prob*num_potential_edges
    already_flipped = set()
    count_additions = 0
    while len(already_flipped) < total_flips:
        node1 = random.randint(0, num_nodes-1)
        node2 = random.randint(0, num_nodes-1)
        if node2 < node1:
            node1, node2 = node2, node1
        if node1 == node2:
            continue
        if (node1, node2) in already_flipped:
            continue
        if not mod_graph.has_edge(node1, node2):
            count_additions += 1
        mod_graph.flip_edge(node1, node2)
        already_flipped.add((node1, node2))

    if dbg:
        if key_edges is not None:
            count = 0
            for edge in key_edges:
                if edge in already_flipped:
                    count += 1
            printts('Number of key edges flipped: '+str(count))
        total_flipped = len(already_flipped)
        flipped_percent = total_flipped*100/graph.num_edges()
        printts("Total number of edges flipped: "+str(total_flipped)+\
                ' ('+str(round(flipped_percent, 2))+'%)')
        printts(str(count_additions)+" additions and "+\
                str(total_flipped - count_additions)+" removals")
        print()
    return mod_graph

