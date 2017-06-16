import argparse
import csv
import sys
import codecs
import networkx as nx

def init():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile_edges', dest='infile_edges', 
                        help='input file with edges in CSV format',
                        required=True)
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
    parser.add_argument('--outfile_graphml', dest='outfile_graphml', 
                        help='output file in GRAPHML format',
                        required=True)
    global args
    args = vars(parser.parse_args())
    print >> sys.stderr, args


def build_graph():

    G = nx.Graph()

if __name__ == '__main__':
    init()
    build_graph()
