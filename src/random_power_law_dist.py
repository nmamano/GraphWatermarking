"""
Functions for the generation of graphs following
the random power law graph model
"""
import random
from graph import Graph

def start_ind(model, dbg=False):
    """
    equation 1 in the paper (called i_0): returns the first index
    of the w vector used in the random power law graph model
    """
    assert model.gamma > 2 #if gamma=2, this returns 0

    num_nodes = model.num_nodes
    max_deg = model.max_deg
    avg_deg = model.avg_deg
    gamma = model.gamma

    numerator = avg_deg*(gamma-2)
    denominator = max_deg*(gamma-1)
    base = numerator/denominator
    res = num_nodes * base**(gamma-1)
    if dbg:
        print(num_nodes, max_deg, avg_deg, gamma, numerator, denominator, base, res)
    return res

def param_k0(model):
    """
    equation 2 in the paper (called K_0):
    Parameter needed to compute the probability of an edge
    between a given pair of nodes according to this model
    """
    avg_deg = model.avg_deg
    gamma = model.gamma
    base = (gamma-2)/(gamma-1)
    return (base**2)*avg_deg

def edge_prob(model, i, j, dbg=False):
    """
    probability of edge between nodes i and j in random power
    law graph model with the parameters specified in model
    note that in the paper i and j are i0-indexed and here
    they are 0-indexed
    """
    #hence:
    if dbg:
        print(i, j)
        print(start_ind(model))

    i = i+start_ind(model)
    j = j+start_ind(model)

    num_nodes = model.num_nodes
    gamma = model.gamma
    first_part = param_k0(model)
    second_part_base = num_nodes**(gamma-3)*i*j
    second_part_exp = -1/(gamma-1)
    res = first_part*second_part_base**second_part_exp
    if dbg:
        print('edge_prob:', res)
    return res

def random_power_law_graph(model):
    """
    returns a graph from the random power law graph model
    with the parameters specified in model
    """
    num_nodes = model.num_nodes
    adj_lists = [[] for i in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(i+1, num_nodes):
            prob_ij = edge_prob(model, i, j) #i,j are converted to i0-indexed inside edge_prob
            is_actual_edge = random.random() < prob_ij
            if is_actual_edge:
                adj_lists[i].append(j)
                adj_lists[j].append(i)
    return Graph(adj_lists)
