# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

from operator import attrgetter

from zh_doclint.preprocessor import TextElement
from zh_doclint.error_detection import (
    detect_e101,
    detect_e102,
    detect_e103,
    detect_e104,
    detect_e203,
    detect_e205,
    detect_e206,
    detect_e207,
    detect_e301,
    detect_block_level_error,

    split_text_element,
    detect_e201,
    detect_e202,
    detect_e204,
)


def test_e101():

    te = TextElement(
        '', '1', '2',
        '中文english',
    )
    assert not detect_e101(te)

    te = TextElement(
        '', '1', '2',
        'english中文',
    )
    assert not detect_e101(te)

    te = TextElement(
        '', '1', '2',
        '中文  english',
    )
    assert not detect_e101(te)

    te = TextElement(
        '', '1', '2',
        'english  中文',
    )
    assert not detect_e101(te)

    te = TextElement(
        '', '1', '2',
        '中文\tenglish',
    )
    assert not detect_e101(te)

    te = TextElement(
        '', '1', '2',
        '中文 english',
    )
    assert detect_e101(te)

    te = TextElement(
        '', '1', '2',
        'english 中文',
    )
    assert detect_e101(te)

    te = TextElement(
        '', '1', '2',
        '中文\nenglish',
    )
    assert detect_e101(te)

    te = TextElement(
        '', '1', '2',
        '42\n中文',
    )
    assert detect_e102(te)


def test_e102():

    te = TextElement(
        '', '1', '2',
        '中文1',
    )
    assert not detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '42中文',
    )
    assert not detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '中文  42',
    )
    assert not detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '42  中文',
    )
    assert not detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '中文\t42',
    )
    assert not detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '中文 42',
    )
    assert detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '42 中文',
    )
    assert detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '中文\n42',
    )
    assert detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '中文 \n42',
    )
    assert detect_e102(te)

    te = TextElement(
        '', '1', '2',
        '42\n中文',
    )
    assert detect_e102(te)


def test_e103():

    # te = TextElement(
    #     '', '1', '2',
    #     'μ42',
    # )
    # assert not detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42μ',
    )
    assert not detect_e103(te)

    # te = TextElement(
    #     '', '1', '2',
    #     'μ  42',
    # )
    # assert not detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42  μ',
    )
    assert not detect_e103(te)

    # te = TextElement(
    #     '', '1', '2',
    #     'μ\t42',
    # )
    # assert not detect_e103(te)

    # te = TextElement(
    #     '', '1', '2',
    #     'μ 42',
    # )
    # assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42 μ',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        'μ\n42',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42\nμ',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42x',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42n',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42％',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42%',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42℃',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '，42',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '42。',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        'Q3',
    )
    assert detect_e103(te)

    te = TextElement(
        '', '1', '2',
        '136-4321-1234',
    )
    assert detect_e103(te)


def test_e104():

    te = TextElement(
        '', '1', '2',
        '(42）',
    )
    assert not detect_e104(te)

    te = TextElement(
        '', '1', '2',
        '（42)',
    )
    assert not detect_e104(te)

    te = TextElement(
        '', '1', '2',
        '（42）',
    )
    assert not detect_e104(te)

    te = TextElement(
        '', '1', '2',
        '42(42)',
    )
    assert not detect_e104(te)

    te = TextElement(
        '', '1', '2',
        '42  (42)',
    )
    assert not detect_e104(te)

    te = TextElement(
        '', '1', '2',
        '42 (42)',
    )
    assert detect_e104(te)

    te = TextElement(
        '', '1', '2',
        '42\n(42)',
    )
    assert detect_e104(te)


def test_e203():

    te = TextElement(
        '', '1', '2',
        '中文， 测试',
    )
    assert not detect_e203(te)

    te = TextElement(
        '', '1', '2',
        '中文 。测试',
    )
    assert not detect_e203(te)

    te = TextElement(
        '', '1', '2',
        '「 中文」',
    )
    assert not detect_e203(te)

    te = TextElement(
        '', '1', '2',
        '中文，测试',
    )
    assert detect_e203(te)

    te = TextElement(
        '', '1', '2',
        '中文；测试',
    )
    assert detect_e203(te)

    te = TextElement(
        '', '1', '2',
        '「中文」',
    )
    assert detect_e203(te)

    te = TextElement(
        '', '1', '2',
        '中文！\n测试',
    )
    assert detect_e203(te)


