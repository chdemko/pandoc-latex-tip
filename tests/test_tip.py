from unittest import TestCase

from panflute import convert_text

import pandoc_latex_tip


class TipTest(TestCase):
    def verify_conversion(
        self,
        text,
        expected,
        transform,
        input_format="markdown",
        output_format="latex",
        standalone=False,
    ) -> None:
        """
        Verify the conversion.

        Parameters
        ----------
        text
            input text
        expected
            expected text
        transform
            filter function
        input_format
            input format
        output_format
            output format
        standalone
            is the output format standalone ?
        """
        doc = convert_text(text, input_format=input_format, standalone=True)
        doc.format = output_format
        doc = transform(doc)
        converted = convert_text(
            doc.content,
            input_format="panflute",
            output_format=output_format,
            extra_args=["--wrap=none"],
            standalone=standalone,
        )
        self.assertEqual(converted.strip(), expected.strip())

    def test_span(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

[]{.tip .listing}[]{.tip}[]{.warning}[]{.v5.0}
            """,
            """
{}
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddright%%
\\else%%
\\pandoclatextipevenright%%
\\fi%%
\\marginnote{\\href{http://www.google.fr}{\\includegraphics[width=0.5in,height=0.5in]{/home/chdemko/.cache/pandoc_latex_tip/darksalmon/fa-file-text.png}}\\includegraphics[width=0.5in,height=0.5in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%
{}
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-exclamation-circle.png}}[0pt]\\vspace{0cm}%%
{}
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%
{}
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/orange/far-user.png}}[0pt]\\vspace{0cm}%%
            """,
            pandoc_latex_tip.main,
        )

    def test_codeblock(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

~~~{.python .warning}
main()
~~~

            """,
            """
\\begin{minipage}{\\textwidth}
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%

\\begin{Shaded}
\\begin{Highlighting}[]
\\NormalTok{main()}
\\end{Highlighting}
\\end{Shaded}

\\end{minipage}

            """,
            pandoc_latex_tip.main,
        )

    def test_div(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

::: warning
Division
:::
            """,
            """
Division
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%
            """,
            pandoc_latex_tip.main,
        )
        self.verify_conversion(
            """
::: {
  latex-tip-icon=fa-address-book
  latex-tip-size=24
  latex-tip-position=right
  latex-tip-color=lightskyblue} :::
Division
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            """,
            """
Division
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddright%%
\\else%%
\\pandoclatextipevenright%%
\\fi%%
\\marginnote{\\includegraphics[width=0.33333in,height=0.33333in]{/home/chdemko/.cache/pandoc_latex_tip/lightskyblue/fa-address-book.png}}[0pt]\\vspace{0cm}%%
            """,
            pandoc_latex_tip.main,
        )

    def test_div_div(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

::: warning
::: div
Division
:::
:::
            """,
            """
Division
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%
            """,
            pandoc_latex_tip.main,
        )

    def test_div_rule(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

::: warning
-----------
:::
            """,
            """
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%

\\begin{center}\\rule{0.5\\linewidth}{0.5pt}\\end{center}
            """,
            pandoc_latex_tip.main,
        )

    def test_div_lineblock(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

::: warning
| Lineblock
| continue
:::
            """,
            """
Lineblock
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%
\\\\
continue
            """,
            pandoc_latex_tip.main,
        )

    def test_div_codeblock(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

::: warning
~~~python
main()
~~~
:::
            """,
            """
\\begin{minipage}{\\textwidth}
\\checkoddpage%%
\\ifoddpage%%
\\pandoclatextipoddleft%%
\\else%%
\\pandoclatextipevenleft%%
\\fi%%
\\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%

\\begin{Shaded}
\\begin{Highlighting}[]
\\NormalTok{main()}
\\end{Highlighting}
\\end{Shaded}

\\end{minipage}
            """,
            pandoc_latex_tip.main,
        )

    def test_div_bulletlist(self):
        self.verify_conversion(
            """
---
pandoc-latex-tip:
  - classes: [tip, listing]
    icons:
      - {name: fa-file-text, color: darksalmon, link: http://www.google.fr}
      - fa-comments
    size: 36
    position: right

  - classes: [warning]
    icons: fa-comments

  - classes: [tip]
    position: left

  - classes: [v5.0]
    icons:
      - name: far-user
        color: orange
---

::: warning
* a
* b
:::
            """,
            """
\\begin{itemize}
\\tightlist
\\item
  a
  \\checkoddpage%%
  \\ifoddpage%%
  \\pandoclatextipoddleft%%
  \\else%%
  \\pandoclatextipevenleft%%
  \\fi%%
  \\marginnote{\\includegraphics[width=0.25in,height=0.25in]{/home/chdemko/.cache/pandoc_latex_tip/black/fa-comments.png}}[0pt]\\vspace{0cm}%%
\\item
  b
\\end{itemize}
            """,
            pandoc_latex_tip.main,
        )
