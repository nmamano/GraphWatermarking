"""Security experiment from Algorithm 1"""

import random
import sys
from math import sqrt
from subprocess import call
from utils import list_head_to_string, printts
from mark import mark
from label import label, degree_cutoffs, max_med_deg_node
from keygen import key_gen
from adversary import approx_random_edge_flip_adver
from identify import identify, get_ori_graph_key_edges, get_id
from graph import Graph
from approximate_isomorphism import ham_dist

def print_experiment_parameters(flip_prob_adversary, num_copies,
                                key_size, max_flips_per_node, hi_thres,
                                med_thres):
    """ printtss the details of the experiment """
    printts("Experiment parameters")

    printts("Adversary type: random flip edge")
    printts("Adversary flip probability: "+str(flip_prob_adversary))
    print()

    printts("key size: "+str(key_size))
    printts("max flips per node: "+str(max_flips_per_node))
    print()

    printts("number of graph copies: "+str(num_copies))
    print()

    printts("high degree threshold: "+str(hi_thres))
    printts("medium degree threshold: "+str(med_thres))
    print()

def section_header(header):
    """ prints the header in a fancy way """
    print()
    padding = (16 - len(header))//2
    print("="*16, " "*padding, header, " "*padding, "="*16)
    print()

def experiment(ori_graph, flip_prob_adversary, num_copies,
               key_size, max_flips_per_node, hi_thres,
               med_thres, dbg=True):
    """ Security experiment from Algorithm 1
    returns 1 if the modified graph is identified correctly,
           -1 if the modified graph is identified incorrectly,
            0 if more than one graph tied
    returns the modified graph too"""

    if dbg:
        print_experiment_parameters(flip_prob_adversary, num_copies,
                                    key_size, max_flips_per_node, hi_thres,
                                    med_thres)

    total_hi_and_med = med_thres
    key = key_gen(key_size, max_flips_per_node, total_hi_and_med)

    if dbg:
        section_header("KEY GENERATION")
        printts('total high and medium degree nodes: '+str(total_hi_and_med))
        printts("key: "+list_head_to_string(key))
        print()
        printts('Original graph:')
        ori_graph.print_statistics()

        section_header("LABELING")
        hi_cutoff, med_cutoff = degree_cutoffs(ori_graph, med_thres, hi_thres)
        printts('High-degree cutoff: '+str(hi_cutoff))
        printts('Medium-degree cutoff: '+str(med_cutoff))
        print()

    labels = label(ori_graph, hi_thres, med_thres)

    if dbg:
        ori_hi_labels, ori_med_labels = labels
        printts('high degree nodes with labels (node_id, label):\n'+
                list_head_to_string(ori_hi_labels))
        printts('medium degree nodes:\n'+
                list_head_to_string(list(zip(*ori_med_labels))[0]))

        section_header("MARKING")

    marked_graphs = [mark(key, ori_graph, labels)
                     for i in range(num_copies)]
    chosen_ind = random.randint(0, num_copies-1)
    chosen_id, chosen_graph = marked_graphs[chosen_ind]

    if dbg:
        ori_edges = get_ori_graph_key_edges(key, ori_graph, hi_thres, med_thres, labels)
        ori_id = get_id(ori_graph, ori_edges)
        printts('Original graph id: '+list_head_to_string(ori_id))
        print('0s/1s in the original graph id: ',
              str(len(ori_id)-sum(ori_id)), '/', str(sum(ori_id)), sep='')
        print('1s in the marked graphs ids:',
              [sum(_id) for _id, _ in marked_graphs])
        print('differences between the original graph id and the marked graphs ids:')
        print([ham_dist(ori_id, _id) for _id, _ in marked_graphs])
        print()

        printts('Chosen graph (index '+str(chosen_ind)+'):')
        chosen_graph.print_statistics()
        printts('Chosen graph id: '+list_head_to_string(chosen_id))
        print()

        other_ind = (chosen_ind+1)%len(marked_graphs)
        other_id, other_graph = marked_graphs[other_ind]
        printts('Other marked graph (index '+str(other_ind)+'):')
        other_graph.print_statistics()
        printts('Other graph id: '+list_head_to_string(other_id))

        section_header("ADVERSARY")

    mod_graph = approx_random_edge_flip_adver(chosen_graph, flip_prob_adversary,
                                              key_edges=key, dbg=dbg)

    if dbg:
        printts('Modified graph:')
        mod_graph.print_statistics()
        mod_edges = get_ori_graph_key_edges(key, mod_graph, hi_thres, med_thres, labels)
        mod_id = get_id(mod_graph, mod_edges)
        printts('Modified graph id: '+list_head_to_string(mod_id))

        print('0s/1s in the chosen graph id: ',
              str(len(chosen_id)-sum(chosen_id)), '/', str(sum(chosen_id)), sep='')
        print('0s/1s in the modified graph id: ',
              str(len(mod_id)-sum(mod_id)), '/', str(sum(mod_id)), sep='')
        print('distance between the chosen graph id and the modified graphs id:',\
              ham_dist(chosen_id, mod_id))

        section_header("IDENTIFY")

    ids = [id_graph_pair[0] for id_graph_pair in marked_graphs]
    identified_inds = identify(key, ori_graph, mod_graph, ids, hi_thres, med_thres, labels, dbg)

    if len(identified_inds) == 1:
        identified_ind = identified_inds[0]
        if identified_ind == chosen_ind:
            printts('Experiment success: the graph '+str(chosen_ind)+\
                ' was identified correctly')
            return 1, mod_graph
        else:
            printts("Experiment fail: graph "+str(identified_ind)+\
                " identified instead of "+str(chosen_ind))
            return -1, mod_graph
    elif chosen_ind in identified_inds:
        printts('Experiment fail: the id was identified correctly, but not uniquely')
        return 0, mod_graph
    else:
        printts('Experiment fail: multiple graphs were identified'+\
            ', and none of them were the chosen one')
        return 0, mod_graph