def test_e205():

    te = TextElement(
        '', '1', '2',
        '中文...',
    )
    assert not detect_e205(te)

    te = TextElement(
        '', '1', '2',
        '中文.......',
    )
    assert not detect_e205(te)

    te = TextElement(
        '', '1', '2',
        '中文。。。',
    )
    assert not detect_e205(te)

    te = TextElement(
        '', '1', '2',
        '中文......',
    )
    assert detect_e205(te)


def test_e206():

    te = TextElement(
        '', '1', '2',
        '中文!!',
    )
    assert not detect_e206(te)

    te = TextElement(
        '', '1', '2',
        '中文！！',
    )
    assert not detect_e206(te)

    te = TextElement(
        '', '1', '2',
        '中文!',
    )
    assert detect_e206(te)

    te = TextElement(
        '', '1', '2',
        '中文！',
    )
    assert detect_e206(te)

    te = TextElement(
        '', '1', '2',
        'english, with space',
    )
    assert detect_e203(te)


def test_e207():

    te = TextElement(
        '', '1', '2',
        '中文~',
    )
    assert not detect_e207(te)

    te = TextElement(
        '', '1', '2',
        '中文',
    )
    assert detect_e207(te)


def test_e301():

    WRONG_WORDS = [
        'APP',
        'app',
        'android',
        'ios',
        'IOS',
        'IPHONE',
        'iphone',
        'AppStore',
        'app store',
        'wifi',
        'Wifi',
        'Wi-fi',
        'E-mail',
        'Email',
        'PS',
        'ps',
        'Ps.',

        '我app store我',
    ]

    for word in WRONG_WORDS:
        te = TextElement(
            '', '1', '2',
            word,
        )
        assert not detect_e301(te)


def test_block_level_error():

    te = TextElement(
        '', '1', '2',
        '好的句子，好的句子',
    )
    assert detect_block_level_error(te)

    te = TextElement(
        '', '1', '2',
        'app好的句子， 好的句子',
    )
    assert not detect_block_level_error(te)


def test_split_text_element():

    def help_(key, te):
        return list(map(attrgetter(key), split_text_element(te)))

    content = '''a
b.
c. inline!
d
e.'''

    te = TextElement(
        'paragraph', '1', '5',
        content,
    )
    lines = help_('content', te)
    begins = help_('loc_begin', te)
    ends = help_('loc_end', te)

    assert ['a\nb.\n', 'c.', ' inline!\n', 'd\ne.'] == lines
    assert ['1', '3', '3', '4'] == begins
    assert ['2', '3', '3', '5'] == ends

    content = '''a......
b!
c;
d.
e?
f！
g；
h。
i？'''

    te = TextElement(
        'paragraph', '1', '9',
        content,
    )
    lines = help_('content', te)
    assert len(lines) == 9


def test_e201():

    te = TextElement(
        '', '1', '2',
        '有中文, 错误.',
    )
    assert not detect_e201(te)

    te = TextElement(
        '', '1', '2',
        '有中文，正确。',
    )
    assert detect_e201(te)

    te = TextElement(
        '', '1', '2',
        '有中文，正确......',
    )
    assert detect_e201(te)

    te = TextElement(
        '', '1', '2',
        'pure english, nothing wrong.',
    )
    assert detect_e201(te)


def test_e202():

    te = TextElement(
        '', '1', '2',
        'pure english，nothing wrong.',
    )
    assert not detect_e202(te)

    te = TextElement(
        '', '1', '2',
        'pure english, nothing wrong.',
    )
    assert detect_e202(te)


def test_e204():

    te = TextElement(
        '', '1', '2',
        "中文'测试'",
    )
    assert not detect_e204(te)

    te = TextElement(
        '', '1', '2',
        '中文"测试"',
    )
    assert not detect_e204(te)

    te = TextElement(
        '', '1', '2',
        '中文‘测试’',
    )
    assert not detect_e204(te)

    te = TextElement(
        '', '1', '2',
        '中文“测试”',
    )
    assert not detect_e204(te)

    te = TextElement(
        '', '1', '2',
        "中文「测试」",
    )
    assert detect_e204(te)