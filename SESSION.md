# Claude Code Session Context

This document contains comprehensive information about the current session for the ukraine_itn_wfst project.

---

## README

# WFST for Ukrainian ITN

Simple WFST for Ukrainian ITN based on NVIDIA NeMo and Pynini

### Installation

```shell
pip install ukr-itn
```

### Usage

```python
from ukr.wfst import normalize

normalize("це трапилося дві тисячі дев'ятнадцятого числа")  # це трапилося 2019 числа
normalize("мінус пять цілих одна десята відсотка")  # -5.1 %
normalize("двадцять дві тисячі сто один")  # 22101
```

#### From command line

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

#### JSON output

For more advanced usage you can get json output

```python
from ukr.wfst import normalize

normalize("це трапилося дві тисячі дев'ятнадцятого числа", json=True)
# >>> '[{"word": "це"}, {"word": "трапилося"}, {"ordinal": "2019"}, {"word": "числа"}]'
```

### How it works

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

---

## Environment Information

```
Working directory: /home/user/ukraine_itn_wfst
Is directory a git repo: Yes
Platform: linux
OS Version: Linux 4.4.0
Today's date: 2025-10-21
Git branch: claude/create-session-markdown-011CULWx3HrchnzyBoePGHgf
Git status: clean
```

### Recent Git Commits

```
90853cd Update version up to 0.1.8 and changelogs
3c91c36 Added additional cases for hours and zero minutes
c49a361 Use normalize everywhere instead of apply_fst_text
ce53478 WIP: use normalize methods in the tests
53744c5 WIP: added option to reorder tokens
```

---

## Running Processes

```
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  2.4  0.0  46040 12196 ?        Ssl  14:40   0:00 /process_api --addr 0.0.0.0:2024 --max-ws-buffer-size 32768 --cpu-shares 4096 --oom-polling-period-ms 100 --memory-limit-bytes 8589934592
root        19  0.0  0.0  10868  4424 ?        S    14:40   0:00 /bin/sh -c mkdir -p /home/user ; cd /home/user && /usr/local/bin/environment-manager task-run --stdin --session session_011CULWx3HrchnzyBoePGHgf --session-mode new --upgrade-claude-code=False >>/tmp/environment-manager.out 2>&1
root        21  0.9  0.4 1844684 55024 ?       Sl   14:40   0:00 /usr/local/bin/environment-manager task-run --stdin --session session_011CULWx3HrchnzyBoePGHgf --session-mode new --upgrade-claude-code=False
root        89  9.1  2.3 32936460 326068 ?     Sl   14:40   0:02 claude
root       584 19.3  0.0  16824 10324 ?        Ss   14:40   0:00 /bin/bash -c -l source /root/.claude/shell-snapshots/snapshot-bash-1761057628835-66l42n.sh && eval 'ps auxww' \< /dev/null && pwd -P >| /tmp/claude-72ab-cwd
root      1378  100  0.0  15956  8764 ?        R    14:40   0:00 ps auxww
root      1379  100  0.0  12580  1824 ?        R    14:40   0:00 git rev-parse --abbrev-ref HEAD
```

---

## Claude Settings

**Note:** The `.claude/settings.json` file does not exist in this project.

---

## Project File Structure

