# WFST for Ukrainian ITN

Simple WFST for Ukrainian ITN based on NVIDIA NeMo and Pynini

## Usage

```python
from ukr.wfst import graph, apply_fst_text

apply_fst_text("це трапилося дві тисячі девятнадцятого числа", graph)  # це трапилося 2019 числа
apply_fst_text("мінус пять цілих одна десята відсотка", graph)  # -5.1 %
apply_fst_text("двадцять дві тисячі сто один", graph)  # 22101
```

## How it works

We have two king of FST: taggers and verbalizers

This is a tagger:

```python
from ukr.wfst import tMeasureFst, apply_fst_text

apply_fst_text("мінус пять цілих одна десята відсотка", tMeasureFst)  
```

will return `"measure { decimal { negative: "true" integer_part: "5" fractional_part: "1" } units: "%" }"`

And this is a verbalizers

```python
from ukr.wfst import vMeasureFst, apply_fst_text

apply_fst_text('measure { decimal { negative: "true" integer_part: "5" fractional_part: "1" } units: "%" }', vMeasureFst)  
```

will return `-5.1 %`