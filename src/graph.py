"""
Class to represent graphs
"""
import math
from utils import printts, list_head_to_string

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

    def print_adj_lists(self):
        """ prints all the adjacency lists """
        for i in range(self.num_nodes()):
            print(i, ': ', sep='', end='')
            print(self.adj_lists[i])

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

    def print_deg_dist(self, max_count=30):
        """
        prints the number of nodes per degree,
        in decreasing order, starting with max_deg
        """
        deg_dist = self.get_deg_dist()
        count = 0
        printts("Degree distribution:")
        for i in range(len(deg_dist)-1, -1, -1):
            if deg_dist[i] != 0:
                if count > 0:
                    print(', ', end='')
                if count >= max_count:
                    print('...')
                    return
                print(i, ': ', deg_dist[i], sep='', end='')
                count += 1

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

    def deg_separation(self, node):
        """
        returns the minimum degree difference between
        a node and any other node in the graph
        note: separation is the same as difference,
        e.g. two nodes with degree 5 and 6 have
        separation 1, not 0

        """
        deg_dist = self.get_deg_dist()
        deg = self.deg(node)
        if deg_dist[deg] > 1:
            return 0
        next_deg_below = deg-1
        while deg_dist[next_deg_below] == 0:
            next_deg_below -= 1
        next_deg_above = deg+1
        while deg_dist[next_deg_above] == 0:
            next_deg_above += 1

        sep_below = deg-next_deg_below
        sep_above = next_deg_above-deg
        return min(sep_below, sep_above)


    def get_separated_degs(self, separation):
        """
        returns the degrees corresponding to nodes
        separated a number of degrees
        note: separation is the same as difference,
        e.g. two nodes with degree 5 and 6 have
        separation 1, not 0

        """
        deg_dist = self.get_deg_dist()
        deg2count_list = []
        for deg, freq in enumerate(deg_dist):
            if freq > 0:
                deg2count_list.append((deg, freq))

        deg = lambda i: deg2count_list[i][0]
        freq = lambda i: deg2count_list[i][1]

        num_degs = len(deg2count_list)
        well_sep_degs = [True for i in range(num_degs)]

        for i in range(num_degs):
            if freq(i) != 1:
                well_sep_degs[i] = False
            if i > 0 and deg(i) - deg(i-1) < separation:
                well_sep_degs[i] = False
            if i < num_degs-1 and deg(i+1) - deg(i) < separation:
                well_sep_degs[i] = False

        res = []
        for i in range(num_degs):
            if well_sep_degs[i]:
                res.append(deg(i))
        return res

    def num_separated_nodes(self, separation):
        """
        returns the number of nodes separated a number of degrees
        note: separation is the same as difference,
        e.g. two nodes with degree 5 and 6 have
        separation 1, not 0

        """
        return len(self.get_separated_degs(separation))

    def num_unique_deg_nodes(self):
        """
        number of nodes with unique degree
        """
        deg_dist = self.get_deg_dist()
        return sum((1 if n == 1 else 0) for n in deg_dist)
        #equivalent to
        #return self.num_separated_nodes(1)

    def num_consecutive_unique_deg_nodes(self):
        """ number of nodes with unique degree,
        in decreasing order of degree,
        until the first node without unique degree """
        deg_dist = self.get_deg_dist()
        count = 0
        for i in range(len(deg_dist)-1, -1, -1):
            if deg_dist[i] == 1:
                count += 1
            elif deg_dist[i] > 1:
                return count
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

    def valid_thresholds(self):
        """ returns the numbers k such that if you group nodes by degree
        and pick the k nodes with highest degree, you don't pick any group partially.
        sorted in increasing order """
        deg_dist = self.get_deg_dist()
        res = [0]
        for num_nodes_with_deg in reversed(deg_dist):
            if num_nodes_with_deg > 0:
                res.append(res[len(res)-1]+num_nodes_with_deg)
        return res

    def prev_valid_threshold(self, threshold):
        """ returns the largest valid threshold smaller than threshold.
        a valid threshold is a number such that if you group nodes by degree
        and pick the k nodes with highest degree, you don't pick any group partially.
        """
        valids = self.valid_thresholds()
        if valids[0] > threshold:
            raise Exception("there is no valide threshold smaller than "+str(threshold))
        i = 0
        while i < len(valids)-1 and valids[i] <= threshold:
            i += 1
        return valids[i-1]

    def dk2_map(self):
        """ returns a map where the key are sorted pairs of degrees, and the values
        the number of edges in the graph such that their endpoints have those degrees.
        it contains only keys for degree pairs with at least one edge. """
        res = dict()
        for node1, node2 in self.get_edge_list():
            deg1 = self.deg(node1)
            deg2 = self.deg(node2)
            if deg1 > deg2:
                deg1, deg2 = deg2, deg1
            if (deg1, deg2) in res:
                res[(deg1, deg2)] = res[(deg1, deg2)] + 1
            else:
                res[(deg1, deg2)] = 1
        return res

    def print_statistics(self, verbose=False):
        """
        prints details about the graph
        """
        if not verbose:
            printts('n: '+str(self.num_nodes())+', m: '+str(self.num_edges())+
                    ', max/avg deg: '+str(self.max_deg())+'/'+str(round(self.avg_deg(), 2))+
                    ', unique degs: '+str(self.num_unique_deg_nodes())+
                    ' ('+str(self.num_consecutive_unique_deg_nodes())+' consecutive)')
            return

        printts('num nodes (n): '+str(self.num_nodes()))
        printts('num edges: '+str(self.num_edges()))
        printts('max degree: '+str(self.max_deg()))
        printts('average degree: '+str(self.avg_deg()))
        num_unique = self.num_unique_deg_nodes()
        printts('unique degree vertices: '+str(num_unique))
        num_cons_unique = self.num_consecutive_unique_deg_nodes()
        printts('consecutive unique degree vertices: '+str(num_cons_unique))
        if verbose:
            printts('log(n): '+str(math.log(self.num_nodes())))
            printts('sqrt(n): '+str(math.sqrt(float(self.num_nodes()))))
            for i in range(1, 10):
                degs = self.num_separated_nodes(i)
                deg_summary = 'degrees with '+str(i)+' sep: '+str(degs)
                if degs > 0:
                    deg_summary += " "
                    nodes = self.get_separated_degs(i)
                    deg_summary += list_head_to_string(nodes, max_items=10)
                printts(deg_summary)

            self.print_deg_dist(max_count=15)
            printts('nodes sorted by degree:')
            for i, node in enumerate(self.nodes_sorted_by_degree()):
                print(node, ': ', self.deg(node), sep='', end='')
                if i == 14:
                    print()
                    break
                else:
                    print(', ', end='')

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
