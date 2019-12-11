import csv
import networkx as nx

def addNodeToGraph(graph_list, repo, path, func_name):
    if repo not in graph_list:
       new_graph = graph_list[repo] = nx.DiGraph()
       new_graph.add_node(repo, name=repo, type='repo')

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
            graph.add_node(element, name=element)
            graph.add_edge(curr_node, element)
            curr_node = element

def createRootedTree(graphs):
    rooted_list = []
    for repo, graph in graphs.items():
        #print(graph.nodes())
        #print(nx.get_node_attributes(graph, 'name'))
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
#print(rooted_list)

connected_graph = nx.algorithms.tree.operations.join(rooted_list)
connected_graph.nodes[0]['name'] = 'root'
#print(connected_graph.nodes())
#print(nx.get_node_attributes(connected_graph, 'name'))
#print(connected_graph.graph)
print("The single graph has " + str(len(connected_graph)) + " nodes.")

def performMapping(graph):
  with open('connected.emb', 'r') as f:
    reader = csv.reader(f)
    all_entries = list(reader)
    embeddings = []
    for entry in all_entries:
      if len(entry[0]) != 0:
        embeddings.append([float(i) for i in entry[1:]])

  #attributes = nx.get_node_attributes(graph, '_old')
  with open('mapping.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',')

    attrs = nx.get_node_attributes(graph, 'name')
    reverse = graph.reverse()
    #print(attrs)
    for idx, node in enumerate(graph.nodes()):
        if len(graph.in_edges(idx)):
          
          it = graph.neighbors(node)
          #print(idx)
          #print(list(it))
          #for i in it:
          #  print(attrs[i])
        #print(idx)
        #print(graph[idx]['name'])
        #print(attrs[idx])
        #print(embeddings[idx])
        #writer.writerow([idx, attrs[idx]] + embeddings[idx])

performMapping(connected_graph)

def writeConnectedGraph(graph):
  nx.write_edgelist(graph, "connectedNamed.edges")
  #nx.write_edgelist(nx.convert_node_labels_to_integers(graph), "graphs/connected.edges", data=False)

writeConnectedGraph(connected_graph)

def writeGraph(graph, i):
  nx.write_edgelist(nx.convert_node_labels_to_integers(graph), "graphs/" + str(i) + ".edges", data=False)

#for i, key in enumerate(graphs):
#   writeGraph(graphs[key], i)