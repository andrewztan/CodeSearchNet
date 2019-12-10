import csv
import networkx as nx

def addNodeToGraph(graph_list, repo, path, func_name):
    if repo not in graph_list:
       new_graph = graph_list[repo] = nx.DiGraph()
       new_graph.add_node(repo)

    graph = graph_list[repo]
    sub = path.split("/")
    sub.append(func_name)

    curr_node = repo
    for element in sub:
        found = False
        for node, _ in graph.out_edges(curr_node):
            if node == element:
                found = True
                curr_node = node
        if not found:
            graph.add_node(element)
            graph.add_edge(curr_node, element)
            curr_node = element

def createRootedTree(graphs):
    rooted_list = []
    for repo, graph in graphs.items():
        print(graph.nodes())
        rooted_list.append((graph, repo))
    return rooted_list

graphs = {} # Dictionary of key = repo, value = NetworkX Graph object
connected_graph = nx.DiGraph() # Single graph connecting all of the disjoint graphs

with open('python_paths.csv', 'r') as f:
  	reader = csv.reader(f)
  	all_entries = list(reader)
  	for entry in all_entries:
  		addNodeToGraph(graphs, entry[7], entry[8], entry[3])

rooted_list = createRootedTree(graphs)
connected_graph = nx.algorithms.tree.operations.join(rooted_list)
print("The single graph has " + str(len(connected_graph)) + " nodes.")


