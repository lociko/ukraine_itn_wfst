# Changelog

### v0.1.8

- Added TIME class, some examples:
    - `"сьома година двадцять п'ять хвилин"` -> `'07:25'`
    - `"о пів на десяту"` -> `'09:30'`
    - `"пів на третю"` -> `'02:30'`
    - `"чверть на одинадцяту"` -> `'10:15'`
    - `"за чверть одинадцята"` -> `'10:45'`
    - `"п'ять хвилин на дванадцяту"` -> `'11:05'`
    - `"дванадцята нуль нуль"` -> `'12:00'`
    - `"одинадцята нуль шість"` -> `'11:06'`
    - `"шоста сорок три"` -> `'06:43'`
- Defined new method `normalize` which should be used istead of `apply_fst_text` in production code.
  The reason is we need additional code to process some non-deterministic cases like for time class (for example minutes goes before hours).

### v0.1.7

- Added DATE class:
    - `"першого січня дві тисячі першого року"` -> `1 січня 2001 року'`
    - `"першого січня"` -> `1 січня'`
    - `"січень дві тисячі першого рок у"` -> `січень 2001 року'`
    - `"січень дві тисячі першого"` -> `січень 2001'`
    - `"дві тисячі першого рік"` -> `2001 рік'`
    - `"дев'ятсот сорок п'ятий рік до нашої ери"` -> `945 рік до н. е.'`
- Added JSON option for command line

### v0.1.6

- Added command line execution mode: `echo "це трапилося дві тисячі дев'ятнадцятого числа" | python -m ukr`
- Fixed bug with single digits, like `"один одного"` (but was `"1 1"`).
  Please note: single digit will normalize as written, like one -> one, two - two, ..., but eleven -> 11, twelve -> 12