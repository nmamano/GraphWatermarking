
def remove_repeated_edges(file):
    edges = set()
    nodes = dict()
    with open(file, 'r') as fin:
        for line in fin:
            if line[0] == '#':
                continue
            edge = line.split()
            node1, node2 = int(edge[0]), int(edge[1])
            if node1 == node2:
                continue
            if node1 in nodes:
                node1 = nodes[node1]
            else:
                new_value = len(nodes)
                nodes[node1] = new_value
                node1 = new_value
            if node2 in nodes:
                node2 = nodes[node2]
            else:
                new_value = len(nodes)
                nodes[node2] = new_value
                node2 = new_value
            if node1 > node2:
                node1, node2 = node2, node1
            edges.add((node1, node2))
    with open(file+"_2", 'w') as fout:
        for node1, node2 in edges:
            fout.write(str(node1)+" "+str(node2)+"\n")

remove_repeated_edges("../networks/youtube/youtube")
