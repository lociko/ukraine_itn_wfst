import argparse
import sys

from ukr.wfst import normalize

parser = argparse.ArgumentParser(
    usage="echo \"це трапилося дев'ятнадцятого числа\" | python -m urk"
)
parser.add_argument('-i', '--inverse', action='store_true', help='inverse inverse text normalization')
parser.add_argument('-j', '--json', action='store_true', help='return result as JSON')
parser.add_argument('-v', '--verbose', action='store_true', help='Print original input and normalized to compare')
args = parser.parse_args()

if args.inverse:
    raise ValueError("'--inverse' option not implement yet")

for line in sys.stdin:
    print(normalize(line.strip(), args.json))
    if args.verbose:
        print(line)
