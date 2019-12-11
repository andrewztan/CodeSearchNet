import csv
import networkx as nx

def addNodeToGraph(graph, repo, path, func_name):
    if repo not in graph.nodes():
       graph.add_node(repo, name=repo, type='repo')
       graph.add_edge('root', repo)

    sub = path.split("/")
    #sub.append(func_name)
    prefix = repo
    curr_node = repo
    for element in sub:
        found = False
        for node, _ in graph.out_edges(curr_node):
            if node == element:
                found = True
                curr_node = node
        if not found:
            node_name = prefix + '/' + element
            graph.add_node(node_name, name=element, type='path', repo = repo)
            graph.add_edge(curr_node, node_name)
            curr_node = node_name
            prefix = prefix + '/' + element
    node_name = prefix + '/' + func_name
    graph.add_node(node_name, name=func_name, type='func', repo = repo, path = prefix)
    graph.add_edge(curr_node, node_name)

def performMapping(graph):
  with open('connected.emb', 'r') as f:
    reader = csv.reader(f)
    all_entries = list(reader)
    embeddings = []
    for entry in all_entries:
      if len(entry[0]) != 0:
        embeddings.append([float(i) for i in entry[1:]])

  with open('mapping.csv', mode='w') as f:
    writer = csv.writer(f, delimiter=',')

    attrs = nx.get_node_attributes(graph, 'type')
    #print(attrs)
    #print(graph.nodes())
    for idx, node in enumerate(graph.nodes()):
        #print(attrs)
        if graph.node[node]['type'] == 'func':
          n = graph.node[node]
          #print(node)
          #print(graph.node[node])
          it = graph.predecessors(node)
          #print(list(it))
          writer.writerow([idx, n['repo'], n['path'], n['name']] + embeddings[idx])

def writeGraph(graph):
  nx.write_edgelist(nx.convert_node_labels_to_integers(graph), 'connected.edges', data=False)

connected_graph = nx.DiGraph() # Single graph connecting all of the disjoint graphs
connected_graph.add_node('root', name='root', type='root')
with open('python_paths.csv', 'r') as f:
    reader = csv.reader(f)
    all_entries = list(reader)
    for entry in all_entries:
        addNodeToGraph(connected_graph, entry[7], entry[8], entry[3])


print("The single graph has " + str(len(connected_graph)) + " nodes.")

#nx.draw(connected_graph)
#writeGraph(connected_graph)
performMapping(connected_graph)

