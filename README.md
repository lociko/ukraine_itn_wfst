# WFST for Ukrainian ITN

Simple WFST for Ukrainian ITN based on NVIDIA NeMo and Pynini

## Installation

```shell
pip install ukr-itn
```

## Usage

```python
from ukr.wfst import graph, apply_fst_text

apply_fst_text("це трапилося дві тисячі дев'ятнадцятого числа", graph)  # це трапилося 2019 числа
apply_fst_text("мінус пять цілих одна десята відсотка", graph)  # -5.1 %
apply_fst_text("двадцять дві тисячі сто один", graph)  # 22101
```

### JSON output

For more advanced usage you can get json output

```python
from ukr.wfst import json_graph, apply_fst_text

apply_fst_text("це трапилося дві тисячі дев'ятнадцятого числа", json_graph)
# >>> '[{"word": "це"}, {"word": "трапилося"}, {"ordinal": "2019"}, {"word": "числа"}]' 
```

## How it works

We have two king of FST: taggers and verbalizers

This is a tagger:

```python
from ukr.wfst import classifyFst, apply_fst_text

apply_fst_text("мінус пять цілих одна десята відсотка", classifyFst.fst)  
```

will return `"measure { decimal { negative: "true" integer_part: "5" fractional_part: "1" } units: "%" }"`

And this is a verbalizers

```python
from ukr.wfst import verbalizeFinalFst, apply_fst_text

apply_fst_text('measure { decimal { negative: "true" integer_part: "5" fractional_part: "1" } units: "%" }', verbalizeFinalFst.fst)  
```

will return `-5.1 %`