def experiment_wrapper():
    """wrapper to initialize the parameters of the experiment"""
    dbg = True
    network_name = "youtube"
    # network_name = "random_power_law"
    # network_name = "facebook"
    graph_file = "../networks/"+network_name+"/"+network_name

    printts('loading graph '+network_name+'...')
    ori_graph = Graph.load_edge_list_format(graph_file)
    printts('done')

    #to emulate the ordering of the nodes generated by the model:
    ori_graph.sort_nodes_by_degree()

    flip_prob_adversary = 0.00001
    num_copies = 10

    #the node with degree equal to the threshold
    #is included in the class
    if network_name == "youtube":
        hi_thres = 3*ori_graph.num_consecutive_unique_deg_nodes()
        hi_thres = 128
        num_copies = 5
    elif network_name == "facebook":
        hi_thres = 2*ori_graph.num_consecutive_unique_deg_nodes()
        hi_thres = 64
    elif network_name == "random_power_law":
        hi_thres = 2*ori_graph.num_consecutive_unique_deg_nodes()
        hi_thres = 51
    else:
        assert False, "set the high and medium thresholds for this network"

    valid_hi_thres = ori_graph.prev_valid_threshold(hi_thres)
    if valid_hi_thres != hi_thres:
        print("Warning: the high-degree node threshold has been adjusted from",
              hi_thres, "to", valid_hi_thres)
    hi_thres = valid_hi_thres

    med_thres = max_med_deg_node(ori_graph, hi_thres)
    med_thres = ori_graph.prev_valid_threshold(med_thres)

    max_flips_per_node = 1
    key_size = (med_thres*max_flips_per_node-1)//2

    experiment(ori_graph, flip_prob_adversary, num_copies,
               key_size, max_flips_per_node, hi_thres,
               med_thres, dbg=dbg)

def dk2_deviation(graph1, graph2):
    """ computes normalized dk2 deviation """
    map1 = graph1.dk2_map()
    map2 = graph2.dk2_map()
    total = 0

    for deg_pair in map1:
        count1 = map1[deg_pair]
        if deg_pair in map2:
            count2 = map2[deg_pair]
        else:
            count2 = 0
        total += (count1-count2)**2

    new_pair_count = 0
    for deg_pair in map2:
        if deg_pair in map1:
            continue #already treated
        else:
            total += map2[deg_pair]**2
            new_pair_count += 1

    return sqrt(total)/(len(map1)+new_pair_count)

def main(argv):
    """ saves in the output file:
    - number of high degree nodes
    - number of medium degre nodes
    - key size
    - success (1) or not (0)
    - normalized dk2 deviation
    """

    network_name = argv[1]
    hi_thres = int(argv[2])
    flip_prob_adversary = float(argv[3])
    res_file = argv[4]

    num_copies = 10
    max_flips_per_node = 1

    graph_file = "../networks/"+network_name+"/"+network_name
    printts('loading graph '+network_name+'...')
    ori_graph = Graph.load_edge_list_format(graph_file)
    printts('done')
    ori_graph.sort_nodes_by_degree()
    printts('sorting done')

    hi_thres = ori_graph.prev_valid_threshold(hi_thres)
    med_thres = max_med_deg_node(ori_graph, hi_thres)
    med_thres = ori_graph.prev_valid_threshold(med_thres)

    key_size = (med_thres*max_flips_per_node)//2

    res, mod_graph = experiment(ori_graph, flip_prob_adversary, num_copies,
                                key_size, max_flips_per_node, hi_thres,
                                med_thres, dbg=True)

    if res == -1:
        res = 0

    dk2_dev = dk2_deviation(ori_graph, mod_graph)

    output = str(hi_thres) + " " + str(med_thres-hi_thres) + " "
    output += str(key_size) + " " + str(res) + " " + str(dk2_dev) + "\n"
    with open(res_file, 'w') as fout:
        fout.write(output)


def submit_to_cluster(argv):
    """ executes the experiment in the cluster """
    res_file = argv[4]
    script_file = res_file + ".sh"
    project_folder = "***modify this: path to src folder" #change this string
    out_file = project_folder + res_file + ".out"
    err_file = project_folder + res_file + ".err"
    with open(script_file, 'w') as fout:
        fout.write("#!/bin/bash\n")
        fout.write("cd "+project_folder+"\n")
        fout.write("python3.3 "+argv[0]+" "+argv[1]+" "+argv[2]+" "+argv[3]+" "+argv[4]+"\n")

    call(["chmod", "+x", script_file])
    call(["qsub", "-o", out_file, "-e", err_file, script_file])


if __name__ == "__main__":
    if len(sys.argv) == 6 and sys.argv[5] == "sub":
        submit_to_cluster(sys.argv)
    else:
        main(sys.argv)
