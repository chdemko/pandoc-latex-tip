# This Python file uses the following encoding: utf-8
from unittest import TestCase
from pandocfilters import Para, Str, Space, Span, Strong, RawInline, Emph, Header

import pandoc_latex_tip

def test_tip():

    src = Span(['', ['class1', 'class2'], []], [])
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
    assert isinstance(dest, list)
    assert len(dest) == 2
    assert dest[1]['t'] == 'RawInline'

