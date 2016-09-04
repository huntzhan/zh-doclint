# -*- coding: utf-8 -*-
from __future__ import (
    division, absolute_import, print_function, unicode_literals,
)
from builtins import *                  # noqa
from future.builtins.disabled import *  # noqa

import re


ERRORS = {
    # space.
    'E101': '英文与非标点的中文之间需要有一个空格',
    'E102': '数字与非标点的中文之间需要有一个空格，'
            '除了「％」、「°C」、以及倍数单位（如 2x、3n）之外，'
            '其余数字与单位之间需要加空格',
    'E103': '书写时括号中全为数字，则括号用半角括号且首括号前要空一格',

    # punctuation.
    'E201': '只有中文或中英文混排中，一律使用中文全角标点',
    'E202': '如果出现整句英文，则在这句英文中使用英文、半角标点',
    'E203': '中文标点与其他字符间一律不加空格',
    'E204': '中文文案中使用中文引号「」和『』，其中「」为外层引号',
    'E205': '省略号请使用「……」标准用法',
    'E206': '感叹号请使用「！」标准用法',
    'E207': '请勿在文章内使用「~」',

    # terminology.
    'E301': '常用名词错误',
}


def error_code(code):
    ERROR_TEMPLATE = (
        'Line {1}-{2},\n'
        '{0}: {3},\n'
        'Detected: {4}\n'
    )

    def decorator(func):
        def wrapper(text_element):

            detected = func(text_element)
            if detected:
                log = ERROR_TEMPLATE.format(
                    code,
                    text_element.loc_begin, text_element.loc_end,
                    ERRORS[code],
                    detected,
                )
                print(log)
                return False
            return True

        return wrapper
    return decorator


def check_on_patterns(patterns, content):
    for pattern in patterns:
        m = re.search(pattern, content, re.UNICODE)
        if m:
            return m.group()
    return False


@error_code('E101')
def check_e101(text_element):
    # 1. no space.
    # prefix check.
    p11 = r'[\u4e00-\u9fff][a-zA-z]'
    # suffix check.
    p12 = r'[a-zA-z][\u4e00-\u9fff]'

    # 2. more than one whitespaces.
    # prefix check.
    p21 = r'[\u4e00-\u9fff]\s{2,}[a-zA-z]'
    # suffix check.
    p22 = r'[a-zA-z]\s{2,}[\u4e00-\u9fff]'

    # 3. wrong single whitespace: [\t\r\f\v]
    # only allow ' ' and '\n'.
    # prefix check.
    p31 = r'[\u4e00-\u9fff](?=[^ \n])\s{1}[a-zA-z]'
    # suffix check.
    p32 = r'[a-zA-z](?=[^ \n])\s{1}[\u4e00-\u9fff]'

    return check_on_patterns(
        [p11, p12, p21, p22, p31, p32],
        text_element.content,
    )


def check_error(text_element):

    BLOCK_LEVEL_CHECKING = [
        'E101',
        'E102',
        'E103',
        'E203',
        'E205',
        'E206',
        'E207',
        'E301',
    ]
    for error_code in BLOCK_LEVEL_CHECKING:
        checker = globals['check_{0}'.format(error_code.lower())]
        checker(text_element)
