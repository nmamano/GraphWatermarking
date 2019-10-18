from plfit import *
from plpva import *
from math import log, floor, ceil
from random import random
import math


class Graph:
    """
    represented using unordered adjacency lists
    """

    def __init__(self, adj_lists):
        """
        the original adj lists are not modified
        """
        self.adj_lists = [adj_lists[i][:] for i in range(len(adj_lists))]
        self.deg_dist = None #initialized only when necessary

    def copy(self):
        """ returns a copy of itself """
        return Graph(self.adj_lists)

    def num_nodes(self):
        """ number of nodes """
        return len(self.adj_lists)

    def num_edges(self):
        """ number of edges """
        return sum(len(adj_list) for adj_list in self.adj_lists)//2

    def get_adj_matrix(self):
        """ adjacency matrix """
        adj_matrix = [[0 for column in range(self.num_nodes())] for row in range(self.num_nodes())]
        for node in self.adj_lists:
            for neighbor in node:
                adj_matrix[node][neighbor] = 1
                adj_matrix[neighbor][node] = 1
        return adj_matrix

    def print_adj_matrix(self):
        """ prints the adjacency matrix """
        matrix = self.get_adj_matrix()
        for i in range(self.num_nodes()):
            print(matrix[i])

    def get_edge_list(self):
        """
        returns the list of edges
        in no particular order
        """
        res = []
        for node1, adj_list in enumerate(self.adj_lists):
            for node2 in adj_list:
                if node1 < node2: #to avoid repeated entries
                    res.append((node1, node2))
        return res

    def has_edge(self, i, j, dbg=False):
        """ returns whether two nodes are connected """
        if dbg:
            print('has_edge('+str(i)+', '+str(j)+'):')
            print('adj_lists['+str(i)+'] = ')
            print(self.adj_lists[i])
            print('adj_lists['+str(j)+'] = ')
            print(self.adj_lists[j])

        return j in self.adj_lists[i]

    def add_edge(self, i, j):
        """
        adds edge if not already there
        note that this might invalidate the degree dist
        """
        if not j in self.adj_lists[i]:
            self.adj_lists[i].append(j)
            self.adj_lists[j].append(i)
            self.deg_dist = None

    def remove_edge(self, i, j):
        """
        removes edge if present
        note that this might invalidate the degree dist
        """
        if j in self.adj_lists[i]:
            self.adj_lists[i].remove(j)
            self.adj_lists[j].remove(i)
            self.deg_dist = None

    def flip_edge(self, i, j):
        """
        if two nodes are connected disconnects them
        and the other way around
        note that this might invalidate the degree dist
        """
        if self.has_edge(i, j):
            self.remove_edge(i, j)
        else:
            self.add_edge(i, j)

    def get_deg_dist(self):
        """
        returns a list with the number of nodes with
        degree 0,1,2,...,max_deg
        the field deg_dist should ONLY be accessed
        through this getter, even within the class,
        as otherwise it might not be initialized
        """
        if self.deg_dist is None:
            self.__init_deg_dist()
        return self.deg_dist


    def __init_deg_dist(self):
        """
        initializes the field self.deg_dist
        since this is an expensive operation, it is only
        performed under request (somewhere get_deg_dist is used)
        """
        degrees = [self.deg(node) for node in range(self.num_nodes())]
        degree2count = dict()
        for degree in degrees:
            if degree not in degree2count:
                degree2count[degree] = 1
            else:
                degree2count[degree] += 1

        count = lambda degree: degree2count[degree] if degree in degree2count else 0
        self.deg_dist = [count(degree) for degree in range(self.max_deg()+1)]

        #equivalent, naive, inefficient implementation:
        #deg_dist = [self.num_nodes_with_deg(d) for d in range(self.max_deg()+1)]

    def deg(self, node):
        """ degree of a node """
        return len(self.adj_lists[node])

    def extended_deg(self, node, k):
        """ returns the list with the degree of the node and the highest
        k degrees of its neighbors, in decreasing order (or all if k is None)
        if there are not k neighbors, fills the vector with 0 """
        neighbor_degs = [self.deg(neighbor) for neighbor in self.adj_lists[node]]
        neighbor_degs.sort(reverse=True)
        if k is None:
            return [self.deg(node)] + neighbor_degs
        elif k <= len(neighbor_degs):
            return [self.deg(node)] + neighbor_degs[:k]
        else: #K > len(neighbor_degs)
            return [self.deg(node)] + neighbor_degs + [0]*(k - len(neighbor_degs))

    def deg_sum(self):
        """ returns the sum of all degrees """
        return self.num_edges()*2

    def max_deg(self):
        """ maximum degree among all nodes """
        return max(self.deg(i) for i in range(self.num_nodes()))

    def avg_deg(self):
        """ average degree """
        return sum(self.deg(i) for i in range(self.num_nodes()))/self.num_nodes()

    def num_nodes_with_deg(self, deg):
        """ number of nodes with a given degree """
        count = 0
        for i in range(self.num_nodes()):
            if self.deg(i) == deg:
                count += 1
        return count

    def get_degs(self):
        """
        returns the list of degrees in decreasing order
        it may contain repeated entries
        """
        res = [self.deg(i) for i in range(0, self.num_nodes())]
        return sorted(res, reverse=True)

    def nodes_sorted_by_degree(self):
        """ returns the nodes sorted by degree, in decreasing order """
        num_nodes = self.num_nodes()
        nodes = list(range(num_nodes))
        nodes.sort(key=self.deg, reverse=True)
        return nodes

    def sort_nodes_by_degree(self):
        """ reorders nodes by degree in decreasing order
        to save space, the reordering is done in-place, in two stages:
        first the contents of the adjacency lists are updated with the
        new indices. second, the adj lists themselves are sorted according
        to the new indices """
        num_nodes = self.num_nodes()
        sorted_nodes = self.nodes_sorted_by_degree()
        old2new = {node:i for i, node in enumerate(sorted_nodes)}
        #replace the elements in place to save space
        for old_i in range(num_nodes):
            old_adj_list = self.adj_lists[old_i]
            for j in range(len(old_adj_list)):
                old_adj_list[j] = old2new[old_adj_list[j]]

        #put adj lists together with their old indices in order
        #to sort them according to their indices
        index_adj_list_tuples = [(i, adj_list) for i, adj_list in enumerate(self.adj_lists)]
        #sort adjacency lists according to their new index
        index_adj_list_tuples.sort(key=lambda tuple: old2new[tuple[0]])
        #use the new ordering
        for i in range(len(self.adj_lists)):
            self.adj_lists[i] = index_adj_list_tuples[i][1]

    def store_edge_list_format(self, file):
        """
        stores the graph in a file using edge list format
        """
        with open(file, 'w') as fout:
            for edge in self.get_edge_list():
                fout.write(str(edge[0])+" "+str(edge[1])+"\n")

    @staticmethod
    def load_edge_list_format(file):
        """
        returns a graph based on the description in a file
        the file is expected to contain one edge per line,
        consisting of two indices (ints)
        duplicated edges are accepted
        possibly with header comment lines starting with '#'
        the file might be 0-indexed or 1-indexed,
        they are converted to 0-indexed
        the file is expected to have continuous indices, if it
        has gaps (e.g. index "3" does not appear anywhere in the file)
        it is assumed that node "3" exists but does not have any neighbor
        """
        min_index = 100000000 #upper bound for ANY index
        max_index = -1
        edges = []
        # print('Loading',file)
        # printts('    parsing file')
        with open(file, 'r') as fin:
            for line in fin:
                if line[0] == '#':
                    continue

                node_ids = line.split()
                id1, id2 = int(node_ids[0]), int(node_ids[1])
                edges.append([id1, id2])
                min_index = min(min_index, id1, id2)
                max_index = max(max_index, id1, id2)

        assert min_index == 0 or min_index == 1
        num_nodes = max_index+1-min_index

        # printts('    building adj lists')
        adj_lists = [[] for node in range(num_nodes)]
        for node1, node2 in edges:
            adj_lists[node1-min_index].append(node2-min_index)
            adj_lists[node2-min_index].append(node1-min_index)

        # printts('    sorting adj lists and removing duplicates')
        for adj_list in adj_lists:
            adj_list = sorted(list(set(adj_list)))

        # printts('    initializing graph')
        return Graph(adj_lists)


