import os,sys,json
import networkx as nx
from pprint import pprint

tgt_graph_fame = sys.argv[1]
edge_list_fname = tgt_graph_fame.replace('.gexf','.edge_list')
nodelabe_to_id_map_fname = tgt_graph_fame.replace('.gexf','nodelabel_to_id_map.json')

g = nx.read_gexf(tgt_graph_fame)

print 'loaded graph from {}, # nodes: {} and #edges: {}'.format(tgt_graph_fame,
                                                                g.number_of_nodes(),
                                                                g.number_of_edges())

unique_node_labels = list(set([g.node[node]['APIs'] for node in g.nodes_iter()]))
unique_node_labels.sort()
nodelabel_to_id_map = {label:i for i, label in enumerate(unique_node_labels)}
print 'found {} unique node labels'.format(len(unique_node_labels))


edge_list = []
for node1, node2 in g.edges_iter():
    node1 = nodelabel_to_id_map[g.node[node1]['APIs']]
    node2 = nodelabel_to_id_map[g.node[node2]['APIs']]
    edge_list.append(str(node1) + ' ' + str(node2))

with open (edge_list_fname,'w') as fh:
    for edge in edge_list:
        print >>fh, edge
print 'dumped the edge list in file: ', edge_list_fname

with open(nodelabe_to_id_map_fname, 'w') as fp:
    json.dump(nodelabel_to_id_map,fp,indent=4)
print 'dumped the node_label to id map dict in file: ',nodelabe_to_id_map_fname