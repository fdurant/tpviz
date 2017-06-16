import argparse
import csv
import sys
import codecs
import networkx as nx
from math import log

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile_edges', dest='infile_edges', 
                        help='input file with edges in CSV format',
                        required=True)
    parser.add_argument('--infile_delimiter', dest='infile_delimiter', 
                        help='field delimiter in the input file',
                        default="\t")
    parser.add_argument('--source_id_fieldname', dest='source_id_fieldname', 
                        help='name of the header field in the input file that refers to the source id',
                        default="source")
    parser.add_argument('--target_id_fieldname', dest='target_id_fieldname', 
                        help='name of the header field in the input file that refers to the target id',
                        default="target")
    parser.add_argument('--source_label_fieldname', dest='source_label_fieldname', 
                        help='name of the header field in the input file that refers to the source label',
                        required=True)
    parser.add_argument('--target_label_fieldname', dest='target_label_fieldname', 
                        help='name of the header field in the input file that refers to the target label',
                        required=True)
    parser.add_argument('--edge_label_fieldname', dest='edge_label_fieldname', 
                        help='name of the header field in the input file that refers to the edge label',
                        required=True)
    node_size_choices = [None,'degree','log10degree','log2degree']
    parser.add_argument('--source_node_size', dest='source_node_size', 
                        help='calculation method for size of source nodes',
                        choices=node_size_choices,
                        default=None)
    parser.add_argument('--source_min_node_size', dest='source_min_node_size', 
                        help='minimum size of a source node',
                        type=int,
                        default=1)
    parser.add_argument('--source_node_size_multiplier', dest='source_node_size_multiplier', 
                        type=float,
                        default=1)
    parser.add_argument('--target_node_size', dest='target_node_size', 
                        help='calculation method for size of target nodes',
                        choices=node_size_choices,
                        default=None)
    parser.add_argument('--target_min_node_size', dest='target_min_node_size', 
                        help='minimum size of a target node',
                        type=int,
                        default=1)
    parser.add_argument('--target_node_size_multiplier', dest='target_node_size_multiplier', 
                        type=float,
                        default=1)
    parser.add_argument('--outfile_graphml', dest='outfile_graphml', 
                        help='output file in GRAPHML format',
                        required=True)
    global args
    args = vars(parser.parse_args())
    print >> sys.stderr, args


def build_graph():

    global G
    G = nx.Graph()

    edgesFH = open(args['infile_edges'], 'rb')
    myReader = csv.reader(edgesFH, delimiter=args['infile_delimiter'])

    header = myReader.next()
    print >> sys.stderr, "header = ", header

    for row in myReader:
        srcId = row[header.index(args['source_id_fieldname'])]
#        print >> sys.stderr, "srcId = ", srcId
        targetId = row[header.index(args['target_id_fieldname'])]
        srcLabel = row[header.index(args['source_label_fieldname'])]
        targetLabel = row[header.index(args['target_label_fieldname'])]
        edgeLabel = row[header.index(args['edge_label_fieldname'])]

        # Create nodes if they do not exist yet
        if not G.has_node(srcId):
            G.add_node(srcId, {'type': args['source_id_fieldname'], 'label': srcLabel})

        if not G.has_node(targetId):
            G.add_node(targetId, {'type': args['target_id_fieldname'], 'label': targetLabel})

        if not G.has_edge(srcId, targetId):
            G.add_edge(srcId, targetId, { 'label':edgeLabel})

    d = nx.degree(G)

    for k,degree in d.items():
        if not args['source_node_size'] is None:
            if G.node[k]['type'] == args['source_id_fieldname']:
                G.node[k]['size'] = calc_node_size(args['source_node_size'],
                                                   degree,
                                                   args['source_min_node_size'],
                                                   args['source_node_size_multiplier']) 
        if not args['target_node_size'] is None:
            if G.node[k]['type'] == args['target_id_fieldname']:
                G.node[k]['size'] = calc_node_size(args['target_node_size'],
                                                   degree,
                                                   args['target_min_node_size'],
                                                   args['target_node_size_multiplier']) 

def calc_node_size(choice, number, minsize=1.0, multiplier=1.0):

    assert(type(number) == type(1))
    assert(not choice is None)

    if choice == 'degree':
        return minsize + (number * multiplier)
    elif choice == 'log2degree':
        return minsize + (log(number, 2) * multiplier)
    elif choice == 'log10degree':
        return minsize + (log(number, 10) * multiplier)
    else:
        throw('Should not happen')

def write_graph():
    print >> sys.stderr, "Writing graph %s with %d nodes and %d edges ... " % (args['outfile_graphml'], nx.number_of_nodes(G), nx.number_of_edges(G)),
    nx.write_graphml(G, args['outfile_graphml'], 'iso-8859-1')
    print >> sys.stderr, "done"

if __name__ == '__main__':
    init()
    build_graph()
    write_graph()
