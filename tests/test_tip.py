# This Python file uses the following encoding: utf-8

from unittest import TestCase

from panflute import (
    MetaList,
    MetaMap,
    MetaString,
    Doc,
    Para,
    Span,
    Div,
    Code,
    CodeBlock,
)

import pandoc_latex_tip


class TipTest(TestCase):
    @classmethod
    def metadata(cls):
        return {
            "pandoc-latex-tip": MetaList(
                MetaMap(
                    classes=MetaList(MetaString("tip"), MetaString("listing")),
                    icons=MetaList(
                        MetaMap(
                            name=MetaString("file-text"),
                            color=MetaString("darksalmon"),
                            link=MetaString("http://www.google.fr"),
                        ),
                        MetaString("comments"),
                    ),
                    size=MetaString("36"),
                    position=MetaString("right"),
                ),
                MetaMap(
                    classes=MetaList(MetaString("warning")),
                    icons=MetaString("comments"),
                ),
                MetaMap(
                    classes=MetaList(MetaString("tip")), position=MetaString("left")
                ),
                MetaMap(
                    classes=MetaList(MetaString("v5.0")),
                    icons=MetaList(
                        MetaMap(
                            name=MetaString("balance-scale"),
                            version=MetaString("5.x"),
                            variant=MetaString("solid"),
                            color=MetaString("orange"),
                        )
                    ),
                ),
            )
        }

    def test_span(self):
        doc = Doc(
            Para(
                Span(classes=["tip", "listing"]),
                Span(classes=["tip"]),
                Span(classes=["warning"]),
                Span(classes=["v5.0"]),
                Span(
                    attributes={
                        "latex-tip-icon": "warning",
                        "latex-tip-position": "right",
                        "latex-tip-size": 24,
                    }
                ),
            ),
            metadata=self.metadata(),
            format="latex",
            api_version=(1, 17, 2),
        )
        pandoc_latex_tip.main(doc)
        self.assertEqual(doc.content[0].content[1].format, "tex")
        self.assertEqual(doc.content[0].content[3].format, "tex")
        self.assertEqual(doc.content[0].content[5].format, "tex")
        self.assertEqual(doc.content[0].content[7].format, "tex")
        self.assertEqual(doc.content[0].content[9].format, "tex")

    def test_div(self):
        doc = Doc(
            Div(classes=["tip", "listing"]),
            Div(classes=["tip"]),
            Div(classes=["warning"]),
            Div(
                attributes={
                    "latex-tip-icon": "warning",
                    "latex-tip-position": "right",
                    "latex-tip-size": 24,
                }
            ),
            metadata=self.metadata(),
            format="latex",
            api_version=(1, 17, 2),
        )
        pandoc_latex_tip.main(doc)
        self.assertEqual(doc.content[0].format, "tex")
        self.assertEqual(doc.content[1].format, "tex")
        self.assertEqual(doc.content[3].format, "tex")
        self.assertEqual(doc.content[4].format, "tex")
        self.assertEqual(doc.content[6].format, "tex")
        self.assertEqual(doc.content[7].format, "tex")
        self.assertEqual(doc.content[9].format, "tex")
        self.assertEqual(doc.content[10].format, "tex")

    def test_code(self):
        doc = Doc(
            Para(
                Code("", classes=["tip", "listing"]),
                Code("", classes=["tip"]),
                Code("", classes=["warning"]),
                Code(
                    "",
                    attributes={
                        "latex-tip-icon": "warning",
                        "latex-tip-position": "right",
                        "latex-tip-size": 24,
                    },
                ),
            ),
            metadata=self.metadata(),
            format="latex",
            api_version=(1, 17, 2),
        )
        pandoc_latex_tip.main(doc)
        self.assertEqual(doc.content[0].content[1].format, "tex")
        self.assertEqual(doc.content[0].content[3].format, "tex")
        self.assertEqual(doc.content[0].content[5].format, "tex")
        self.assertEqual(doc.content[0].content[7].format, "tex")

    def test_codeblock(self):
        doc = Doc(
            CodeBlock("", classes=["tip", "listing"]),
            CodeBlock("", classes=["tip"]),
            CodeBlock("", classes=["warning"]),
            CodeBlock(
                "",
                attributes={
                    "latex-tip-icon": "warning",
                    "latex-tip-position": "right",
                    "latex-tip-size": 24,
                },
            ),
            metadata=self.metadata(),
            format="latex",
            api_version=(1, 17, 2),
        )
        pandoc_latex_tip.main(doc)
        self.assertEqual(doc.content[0].format, "tex")
        self.assertEqual(doc.content[2].format, "tex")
        self.assertEqual(doc.content[5].format, "tex")
        self.assertEqual(doc.content[8].format, "tex")