# Note: the code that was used to find gamma and x-min was written in Python 2

# returns the scaling parameter, gamma, and the x-min value
#   requires snap module, which can be found at the Stanford Large Network Dataset Collection website
#   if test_fit is true, then a p-value is printed (this calculation takes a really long time)
#   if plot_data is true, a plot of the data is given to visually see if it follows a power-law distribution
def get_parameters_snap(txt_file, test_fit, plot_data):
    try:
        import snap
    except ImportError:
        print("Error importing snap (Stanford Large Network Dataset Collection)")
        return

    directed_graph = snap.LoadEdgeList(snap.PNGraph, txt_file, 0, 1)
    undirected_graph = snap.ConvertGraph(snap.PUNGraph, directed_graph)

    degree_dist = dict()
    for node in undirected_graph.Nodes():
        if node.GetOutDeg() not in degree_dist:
            degree_dist[node.GetOutDeg()] = 0
        degree_dist[node.GetOutDeg()] += 1

    data = [float(value)/undirected_graph.GetNodes() for value in degree_dist.values()]

    gamma_x_min = plfit(data)

    test_fit_and_plot(data, gamma_x_min, test_fit, plot_data)

    # gamma_x_min[0] is the scaling parameter, gamma, and gamma_x_min[1] is x-min
    return [gamma_x_min[0], gamma_x_min[1]]

