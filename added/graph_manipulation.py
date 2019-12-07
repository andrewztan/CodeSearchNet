import json
import matplotlib.pyplot as plt
import networkx as nx

graphs = {}
data = []
predicted_nodes = []

for line in open('python_test_0.jsonl', 'r'):
    data.append(json.loads(line))

def addNodeToGraph(path, func_name, repo, graph_list):
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

for i, datapoint in enumerate(data):
   addNodeToGraph(datapoint["path"], datapoint["func_name"], datapoint["repo"], graphs)

print("There are " + str(len(graphs)) + " graphs in total.")

"""nx.draw(graphs[datapoint["repo"]])
plt.draw()
plt.show()"""