```
/home/user/ukraine_itn_wfst
/home/user/ukraine_itn_wfst/CHANGELOG.md
/home/user/ukraine_itn_wfst/.github
/home/user/ukraine_itn_wfst/.github/workflows
/home/user/ukraine_itn_wfst/.github/workflows/python-publish.yml
/home/user/ukraine_itn_wfst/requirements.txt
/home/user/ukraine_itn_wfst/MANIFEST.in
/home/user/ukraine_itn_wfst/.gitignore
/home/user/ukraine_itn_wfst/pyproject.toml
/home/user/ukraine_itn_wfst/.git
/home/user/ukraine_itn_wfst/.git/FETCH_HEAD
/home/user/ukraine_itn_wfst/.git/hooks
/home/user/ukraine_itn_wfst/.git/hooks/pre-receive.sample
/home/user/ukraine_itn_wfst/.git/hooks/push-to-checkout.sample
/home/user/ukraine_itn_wfst/.git/hooks/commit-msg.sample
/home/user/ukraine_itn_wfst/.git/hooks/prepare-commit-msg.sample
/home/user/ukraine_itn_wfst/.git/hooks/fsmonitor-watchman.sample
/home/user/ukraine_itn_wfst/.git/hooks/update.sample
/home/user/ukraine_itn_wfst/.git/hooks/post-update.sample
/home/user/ukraine_itn_wfst/.git/hooks/pre-applypatch.sample
/home/user/ukraine_itn_wfst/.git/hooks/applypatch-msg.sample
/home/user/ukraine_itn_wfst/.git/hooks/pre-rebase.sample
/home/user/ukraine_itn_wfst/.git/hooks/pre-merge-commit.sample
/home/user/ukraine_itn_wfst/.git/hooks/pre-push.sample
/home/user/ukraine_itn_wfst/.git/hooks/sendemail-validate.sample
/home/user/ukraine_itn_wfst/.git/hooks/pre-commit.sample
/home/user/ukraine_itn_wfst/.git/shallow
/home/user/ukraine_itn_wfst/.git/objects
/home/user/ukraine_itn_wfst/.git/objects/pack
/home/user/ukraine_itn_wfst/.git/objects/pack/pack-0dc05d6b14f1ee095d7d2a06dc2fbb0d7d381ef8.rev
/home/user/ukraine_itn_wfst/.git/objects/pack/pack-0dc05d6b14f1ee095d7d2a06dc2fbb0d7d381ef8.idx
/home/user/ukraine_itn_wfst/.git/objects/pack/pack-0dc05d6b14f1ee095d7d2a06dc2fbb0d7d381ef8.pack
/home/user/ukraine_itn_wfst/.git/objects/info
/home/user/ukraine_itn_wfst/.git/description
/home/user/ukraine_itn_wfst/.git/logs
/home/user/ukraine_itn_wfst/.git/logs/HEAD
/home/user/ukraine_itn_wfst/.git/logs/refs
/home/user/ukraine_itn_wfst/.git/logs/refs/remotes
/home/user/ukraine_itn_wfst/.git/logs/refs/remotes/origin
/home/user/ukraine_itn_wfst/.git/logs/refs/remotes/origin/claude
/home/user/ukraine_itn_wfst/.git/logs/refs/remotes/origin/claude/create-session-markdown-011CULWx3HrchnzyBoePGHgf
/home/user/ukraine_itn_wfst/.git/logs/refs/heads
/home/user/ukraine_itn_wfst/.git/logs/refs/heads/claude
/home/user/ukraine_itn_wfst/.git/logs/refs/heads/claude/create-session-markdown-011CULWx3HrchnzyBoePGHgf
/home/user/ukraine_itn_wfst/.git/HEAD
/home/user/ukraine_itn_wfst/.git/index
/home/user/ukraine_itn_wfst/.git/info
/home/user/ukraine_itn_wfst/.git/info/exclude
/home/user/ukraine_itn_wfst/.git/branches
/home/user/ukraine_itn_wfst/.git/refs
/home/user/ukraine_itn_wfst/.git/refs/tags
/home/user/ukraine_itn_wfst/.git/refs/remotes
/home/user/ukraine_itn_wfst/.git/refs/remotes/origin
/home/user/ukraine_itn_wfst/.git/refs/remotes/origin/claude
/home/user/ukraine_itn_wfst/.git/refs/remotes/origin/claude/create-session-markdown-011CULWx3HrchnzyBoePGHgf
/home/user/ukraine_itn_wfst/.git/refs/heads
/home/user/ukraine_itn_wfst/.git/refs/heads/claude
/home/user/ukraine_itn_wfst/.git/refs/heads/claude/create-session-markdown-011CULWx3HrchnzyBoePGHgf
/home/user/ukraine_itn_wfst/.git/config
/home/user/ukraine_itn_wfst/README.md
/home/user/ukraine_itn_wfst/requirements-dev.txt
/home/user/ukraine_itn_wfst/tests
/home/user/ukraine_itn_wfst/tests/test_decimal.py
/home/user/ukraine_itn_wfst/tests/test_time.py
/home/user/ukraine_itn_wfst/tests/test_utils.py
/home/user/ukraine_itn_wfst/tests/test_measure.py
/home/user/ukraine_itn_wfst/tests/test_word.py
/home/user/ukraine_itn_wfst/tests/test_ordinal.py
/home/user/ukraine_itn_wfst/tests/__init__.py
/home/user/ukraine_itn_wfst/tests/test_cardinal.py
/home/user/ukraine_itn_wfst/tests/test_money.py
/home/user/ukraine_itn_wfst/tests/test_date.py
/home/user/ukraine_itn_wfst/LICENSE
/home/user/ukraine_itn_wfst/ukr
/home/user/ukraine_itn_wfst/ukr/graph_utils.py
/home/user/ukraine_itn_wfst/ukr/utils.py
/home/user/ukraine_itn_wfst/ukr/__init__.py
/home/user/ukraine_itn_wfst/ukr/verbalizers
/home/user/ukraine_itn_wfst/ukr/verbalizers/decimal.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/cardinal.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/ordinal.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/verbalize.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/date.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/word.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/measure.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/__init__.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/money.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/time.py
/home/user/ukraine_itn_wfst/ukr/verbalizers/verbalize_final.py
/home/user/ukraine_itn_wfst/ukr/__main__.py
/home/user/ukraine_itn_wfst/ukr/taggers
/home/user/ukraine_itn_wfst/ukr/taggers/decimal.py
/home/user/ukraine_itn_wfst/ukr/taggers/cardinal.py
/home/user/ukraine_itn_wfst/ukr/taggers/tokenize_and_classify.py
/home/user/ukraine_itn_wfst/ukr/taggers/ordinal.py
/home/user/ukraine_itn_wfst/ukr/taggers/date.py
/home/user/ukraine_itn_wfst/ukr/taggers/word.py
/home/user/ukraine_itn_wfst/ukr/taggers/measure.py
/home/user/ukraine_itn_wfst/ukr/taggers/__init__.py
/home/user/ukraine_itn_wfst/ukr/taggers/money.py
/home/user/ukraine_itn_wfst/ukr/taggers/time.py
/home/user/ukraine_itn_wfst/ukr/data
/home/user/ukraine_itn_wfst/ukr/data/measurements.tsv
/home/user/ukraine_itn_wfst/ukr/data/currency
/home/user/ukraine_itn_wfst/ukr/data/currency/currency_major.tsv
/home/user/ukraine_itn_wfst/ukr/data/currency/currency_minor.tsv
/home/user/ukraine_itn_wfst/ukr/data/time
/home/user/ukraine_itn_wfst/ukr/data/time/to_hour.tsv
/home/user/ukraine_itn_wfst/ukr/data/time/__init__.py
/home/user/ukraine_itn_wfst/ukr/data/time/hours.tsv
/home/user/ukraine_itn_wfst/ukr/data/time/minute_to.tsv
/home/user/ukraine_itn_wfst/ukr/data/time/minutes.tsv
/home/user/ukraine_itn_wfst/ukr/data/month.tsv
/home/user/ukraine_itn_wfst/ukr/data/suppletive.tsv
/home/user/ukraine_itn_wfst/ukr/data/__init__.py
/home/user/ukraine_itn_wfst/ukr/data/numbers
/home/user/ukraine_itn_wfst/ukr/data/numbers/quantity.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/ordinal
/home/user/ukraine_itn_wfst/ukr/data/numbers/ordinal/ordinal_teen.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/ordinal/ordinal_digit.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/ordinal/ordinal_thousand.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/ordinal/ordinal_ties.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/ordinal/ordinal_hundred.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinals_billion.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/accusative
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/accusative/cardinals_digit.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/accusative/cardinals_ties.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/accusative/cardinals_zero.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/accusative/cardinals_hundred.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/accusative/cardinals_teen.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/instrumental
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/instrumental/cardinals_digit.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/instrumental/cardinals_ties.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/instrumental/cardinals_zero.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/instrumental/cardinals_hundred.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/instrumental/cardinals_teen.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/nominative
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/nominative/cardinals_digit.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/nominative/cardinals_ties.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/nominative/cardinals_zero.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/nominative/cardinals_hundred.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/nominative/cardinals_teen.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/genitive
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/genitive/cardinals_digit.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/genitive/cardinals_ties.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/genitive/cardinals_zero.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/genitive/cardinals_hundred.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/genitive/cardinals_teen.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/dative
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/dative/cardinals_digit.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/dative/cardinals_ties.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/dative/cardinals_zero.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/dative/cardinals_hundred.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/dative/cardinals_teen.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/prepositional
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/prepositional/cardinals_digit.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/prepositional/cardinals_ties.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/prepositional/cardinals_zero.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/prepositional/cardinals_hundred.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinal/prepositional/cardinals_teen.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinals_thousand.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/cardinals_million.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/decimal_delimiter.tsv
/home/user/ukraine_itn_wfst/ukr/data/numbers/__init__.py
/home/user/ukraine_itn_wfst/ukr/data/numbers/decimal_endings.tsv
/home/user/ukraine_itn_wfst/ukr/wfst.py
```

---

## Load Embedding File to API

To share this session context with new Claude Code sessions, this file has been uploaded to Anthropic's API storage.

### How to Load This Context in a New Session

Use the following command to retrieve and view this session context:

```bash
curl "https://api.anthropic.com/v1/files/{FILE_ID}" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

Replace `{FILE_ID}` with the actual file ID returned when this file was uploaded.

### Listing All Stored Files

To see all files stored in the API:

```bash
curl "https://api.anthropic.com/v1/files" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: files-api-2025-04-14"
```

---

**Session ID:** session_011CULWx3HrchnzyBoePGHgf
**Generated:** 2025-10-21
