from typing import List, Tuple

import _mecab
from collections import namedtuple


Feature = namedtuple(
    "Feature",
    [
        "pos",
        "semantic",
        "has_jongseong",
        "reading",
        "type",
        "start_pos",
        "end_pos",
        "expression",
    ],
)


def _create_lattice(sentence):
    lattice = _mecab.Lattice()
    lattice.add_request_type(_mecab.MECAB_ALLOCATE_SENTENCE)  # Required
    lattice.set_sentence(sentence)

    return lattice


def _extract_feature(node):
    # Reference:
    # - http://taku910.github.io/mecab/learn.html
    # - https://docs.google.com/spreadsheets/d/1-9blXKjtjeKZqsf4NzHeYJCrr49-nXeRF6D80udfcwY
    # - https://bitbucket.org/eunjeon/mecab-ko-dic/src/master/utils/dictionary/lexicon.py

    # feature = <pos>,<semantic>,<has_jongseong>,<reading>,<type>,<start_pos>,<end_pos>,<expression>
    values = node.feature.split(",")
    assert len(values) == 8

    values = [value if value != "*" else None for value in values]
    feature = dict(zip(Feature._fields, values))
    feature["has_jongseong"] = {"T": True, "F": False}.get(feature["has_jongseong"])

    return Feature(**feature)


def _preserve_space(text, tokens, spaces):
    results = list()
    len_text = len(text)
    text_ptr = 0
    token_ptr = 0

    while text_ptr < len_text:
        character = text[text_ptr]
        if character in spaces:
            results.append(
                (
                    character,
                    Feature(
                        pos="SP",
                        semantic=None,
                        has_jongseong=None,
                        reading=None,
                        type=None,
                        start_pos=None,
                        end_pos=None,
                        expression=None,
                    ),
                )
            )
            text_ptr += 1
        else:
            token = tokens[token_ptr]
            results.append(token)
            text_ptr += len(token[0])
            token_ptr += 1
    return results


class MeCabError(Exception):
    pass


class MeCab:  # APIs are inspried by KoNLPy
    def __init__(self, dicpath=""):
        argument = ""

        if dicpath != "":
            argument = "-d %s" % dicpath

        self.tagger = _mecab.Tagger(argument)

    def parse(self, sentence, drop_space=True):
        lattice = _create_lattice(sentence)
        if not self.tagger.parse(lattice):
            raise MeCabError(self.tagger.what())

        output = [(node.surface, _extract_feature(node)) for node in lattice]

        if drop_space is False:
            output = _preserve_space(sentence, output, spaces=" \n\r\t\v")

        return output

    def pos(self, sentence, drop_space=True):
        return [
            (surface, feature.pos)
            for surface, feature in self.parse(sentence, drop_space=drop_space)
        ]

    def morphs(self, sentence, drop_space=True):
        return [surface for surface, _ in self.parse(sentence, drop_space=drop_space)]

    def nouns(self, sentence, drop_space=True):
        return [
            surface
            for surface, feature in self.parse(sentence, drop_space=drop_space)
            if feature.pos.startswith("N")
        ]
