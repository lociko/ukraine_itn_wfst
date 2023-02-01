import sys
from ukr.wfst import graph, apply_fst_text

for line in sys.stdin:
    print(apply_fst_text(line.strip(), graph))