from collections import defaultdict

import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, NEMO_DIGIT
from ukr.taggers.cardinal import CardinalFst
from ukr.utils import get_abs_path, load_labels


def prepare_labels_for_insertion(file_path: str) -> dict:
    labels = load_labels(file_path)
    mapping = defaultdict(list)
    for k, v in labels:
        mapping[k].append(v)

    for k in mapping:
        mapping[k] = pynini.union(*mapping[k]).optimize()
    return mapping


class DecimalFst(GraphFst):

    def __init__(self, cardinal: CardinalFst, ):
        super().__init__(name="decimal", kind="classify")

        delimiter = pynini.string_file(get_abs_path("data/numbers/decimal_delimiter.tsv"))

        delimiter = pynini.cross(delimiter, " ") + pynini.closure(delete_space + pynutil.delete("і"), 0, 1)
        delimiter |= pynini.closure(delete_space + pynini.cross("і", " "), 1, 1)

        decimal_endings_map = prepare_labels_for_insertion(get_abs_path("data/numbers/decimal_endings.tsv"))

        tenth_labels = pynutil.delete(decimal_endings_map["10"])
        tenth = cardinal.graph @ NEMO_DIGIT + delete_space + tenth_labels

        hundreds_labels = pynutil.delete(decimal_endings_map["100"])
        hundreds = cardinal.graph @ (NEMO_DIGIT + NEMO_DIGIT) + delete_space + hundreds_labels
        hundreds |= cardinal.graph @ (pynutil.insert("0") + NEMO_DIGIT) + delete_space + hundreds_labels

        thousands_labels = pynutil.delete(decimal_endings_map["1000"])
        thousands = cardinal.graph @ (NEMO_DIGIT + NEMO_DIGIT + NEMO_DIGIT) + delete_space + thousands_labels
        thousands |= cardinal.graph @ (pynutil.insert("0") + NEMO_DIGIT + NEMO_DIGIT) + delete_space + thousands_labels
        thousands |= cardinal.graph @ (pynutil.insert("0") + pynutil.insert("0") + NEMO_DIGIT) + delete_space + thousands_labels

        graph_fractional_part = pynini.union(
            tenth,
            hundreds,
            thousands
        ).optimize()

        graph_integer_part = cardinal.graph

        billion = pynini.string_file(get_abs_path("data/numbers/cardinals_billion.tsv"))
        million = pynini.string_file(get_abs_path("data/numbers/cardinals_million.tsv"))

        quantity = pynutil.insert(" quantity: \"") + (billion | million) + pynutil.insert("\"")
        optional_graph_quantity = pynini.closure(" " + quantity, 0, 1)

        graph_fractional = pynutil.insert("fractional_part: \"") + graph_fractional_part + pynutil.insert("\"")
        graph_integer = pynutil.insert("integer_part: \"") + graph_integer_part + pynutil.insert("\"")

        self.graph = graph_integer + delete_space + delimiter + delete_space + graph_fractional + optional_graph_quantity
        self.graph |= graph_integer + delete_space + quantity
        self.graph |= pynutil.insert("integer_part: \"0\" fractional_part: \"") + (tenth | hundreds) + pynutil.insert("\"")

        optional_minus_graph = pynini.closure(pynutil.insert("negative: \"true\" ") + pynutil.delete("мінус"), 0, 1)

        final_graph = optional_minus_graph + self.graph
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
