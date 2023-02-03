# Changelog

### v0.1.6

- Added command line execution mode: `echo "це трапилося дві тисячі дев'ятнадцятого числа" | python -m ukr`
- Fixed bug with single digits, like `"один одного"` (but was `"1 1"`). 
  Please note: single digit will normalize as written, like one -> one, two - two, ..., but eleven -> 11, twelve -> 12