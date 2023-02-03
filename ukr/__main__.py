import argparse
import sys

from ukr.wfst import graph, apply_fst_text

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inverse', action='store_true', help='inverse inverse text normalization')
args = parser.parse_args()

if args.inverse:
    graph = graph.invert()

for line in sys.stdin:
    print(apply_fst_text(line.strip(), graph))
