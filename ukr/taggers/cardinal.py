import pynini
from pynini.lib import pynutil

from ukr.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
)

from ukr.utils import get_abs_path


def get_zeros():
    graph_zeros = pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/nominative/cardinals_zero.tsv")))
    graph_zeros |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/genitive/cardinals_zero.tsv")))
    graph_zeros |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/dative/cardinals_zero.tsv")))
    graph_zeros |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/accusative/cardinals_zero.tsv")))
    graph_zeros |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/instrumental/cardinals_zero.tsv")))
    graph_zeros |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/prepositional/cardinals_zero.tsv")))

    return graph_zeros.optimize()


def get_digits():
    graph_digit = pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/nominative/cardinals_digit.tsv")))
    graph_digit |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/genitive/cardinals_digit.tsv")))
    graph_digit |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/dative/cardinals_digit.tsv")))
    graph_digit |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/accusative/cardinals_digit.tsv")))
    graph_digit |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/instrumental/cardinals_digit.tsv")))
    graph_digit |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/prepositional/cardinals_digit.tsv")))

    return graph_digit.optimize()


def get_teen():
    graph_teen = pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/nominative/cardinals_teen.tsv")))
    graph_teen |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/genitive/cardinals_teen.tsv")))
    graph_teen |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/dative/cardinals_teen.tsv")))
    graph_teen |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/accusative/cardinals_teen.tsv")))
    graph_teen |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/instrumental/cardinals_teen.tsv")))
    graph_teen |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/prepositional/cardinals_teen.tsv")))

    return graph_teen.optimize()


def get_ties():
    graph_ties = pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/nominative/cardinals_ties.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/genitive/cardinals_ties.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/dative/cardinals_ties.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/accusative/cardinals_ties.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/instrumental/cardinals_ties.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/prepositional/cardinals_ties.tsv")))

    return graph_ties.optimize()


def get_hundred():
    graph_ties = pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/nominative/cardinals_hundred.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/genitive/cardinals_hundred.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/dative/cardinals_hundred.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/accusative/cardinals_hundred.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/instrumental/cardinals_hundred.tsv")))
    graph_ties |= pynini.invert(pynini.string_file(get_abs_path("data/numbers/cardinal/prepositional/cardinals_hundred.tsv")))

    return graph_ties.optimize()


class CardinalFst(GraphFst):

    def __init__(self):
        super().__init__(name="cardinal", kind="classify")

        delete_space = pynutil.delete(" ")
        delete_space_optional = pynini.closure(delete_space, 0, 1)

        self.graph_zero = get_zeros()
        self.graph_digit = get_digits()
        self.graph_teen = get_teen()
        self.graph_ties = get_ties()
        self.graph_hundred = get_hundred()

        # From 1 to 99
        graph_up_to_hundred_component = pynini.union(
            self.graph_teen,
            (self.graph_ties | pynutil.insert("0")) + delete_space_optional + (self.graph_digit | pynutil.insert("0"))
        )

        graph_hundred_component = self.graph_hundred + delete_space_optional + graph_up_to_hundred_component
        graph_hundred_component |= pynutil.insert("0") + graph_up_to_hundred_component

        thousands = pynini.string_file(get_abs_path("data/numbers/cardinals_thousand.tsv"))

        one_thousand = pynini.cross(thousands, '1') + delete_space + graph_hundred_component
        graph_thousands = (
            pynini.union(
                graph_hundred_component + delete_space + pynutil.delete(thousands),
                pynutil.insert("000", weight=0.1),
            )
        )

        millions = pynini.string_file(get_abs_path("data/numbers/cardinals_million.tsv"))
        graph_millions = (
            pynini.union(
                graph_hundred_component + delete_space + pynutil.delete(millions),
                pynutil.insert("000", weight=0.1),
            )
        )

        billions = pynini.string_file(get_abs_path("data/numbers/cardinals_billion.tsv"))
        graph_billions = (
            pynini.union(
                graph_hundred_component + delete_space + pynutil.delete(billions),
                pynutil.insert("000", weight=0.1),
            )
        )

        graph = pynini.union(
            graph_billions
            + delete_space_optional
            + graph_millions
            + delete_space_optional
            + graph_thousands
            + delete_space_optional
            + (graph_hundred_component | pynutil.insert("000")),
            one_thousand,
            graph_up_to_hundred_component,
            self.graph_zero,
        )

        self.graph_zeroth = graph
        graph = graph @ pynini.union(
            pynini.closure(pynutil.delete(pynini.union("0", ",")))
            + pynini.difference(NEMO_DIGIT, "0")
            + pynini.closure(pynini.union(NEMO_DIGIT, ",")),
            "0",
        )

        self.graph_hundred_component = graph_hundred_component

        self.graph_up_to_hundred_component = graph_up_to_hundred_component
        self.graph = graph

        optional_minus_graph = pynini.closure(pynutil.insert("negative: \"true\" ") + pynutil.delete("мінус"), 0, 1)

        final_graph = optional_minus_graph + pynutil.insert("integer: \"") + self.graph + pynutil.insert("\"")
        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
