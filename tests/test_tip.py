# This Python file uses the following encoding: utf-8
from unittest import TestCase
from panflute import *

import pandoc_latex_tip

def metadata():
    return {
        'pandoc-latex-tip': MetaList(
            MetaMap(
                classes=MetaList(MetaString('class1'), MetaString('class2'))
            )
        )
    }

def test_span():
    doc = Doc(Para(Span(classes = ['class1', 'class2'])), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].content[0].format == 'tex'

def test_div():
    doc = Doc(Div(classes = ['class1', 'class2']), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].format == 'tex'

def test_code():
    doc = Doc(Para(Code('', classes = ['class1', 'class2'])), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].content[0].format == 'tex'

def test_codeblock():
    doc = Doc(CodeBlock('', classes = ['class1', 'class2']), metadata=metadata(), format='latex', api_version=(1, 17, 2))
    pandoc_latex_tip.main(doc)
    assert doc.content[0].format == 'tex'

