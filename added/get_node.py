import matplotlib.pyplot as plt
import networkx as nx

"""
Given a dictionary of graphs, the repo, path and function name, this script returns the data associated with the corresponding node.
"""

# For testing purposes only
"""graphs = {}
graph = nx.DiGraph()
repo = "espressif/esptool"
graph.add_node(repo)
graph.add_node("ecdsa")
graph.add_edge(repo, "ecdsa")
graph.add_node("ecdsa.py")
graph.add_edge("ecdsa", "ecdsa.py")
graph.add_node("string_to_int")
graph.add_edge("ecdsa.py", "string_to_int")
graph.add_node("hi.py")
graphs[repo] = graph"""

predicted_nodes = []

def getNodeFromInfo(repo, path, func_name, graphs):
    if repo not in graphs:
        return None

    graph = graphs[repo]
    sub = path.split("/")
    sub[-1] = sub[-1][:sub[-1].find("#")]
    sub.append(func_name)

    curr_node = repo
    for i, element in enumerate(sub):
        found = False
        for original_node, new_node in graph.out_edges(curr_node):
            if new_node == element:
                found = True
                curr_node = new_node
        if not found:
            return None
        elif i == len(sub) - 1:
            return dict(graph.nodes(data=True))[new_node]

reader = open("model_submissions_python_paths.csv")
next(reader)
for i, l in enumerate(reader):
    parts = l.strip().split(",")
    if len(parts) == 4:
      repo, path, func_name, _ = parts
      predicted_nodes.append(getNodeFromInfo(repo, path, func_name, graphs))
print(predicted_nodes)