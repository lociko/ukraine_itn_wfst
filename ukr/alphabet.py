# Copyright (c) 2021, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adapted from https://github.com/google/TextNormalizationCoveringGrammars
# Russian minimally supervised number grammar.

from nemo_text_processing.text_normalization.en.graph_utils import NEMO_NON_BREAKING_SPACE, NEMO_SPACE
from nemo_text_processing.text_normalization.ukr.utils import get_abs_path

try:
    import pynini

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False

try:
    UKR_LOWER_ALPHA = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"
    UKR_UPPER_ALPHA = UKR_LOWER_ALPHA.upper()
    UKR_LOWER_ALPHA = pynini.union(*UKR_LOWER_ALPHA).optimize()
    UKR_UPPER_ALPHA = pynini.union(*UKR_UPPER_ALPHA).optimize()
    UKR_ALPHA = (UKR_LOWER_ALPHA | UKR_UPPER_ALPHA).optimize()

    UKR_STRESSED_MAP = [
        ("А́", "А'"),
        ("Е́", "Е'"),
        ("И́", "И'"),
        ("О́", "О'"),
        ("У́", "У'"),
        ("Є́", "Є'"),
        ("Ю́", "Ю'"),
        ("Я́", "Я'"),
        ("а́", "а'"),
        ("е́", "е'"),
        ("и́", "и'"),
        ("о́", "о'"),
        ("у́", "у'"),
        ("є́", "є'"),
        ("ю́", "ю'"),
        ("я́", "я'"),
    ]

    REWRITE_STRESSED = pynini.closure(pynini.string_map(UKR_STRESSED_MAP).optimize() | UKR_ALPHA).optimize()
    TO_CYRILLIC = pynini.string_file(get_abs_path("data/latin_to_cyrillic.tsv")).optimize()
    TO_LATIN = pynini.invert(TO_CYRILLIC).optimize()
    UKR_ALPHA_OR_SPACE = pynini.union(UKR_ALPHA, NEMO_SPACE, NEMO_NON_BREAKING_SPACE).optimize()

except (ModuleNotFoundError, ImportError):
    # Create placeholders
    UKR_ALPHA = None
    LO_LATIN = None
