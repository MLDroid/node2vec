import os,sys,json
from pprint import pprint

def load_node2vec_emb_as_dict (emb_fname):
    nodeid_to_vec_map = {}
    lines = [l.strip() for l in open (emb_fname)][1:]
    for l in lines:
        parts = l.split()
        key = parts[0]
        value = [float(v) for v in parts[1:]]
        nodeid_to_vec_map[key] = value
    return nodeid_to_vec_map


# nodelabel_to_id_map_fname = 'drebin_combined_ADGnodelabel_to_id_map.json'
# emb_fname = 'drebin_combined_ADG.embeds'

nodelabel_to_id_map_fname = sys.argv[1]
emb_fname = sys.argv[2]
op_fname = emb_fname.replace('.embeds','.json')

with open (nodelabel_to_id_map_fname) as fh:
    nodelabel_to_id_map = json.load(fh)
nodeid_to_label_map = {v:k for k,v in nodelabel_to_id_map.iteritems()}
del nodelabel_to_id_map

nodeid_to_vector_map = load_node2vec_emb_as_dict (emb_fname)
# pprint (nodeid_to_vector_map)
# raw_input()
nodelabe_to_vector_map = {nodeid_to_label_map[int(id)]:vect for id,vect in nodeid_to_vector_map.iteritems()}

with open(op_fname,'w') as fh:
    json.dump(nodelabe_to_vector_map,fh,indent=4)

