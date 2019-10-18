""" experiment to test the number of medium-degree nodes as a function
of the numbero of high-degree nodes """

from utils import printts
from label import max_med_deg_node
from graph import Graph

def high_vs_med_threshold():
    """ prints for each hi_thres, the maximum med_thres """
    network_name = "youtube"
    # network_name = "random_power_law"
    # network_name = "facebook"
    graph_file = "../networks/"+network_name+"/"+network_name

    printts('loading graph '+network_name+'...')
    ori_graph = Graph.load_edge_list_format(graph_file)
    printts('done')

    #to emulate the ordering of the nodes generated by the model:
    ori_graph.sort_nodes_by_degree()

    for hi_thres in range(1, 1000):
        printts(str(hi_thres)+": "+str(max_med_deg_node(ori_graph, hi_thres)))

high_vs_med_threshold()
