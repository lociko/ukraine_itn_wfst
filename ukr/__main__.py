import argparse
import sys

from ukr.wfst import graph, json_graph, apply_fst_text

parser = argparse.ArgumentParser(
    usage="echo \"це трапилося дев'ятнадцятого числа\" | python -m urk"
)
parser.add_argument('-i', '--inverse', action='store_true', help='inverse inverse text normalization')
parser.add_argument('-j', '--json', action='store_true', help='return result as JSON')
parser.add_argument('-v', '--verbose', action='store_true', help='Print original input and normalized to compare')
args = parser.parse_args()

if args.inverse:
    graph = graph.invert()

main_graph = json_graph if args.json else graph

for line in sys.stdin:
    print(apply_fst_text(line.strip(), main_graph))
    if args.verbose:
        print(line)
