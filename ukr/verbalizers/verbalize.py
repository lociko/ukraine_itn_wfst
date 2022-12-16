from ukr.graph_utils import GraphFst
from ukr.verbalizers.cardinal import CardinalFst
from ukr.verbalizers.decimal import DecimalFst
from ukr.verbalizers.measure import MeasureFst
from ukr.verbalizers.money import MoneyFst
from ukr.verbalizers.ordinal import OrdinalFst
from pynini.lib import pynutil

from ukr.verbalizers.word import WordFst


class VerbalizeFst(GraphFst):

    def __init__(self):
        super().__init__(name="verbalize", kind="verbalize")

        self.cardinal = CardinalFst()
        self.decimal = DecimalFst()
        self.ordinal = OrdinalFst()
        self.measure = MeasureFst(decimal=self.decimal, cardinal=self.cardinal)
        self.money = MoneyFst(decimal=self.decimal)
        self.word = WordFst()

        graph = (
                self.money.fst
                | self.measure.fst
                | self.ordinal.fst
                | self.decimal.fst
                | self.cardinal.fst
        )
        graph |= pynutil.add_weight(self.word.fst, 100)

        self.fst = graph

    def as_json(self):
        graph = (
                self.money.as_json()
                | self.measure.as_json()
                | self.ordinal.as_json()
                | self.decimal.as_json()
                | self.cardinal.as_json()
        )

        graph |= pynutil.add_weight(self.word.as_json(), 100)

        return graph
