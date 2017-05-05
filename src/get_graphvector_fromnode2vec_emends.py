import os,sys,json,glob
from pprint import pprint
import networkx as nx
from collections import defaultdict
import numpy as np
from joblib import Parallel,delayed
import psutil

def get_graphvector_from_nodevectors (fname, nodelabel_to_embed_map):
    try:
        g = nx.read_gexf (fname)
        print 'loaded graph with {} nodes and {} edges from {}'.format(g.number_of_nodes(),
                                                                       g.number_of_edges(),
                                                                       fname)
    except:
        print 'unable to load ',fname
        return None

    nodelabel_to_freq_cnt = defaultdict(int)
    for node, attr_dict in g.nodes_iter(data=True):
        nodelabel = attr_dict['APIs']
        nodelabel_to_freq_cnt[nodelabel] += 1
    # pprint (nodelabel_to_freq_cnt)

    scaled_nodevectors = []
    for nodelabel,nodefreq in nodelabel_to_freq_cnt.iteritems():
        try:
            scalednodevector = nodefreq * nodelabel_to_embed_map[nodelabel]
        except:
            continue
        scaled_nodevectors.append(scalednodevector)

    # pprint (scaled_nodevectors)
    scaled_nodevectors = np.array (scaled_nodevectors)
    # print scaled_nodevectors.shape
    graph_vector = np.sum(scaled_nodevectors,axis=0)
    graph_vector = graph_vector/float(g.number_of_nodes())
    # print graph_vector.shape
    # raw_input()
    return graph_vector





# nodelabel_to_embed_map_fname = '/mnt/nas239/anna/drebin_combined_ADG.json'
# graphs_folder = '../../tmp/DrebinADGs/'
# op_fname = nodelabel_to_embed_map_fname.replace('.json','_graphvectors.json')

nodelabel_to_embed_map_fname = sys.argv[1]
graphs_folder = sys.argv[2]
op_fname = sys.argv[3]
n_cpus = psutil.cpu_count()

with open(nodelabel_to_embed_map_fname) as fh:
    nodelabel_to_embed_map = json.load(fh)
print 'loaded dict with {} node labels as keys ' \
      'and their node2vec embeds as values'.format(len(nodelabel_to_embed_map.keys()))

nodelabel_to_embed_map = {nlabel:np.array(vect) for nlabel, vect in nodelabel_to_embed_map.iteritems()}

adg_fnames = glob.glob( os.path.join(graphs_folder, 'APKs_chunk_0*.gexf'))
# adg_fnames = glob.glob( os.path.join(graphs_folder, '*.gexf'))
adg_fnames.sort()
print 'loaded {} graph files from {}'.format(len(adg_fnames),graphs_folder)
raw_input('hit any key to get graph vectors for these graphs using node2vec...')

# Parallel(n_jobs=2)(delayed(sqrt)(i ** 2) for i in range(10))
graph_vectors = Parallel(n_jobs=n_cpus)(delayed(get_graphvector_from_nodevectors)
                                        (fname, nodelabel_to_embed_map) for fname in adg_fnames)

graph_fname_to_vector_map = {fname:graph_vectors[i].tolist() for i,fname in enumerate(adg_fnames)}

with open(op_fname,'w') as fh:
    json.dump(graph_fname_to_vector_map,fh,indent=4)
