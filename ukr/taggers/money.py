from collections import defaultdict

import pynini
from pynini.lib import pynutil

from ukr.graph_utils import (
    GraphFst,
    NEMO_DIGIT,
    delete_space,
)

from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.decimal import DecimalFst
from ukr.utils import get_abs_path, load_labels


def load_currency(file_path):
    labels = load_labels(file_path)

    mapping = defaultdict(list)
    for k, v in labels:
        mapping[k].append(v)

    for k in mapping:
        mapping[k] = pynini.union(*mapping[k]).optimize()

    return mapping


class MoneyFst(GraphFst):
    """
    Finite state transducer for classifying money
        e.g. twelve dollars and five cents -> money { integer_part: "12" fractional_part: 05 currency: "$" }

    Args:
        cardinal: CardinalFst
        decimal: DecimalFst
    """

    def __init__(self, cardinal: CardinalFst, decimal: DecimalFst):
        super().__init__(name="money", kind="classify")

        integer_graph = pynutil.insert("integer_part: \"") + cardinal.graph + pynutil.insert("\" ")
        decimal_graph = decimal.graph

        # сім копійок -> 0.07
        # двадцять сім копійок -> 0.27
        add_leading_zero_to_double_digit = (NEMO_DIGIT + NEMO_DIGIT) | (pynutil.insert("0") + NEMO_DIGIT)
        fractional_graph = pynutil.insert("fractional_part: \"") + cardinal.graph @ add_leading_zero_to_double_digit + pynutil.insert("\"")

        unit_majors = load_currency(get_abs_path("data/currency/currency_major.tsv"))
        unit_minors = load_currency(get_abs_path("data/currency/currency_minor.tsv"))

        units = []
        optional_and = pynini.closure(delete_space + pynutil.delete("і"), 0, 1)
        for signature, major in unit_majors.items():
            minor = unit_minors[signature]

            # just integer: one dollar, two dollars
            integer_part = integer_graph + delete_space + pynutil.delete(major)
            units.append(pynutil.insert(f"currency: \"{signature}\" ") + integer_part)

            # just integer and fractional: one dollar and two cents, two dollars two cents, etc.
            fractional_part = fractional_graph + delete_space + pynutil.delete(minor)
            unit = integer_part + optional_and + delete_space + fractional_part
            units.append(pynutil.insert(f"currency: \"{signature}\" ") + unit)

            # just fractional: two cents, one cents, etc.
            integer_part = pynutil.insert("integer_part: \"0\" ")
            fractional_part = fractional_graph + delete_space + pynutil.delete(minor)
            unit = integer_part + fractional_part
            units.append(pynutil.insert(f"currency: \"{signature}\" ") + unit)

            # decimal: two point one million dollars, etc.
            unit = decimal_graph + delete_space + pynutil.delete(major)
            units.append(pynutil.insert(f"currency: \"{signature}\" ") + unit)

        final_graph = pynini.union(*units)
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
