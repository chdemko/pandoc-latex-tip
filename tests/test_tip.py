# This Python file uses the following encoding: utf-8
from unittest import TestCase
from pandocfilters import Para, Str, Space, Span, Div, Strong, RawInline, RawBlock, Emph, Header

import pandoc_latex_tip

def test_span():
    do_test(Span(['', ['class1', 'class2'], []], []))

def test_div():
    do_test(Div(['', ['class1', 'class2'], []], []))

def do_test(src):
    meta = {
        'pandoc-latex-tip': {
            't': 'MetaList',
            'c': [
                {
                    't': 'MetaMap',
                    'c': {
                        'classes': {
                            't': 'MetaList',
                            'c': [
                                {
                                    't': 'MetaInlines',
                                    'c': [
                                        {
                                            't': 'Str',
                                            'c': 'class1'
                                        }
                                    ]
                                },
                                {
                                    't': 'MetaInlines',
                                    'c': [
                                        {
                                            't': 'Str',
                                            'c': 'class2'
                                        }
                                    ]
                                }
                            ]
                        },
                    }
                }
            ]
        }
    }


    dest = pandoc_latex_tip.tip(src['t'], src['c'], 'latex', meta)
    assert dest[0]['c'][0] == 'tex'

