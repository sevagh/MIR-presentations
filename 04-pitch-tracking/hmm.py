import networkx as nx
import pydot

states = ['A1', 'A#1', 'B1' ,'C2']

# create graph object
G = nx.DiGraph(rankdir="TB")

# nodes correspond to states
G.add_nodes_from(states)
print(f'Nodes:\n{G.nodes()}\n')

G.add_edge('A#1', 'A1', weight=0.2, label=0.2)
G.add_edge('A1', 'B1', weight=0.3, label=0.3)
G.add_edge('A#1', 'B1', weight=0.45, label=0.4)
G.add_edge('B1', 'C2', weight=0.15, label=0.15)
G.add_edge('C2', 'B1', weight=0.15, label=0.15)

pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='dot')
nx.draw_networkx(G, pos)

# create edge labels for jupyter plot but is not necessary
edge_labels = {(n1,n2):d['label'] for n1,n2,d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G , pos, edge_labels=edge_labels)
nx.drawing.nx_pydot.write_dot(G, 'hmm.dot')
