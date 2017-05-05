import os,sys,json
from pprint import pprint
import networkx as nx

def combine_all_graphs(all_g_fnames):
    total_fnames = len(all_g_fnames)
    comb_g = nx.Graph()
    for i,fname in enumerate(all_g_fnames):
        print 'before: ', comb_g.number_of_nodes()
        comb_g = nx.compose(comb_g, nx.read_gexf(fname))
        print 'before: ', comb_g.number_of_nodes()
        print 'done with graph: {}/{}'.format(i,total_fnames)
    return comb_g


def main ():
    tgt_dir_list = ['../../tmp/DrebinADGs']
    extn = '.gexf'
    full_g_fname = '/mnt/nas239/anna/drebin_combined_ADG.gexf'

    tgt_files = []
    for tgt_dir in tgt_dir_list:
        for root,folders,files in os.walk(tgt_dir):
            for f in files:
                if f.endswith(extn):
                    tgt_files.append(os.path.join(root,f))

    print 'loaded {} files from {}'.format(len(tgt_files),tgt_dir_list)
    raw_input()

    comb_g = combine_all_graphs(tgt_files)

    nx.write_gexf(G=comb_g,path=full_g_fname,prettyprint=True)



if __name__ == '__main__':
    main ()


