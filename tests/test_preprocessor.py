# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import os.path

from mistune import preprocessing

from zhlint.preprocessor import transform


DATA = os.path.join(
    os.path.dirname(__file__),
    'data',
)


def load_test_md(name):
    return preprocessing(
        open(os.path.join(DATA, name), encoding='utf-8').read(),
    )


def eof(element):
    assert 'EOF\n' == element.content


def test_latex_inline():
    elements = transform(load_test_md('latex_inline.md'))
    for e in elements:
        print(repr(e.content))
    assert 'a line with $$ words.\n' == elements[0].content
    assert 'a line with \\(\\) words.\n' == elements[1].content
    assert '会使 $$ 加入到 $$ 中\n' == elements[2].content
    eof(elements[3])


def test_latex_block():
    elements = transform(load_test_md('latex_block.md'))
    assert 'block 1\n' == elements[0].content
    assert 'block 2\n' == elements[1].content
    eof(elements[2])


def test_yaml_header():
    elements = transform(load_test_md('yaml_header.md'))
    assert 'test line.\n' == elements[0].content
    eof(elements[1])


def assert_loc(begin, end, element):
    assert begin == int(element.loc_begin)
    assert end == int(element.loc_end)


def test_loc():
    elements = transform(load_test_md('loc.md'))

    assert_loc(5, 5, elements[0])
    assert_loc(9, 11, elements[1])
    assert_loc(16, 16, elements[2])
    eof(elements[3])


def test_ref_loc():
    elements = transform(load_test_md('ref.md'))

    assert 5 == len(elements)
    assert_loc(2, 2, elements[0])
    assert_loc(4, 4, elements[1])
    assert_loc(7, 7, elements[2])
    assert_loc(9, 11, elements[3])
    eof(elements[4])


def test_list_block():
    elements = transform(load_test_md('list_block.md'))

    assert 3 == len(elements)
    assert_loc(2, 6, elements[0])
    assert_loc(8, 8, elements[1])

    eof(elements[2])


def test_table():
    elements = transform(load_test_md('table.md'))
    assert 1 == len(elements)
    eof(elements[0])


def test_link():
    elements = transform(load_test_md('link.md'))
    assert 3 == len(elements)
    assert_loc(3, 10, elements[0])
    assert_loc(12, 12, elements[1])
    eof(elements[2])

    lines = elements[0].content.split('\n')
    expected = [
        '',
        'this',
        'is',
        'a',
        'long',
        'link',
        'a',
        'this is test',
        '',
    ]
    assert expected == lines


def test_link_ending():
    elements = transform(load_test_md('link_ending.md'))
    assert 2 == len(elements)
    eof(elements[1])


def test_newline():
    elements = transform(load_test_md('newline.md'))
    assert 2 == len(elements)
    assert_loc(1, 5, elements[0])
    eof(elements[1])
