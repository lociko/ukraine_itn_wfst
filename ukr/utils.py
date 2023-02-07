import csv
import os
import re


def get_abs_path(rel_path):
    """
    Get absolute path

    Args:
        rel_path: relative path to this file
        
    Returns absolute path
    """
    abs_path = os.path.dirname(os.path.abspath(__file__)) + os.sep + rel_path

    if not os.path.exists(abs_path):
        print(f'{abs_path} does not exist')
    return abs_path


def load_labels(abs_path):
    """
    loads relative path file as dictionary

    Args:
        abs_path: absolute path

    Returns dictionary of mappings
    """
    label_tsv = open(abs_path)
    labels = list(csv.reader(label_tsv, delimiter="\t"))
    return labels


REORDER_PATTERN = r'(?P<second>\w+: ".*?")>> (?P<first>\w+: ".*")'


def reorder(tagged_text):
    """
    Change the order of tags if required. For example:
    >>> reorder('tokens { time { minutes: "05">> hours: "11" } }')
    # tokens { time { hours: "11" minutes: "05"} }
    """
    res = []
    for tag in tagged_text.split('tokens '):
        match = re.search(REORDER_PATTERN, tag)
        if match:
            groups = match.groupdict()

            original = f"{groups['second']}>> {groups['first']}"
            reordered = f"{groups['first']} {groups['second']}"
            new = tag.replace(original, reordered)

            res.append(new)
        else:
            res.append(tag)

    return 'tokens '.join(res)
