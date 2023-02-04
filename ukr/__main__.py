import argparse
import sys

from ukr.wfst import graph, json_graph, apply_fst_text

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inverse', action='store_true', help='inverse inverse text normalization')
parser.add_argument('-j', '--json', action='store_true', help='inverse inverse text normalization')
args = parser.parse_args()

if args.inverse:
    graph = graph.invert()

main_graph = json_graph if args.json else graph

for line in sys.stdin:
    print(apply_fst_text(line.strip(), main_graph))
