# This Python file uses the following encoding: utf-8
from unittest import TestCase
from panflute import *

import pandoc_latex_tip

def metadata():
    return {
        'pandoc-latex-tip': MetaList(
            MetaMap(
                classes = MetaList(MetaString('tip'), MetaString('listing')),
                icons = MetaList(MetaMap(name = MetaString('file-text'), color=MetaString('darksalmon'))),
                size = MetaString('36'),
                position = MetaString('right')
            ),
            MetaMap(
                classes = MetaList(MetaString('tip'))
            )
        )
    }

def test_span():
    doc = Doc(Para(Span(classes = ['tip', 'listing']), Span(classes = ['tip'])), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].content[0].format == 'tex'
    assert doc.content[0].content[2].format == 'tex'

def test_div():
    doc = Doc(Div(classes = ['tip', 'listing']), Div(classes = ['tip']), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].format == 'tex'
    assert doc.content[2].format == 'tex'

def test_code():
    doc = Doc(Para(Code('', classes = ['tip', 'listing']), Code('', classes = ['tip'])), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].content[0].format == 'tex'
    assert doc.content[0].content[2].format == 'tex'

def test_codeblock():
    doc = Doc(CodeBlock('', classes = ['tip', 'listing']), CodeBlock('', classes = ['tip']), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].format == 'tex'
    assert doc.content[2].format == 'tex'

