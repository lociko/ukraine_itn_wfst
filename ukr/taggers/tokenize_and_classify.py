import pynini
from pynini.lib import pynutil

from ukr.graph_utils import delete_space, GraphFst, delete_extra_space
from ukr.taggers.cardinal import CardinalFst
from ukr.taggers.decimal import DecimalFst
from ukr.taggers.measure import MeasureFst
from ukr.taggers.money import MoneyFst
from ukr.taggers.ordinal import OrdinalFst
from ukr.taggers.word import WordFst


class ClassifyFst(GraphFst):

    def __init__(self):
        super().__init__(name="tokenize_and_classify", kind="classify")

        cardinal = CardinalFst()
        cardinal_graph = cardinal.fst

        ordinal = OrdinalFst(cardinal)
        ordinal_graph = ordinal.fst

        decimal = DecimalFst(cardinal)
        decimal_graph = decimal.fst

        measure_graph = MeasureFst(cardinal=cardinal, decimal=decimal).fst
        word_graph = WordFst().fst
        money_graph = MoneyFst(cardinal=cardinal, decimal=decimal).fst

        classify = (
                pynutil.add_weight(decimal_graph, 1.1)
                | pynutil.add_weight(measure_graph, 1.1)
                | pynutil.add_weight(cardinal_graph, 1.1)
                | pynutil.add_weight(ordinal_graph, 1.1)
                | pynutil.add_weight(money_graph, 1.1)
                | pynutil.add_weight(word_graph, 100)
        )

        token = pynutil.insert("tokens { ") + classify + pynutil.insert(" }")

        graph = token + pynini.closure(delete_extra_space + token)
        graph = delete_space + graph + delete_space

        self.fst = graph.optimize()
