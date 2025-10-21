# WFST for Ukrainian ITN

Simple WFST for Ukrainian ITN based on NVIDIA NeMo and Pynini

## Load Embedding File to API

For new Claude Code sessions, you can load the comprehensive session context that has been uploaded to Anthropic's API storage.

### View Session Context

To retrieve and view the session context file:

```bash
curl "https://api.anthropic.com/v1/files/file_011CULX88SByZJ9csZo8da9M" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

### List All Stored Files

To see all files stored in the API:

```bash
curl "https://api.anthropic.com/v1/files" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

The SESSION.md file contains:
- Project README
- Environment information
- Running processes
- Claude settings
- Complete file structure

## Installation

```shell
pip install ukr-itn
```

## Usage

```python
from ukr.wfst import normalize

normalize("це трапилося дві тисячі дев'ятнадцятого числа")  # це трапилося 2019 числа
normalize("мінус пять цілих одна десята відсотка")  # -5.1 %
normalize("двадцять дві тисячі сто один")  # 22101
```

### From command line

```shell
echo "це трапилося дві тисячі дев'ятнадцятого числа" | python -m ukr
```

```
Options:
  -h, --help     Show this help message and exit
  -j, --json     Return result as JSON
  -v, --verbose  Print original input and normalized to compare

```

Will return `це трапилося 2019-го числа`

### JSON output

For more advanced usage you can get json output

```python
from ukr.wfst import normalize

normalize("це трапилося дві тисячі дев'ятнадцятого числа", json=True)
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