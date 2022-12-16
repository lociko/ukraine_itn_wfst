import pynini
from pynini.lib import pynutil

from ukr.graph_utils import GraphFst, delete_space, delete_extra_space
from ukr.verbalizers.verbalize import VerbalizeFst
from ukr.verbalizers.word import WordFst


class VerbalizeFinalFst(GraphFst):
    """
    Finite state transducer that verbalizes an entire sentence, e.g. 
    tokens { name: "its" } tokens { time { hours: "12" minutes: "30" } } tokens { name: "now" } -> its 12:30 now
    """

    def __init__(self):
        super().__init__(name="verbalize_final", kind="verbalize")

        self.verbalize = VerbalizeFst()

        graph = (
                pynutil.delete("tokens")
                + delete_space
                + pynutil.delete("{")
                + delete_space
                + self.verbalize.fst
                + delete_space
                + pynutil.delete("}")
        )
        graph = delete_space + pynini.closure(graph + delete_extra_space) + graph + delete_space

        self.fst = graph

    def as_json(self):
        types = self.verbalize.as_json()
        graph = (
                pynutil.delete("tokens")
                + delete_space
                + pynutil.delete("{")
                + delete_space
                + types
                + delete_space
                + pynutil.delete("}")
        )

        graph = delete_space + pynini.closure(graph + pynutil.insert(",") + delete_extra_space) + graph + delete_space
        graph = pynutil.insert(pynini.escape("[")) + graph + pynutil.insert(pynini.escape("]"))
        return graph
