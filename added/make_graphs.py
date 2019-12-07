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

def getNodeFromInfo(repo, path, func_name, graphs):
   if repo not in graphs:
      return None

   graph = graphs[repo]
   sub = path.split("/")
   sub.append(func_name)

   curr_node = repo
   for i, element in enumerate(sub):
      found = False
      for node, _ in graph.out_edges(curr_node):
         if node == element:
            found = True
            curr_node = node
      if not found:
         return None
      elif i == len(sub) - 1:
         return node


for i, datapoint in enumerate(data):
   addNodeToGraph(datapoint["path"], datapoint["func_name"], datapoint["repo"], graphs)

print("There are " + str(len(graphs)) + " graphs in total.")

reader = open("model_submissions_python_paths.csv")
next(reader)
for l in reader:
    parts = l.strip().split(",")
    if len(parts) == 4:
      repo, path, func_name, _ = parts
      predicted_nodes.append(getNodeFromInfo(repo, path, func_name, graphs))
print(predicted_nodes)



"""nx.draw(graphs[datapoint["repo"]])
plt.draw()
plt.show()"""