# returns the scaling parameter, gamma, and the x-min value
#   uses Nil's graph class
#   if test_fit is true, then a p-value is printed (this calculation takes a really long time)
#   if plot_data is true, a plot of the data is given to visually see if it follows a power-law distribution
def get_parameters_graph(txt_file, test_fit, plot_data):
    undirected_graph = Graph.load_edge_list_format(txt_file)

    num_nodes = undirected_graph.num_nodes()

    data = [degree/float(num_nodes) for degree in undirected_graph.get_deg_dist() if degree != 0]

    gamma_x_min = plfit(data)
    print "This is the number of nodes: ", num_nodes
    print "This is the number of edges: ", undirected_graph.num_edges()
    print "This is the max degree: ", undirected_graph.max_deg()

    test_fit_and_plot(data, gamma_x_min, test_fit, plot_data)

    # gamma_x_min[0] is the scaling parameter, gamma, and gamma_x_min[1] is x-min
    return [gamma_x_min[0], gamma_x_min[1]]


def get_p_value(data, x_min):
    p_val = plpva(data, x_min, 'silent')
    if p_val[0] > 0.1:
        print("The p-value is ", p_val[0], " which implies that the power-law distribution is a good fit.")
    else:
        print("The p-value is ", p_val[0], " which implies that the power-law distribution is not a good fit.")


def test_fit_and_plot(data, gamma_x_min, test_fit, plot_data):
    if test_fit:
        get_p_value(data, gamma_x_min[1])

    if plot_data:
        data.sort(reverse=True)
        plot_data_and_line(data, gamma_x_min[0])
        plot_Clauset(data, gamma_x_min[1], gamma_x_min[0])


# Generates data to test the correctness of the function plfit
#   reasoning behind the generation of the numbers in this way given at http://mathworld.wolfram.com/RandomNumber.html
def random_power_law(num_data, x_min, gamma):
    return [x_min*pow((1.0 - random()), 1.0/(gamma + 1.0)) for i in range(0, num_data)]


# Tests the correctness of function plfit
#   gamma is the exponential parameter in the model
#   test_fit will generate p-value but takes a substantial amount of time, even if using pypy
#   plot_data plots the data in two different ways and requires matplotlib to work
def test_plfit(num_data, x_min, gamma, test_fit, plot_data):
    data = random_power_law(num_data, x_min, -gamma)
    gamma_x_min = plfit(data)

    test_fit_and_plot(data, gamma_x_min, test_fit, plot_data)

    # gamma_x_min[0] is the exponential parameter, gamma, and gamma_x_min[1] is x-min
    return [gamma_x_min[0], gamma_x_min[1]]


def plot_data_and_line(data, gamma):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Error importing matplotlib")
        return
    else:
        plt.plot([pow(.01*i, -gamma) for i in range(1, 10000)])
        plt.plot(data, 'ro')
        plt.axis([0, len(data), 0, max(data) + max(data)*0.1])
        plt.show()


# This code is taken from Joel Ornstein's implementation of Aaron Clauset's code, which is also where the files
#   plfit and plpva came from
def plot_Clauset(data, x_min, gamma):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Error importing matplotlib")
        return
    else:
        h = [[], []]
        n = len(data)
        c1 = sorted(data)
        c2 = map(lambda X: X/float(n), range(n, 0, -1))
        q = sorted(filter(lambda X: X >= x_min, data))
        cf = map(lambda X: pow(float(X)/x_min, 1.-gamma), q)
        cf = map(lambda X: X*float(c2[c1.index(q[0])]), cf)

        h[0] = plt.loglog(c1, c2, 'bo',markersize=8,markerfacecolor=[1,1,1],markeredgecolor=[0,0,1])
        h[1] = plt.loglog(q, cf, 'k--',linewidth=2)

        xr1 = pow(10, floor(log(min(data), 10)))
        xr2 = pow(10, ceil(log(min(data), 10)))
        yr1 = pow(10, floor(log(1./n, 10)))
        yr2 = 1

        plt.axhspan(ymin=yr1, ymax=yr2, xmin=xr1, xmax=xr2)
        plt.ylabel('Pr(X >= x)', fontsize=16)
        plt.xlabel('x', fontsize=16)
        plt.show()


if __name__ == "__main__":
    # In order to get the p-value, must set the first boolean parameter to True
    alpha, x_min = get_parameters_graph("name_of_file.txt", False, False)

    print "The value of gamma: ", alpha
    print "The value of x_min: ", x_min
