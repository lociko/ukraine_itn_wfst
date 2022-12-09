# WFST for Ukrainian ITN

Simple WFST for Ukrainian ITN based on NVIDIA NeMo and Pynini

## Usage

```python
from ukr.wfst import graph, apply_fst_text

apply_fst_text("це трапилося дві тисячі девятнадцятого числа", graph)  # це трапилося 2019 числа
apply_fst_text("мінус пять цілих одна десята відсотка", graph)  # -5.1 %
apply_fst_text("двадцять дві тисячі сто один", graph)  # 22101
```