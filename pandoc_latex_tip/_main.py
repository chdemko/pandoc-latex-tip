#!/usr/bin/env python

"""
Pandoc filter for adding tip in LaTeX.
"""
from __future__ import annotations

import operator
import os
import pathlib
import re
import sys
import tempfile
from typing import Any

import PIL.Image
import PIL.ImageColor
import PIL.ImageDraw
import PIL.ImageFont

from cleo.application import Application
from cleo.commands.command import Command

import fontTools.ttLib

from panflute import (
    BulletList,
    Code,
    CodeBlock,
    DefinitionList,
    Div,
    Doc,
    Element,
    Figure,
    HorizontalRule,
    Image,
    LineBlock,
    Link,
    MetaInlines,
    MetaList,
    OrderedList,
    Para,
    Plain,
    RawBlock,
    RawInline,
    Span,
    convert_text,
    debug,
    run_filter,
)

import platformdirs

import tinycss2

import yaml


class IconFont:
    """
    Base class that represents web icon font.

    This class has been gratly inspired by the code found
    in https://github.com/Pythonity/icon-font-to-png

    Arguments
    ---------
    css_file
        path to icon font CSS file
    ttf_file
        path to icon font TTF file
    prefix
        new prefix if any
    """

    def __init__(
        self,
        css_file: pathlib.Path,
        ttf_file: pathlib.Path,
        prefix: str | None = None,
    ) -> None:
        self.css_file = css_file
        self.ttf_file = ttf_file
        self.css_icons = self.load_css(prefix)

    def load_css(self, prefix: str | None) -> dict[str, str]:
        """
        Create a dict of all icons available in CSS file.

        Arguments
        ---------
        prefix
            new prefix if any

        Returns
        -------
        dict[str, str]
            sorted icons dict
        """
        # pylint: disable=too-many-locals
        icons = {}
        common = None
        with self.css_file.open() as stream:
            rules = tinycss2.parse_stylesheet(stream.read())
        font = fontTools.ttLib.TTFont(self.ttf_file)
        prelude_regex = re.compile("\\.([^:]*):?:before,?")
        content_regex = re.compile("\\s*content:\\s*([^;]+);")

        # pylint: disable=too-many-nested-blocks
        for rule in rules:
            if rule.type == "qualified-rule":
                prelude = tinycss2.serialize(rule.prelude)
                content = tinycss2.serialize(rule.content)
                prelude_result = prelude_regex.match(prelude)
                content_result = content_regex.match(content)
                if prelude_result and content_result:
                    name = prelude_result.group(1)
                    character = content_result.group(1)[1:-1]
                    for cmap in font["cmap"].tables:
                        if cmap.isUnicode() and ord(character) in cmap.cmap:
                            if common is None:
                                common = name
                            else:
                                common = os.path.commonprefix((common, name))
                            icons[name] = character
                            break

        common = common or ""

        # Remove common prefix
        if prefix:
            icons = {
                prefix + name[len(common) :]: value for name, value in icons.items()
            }

        return dict(sorted(icons.items(), key=operator.itemgetter(0)))

    # pylint: disable=too-many-arguments,too-many-locals
    def export_icon(
        self,
        icon: str,
        size: int,
        color: str = "black",
        scale: float | str = "auto",
        filename: str | None = None,
        export_dir: str = "exported",
    ) -> None:
        """
        Export given icon with provided parameters.

        If the desired icon size is less than 150x150 pixels, we will first
        create a 150x150 pixels image and then scale it down, so that
        it's much less likely that the edges of the icon end up cropped.

        Parameters
        ----------
        icon
            valid icon name
        size
            icon size in pixels
        color
            color name or hex value
        scale
            scaling factor between 0 and 1, or 'auto' for automatic scaling
        filename
            name of the output file
        export_dir
            path to export directory
        """
        org_size = size
        size = max(150, size)

        image = PIL.Image.new("RGBA", (size, size), color=(0, 0, 0, 0))
        draw = PIL.ImageDraw.Draw(image)

        if scale == "auto":
            scale_factor = 1.0
        else:
            scale_factor = float(scale)

        font_size = int(size * scale_factor)
        font = PIL.ImageFont.truetype(self.ttf_file, font_size)
        width = draw.textlength(self.css_icons[icon], font=font)
        height = font_size  # always, as long as single-line of text

        # If auto-scaling is enabled, we need to make sure the resulting
        # graphic fits inside the boundary. The values are rounded and may be
        # off by a pixel or two, so we may need to do a few iterations.
        # The use of a decrementing multiplication factor protects us from
        # getting into an infinite loop.
        if scale == "auto":
            iteration = 0
            factor = 1.0

            while True:
                width = draw.textlength(self.css_icons[icon], font=font)

                # Check if the image fits
                dim = max(width, height)
                if dim > size:
                    font = PIL.ImageFont.truetype(
                        self.ttf_file,
                        int(size * size / dim * factor),
                    )
                else:
                    break

                # Adjust the factor every two iterations
                iteration += 1
                if iteration % 2 == 0:
                    factor *= 0.99

        draw.text(
            ((size - width) / 2, (size - height) / 2),
            self.css_icons[icon],
            font=font,
            fill=color,
        )

        # Get bounding box
        bbox = image.getbbox()

        # Create an alpha mask
        image_mask = PIL.Image.new("L", (size, size))
        draw_mask = PIL.ImageDraw.Draw(image_mask)

        # Draw the icon on the mask
        draw_mask.text(
            ((size - width) / 2, (size - height) / 2),
            self.css_icons[icon],
            font=font,
            fill=255,
        )

        # Create a solid color image and apply the mask
        icon_image = PIL.Image.new("RGBA", (size, size), color)
        icon_image.putalpha(image_mask)

        if bbox:
            icon_image = icon_image.crop(bbox)

        border_w = int((size - (bbox[2] - bbox[0])) / 2)  # type: ignore
        border_h = int((size - (bbox[3] - bbox[1])) / 2)  # type: ignore

        # Create output image
        out_image = PIL.Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out_image.paste(icon_image, (border_w, border_h))

        # If necessary, scale the image to the target size
        if org_size != size:
            out_image = out_image.resize(
                (org_size, org_size),
                PIL.Image.Resampling.LANCZOS,
            )

        # Make sure export directory exists
        if not pathlib.Path(export_dir).exists():
            pathlib.Path(export_dir).mkdir(parents=True)

        # Default filename
        if not filename:
            filename = icon + ".png"

        # Save file
        out_image.save(os.path.join(export_dir, filename))


def load_icons() -> dict[str, IconFont]:
    """
    Get the icons.

    Returns
    -------
    dict["str", IconFont]
        A dictionnary from icon name to IconFont.
    """
    icons = {}
    icon_font = IconFont(
        css_file=pathlib.Path(
            sys.prefix, "share", "pandoc_latex_tip", "fontawesome", "fontawesome.css"
        ),
        ttf_file=pathlib.Path(
            sys.prefix, "share", "pandoc_latex_tip", "fontawesome", "fa-solid-900.ttf"
        ),
    )
    icons.update({key: icon_font for key in icon_font.css_icons})
    icon_font = IconFont(
        css_file=pathlib.Path(
            sys.prefix, "share", "pandoc_latex_tip", "fontawesome", "fontawesome.css"
        ),
        ttf_file=pathlib.Path(
            sys.prefix, "share", "pandoc_latex_tip", "fontawesome", "fa-regular-400.ttf"
        ),
        prefix="far-",
    )
    icons.update({key: icon_font for key in icon_font.css_icons})
    icon_font = IconFont(
        css_file=pathlib.Path(
            sys.prefix, "share", "pandoc_latex_tip", "fontawesome", "brands.css"
        ),
        ttf_file=pathlib.Path(
            sys.prefix, "share", "pandoc_latex_tip", "fontawesome", "fa-brands-400.ttf"
        ),
    )
    icons.update({key: icon_font for key in icon_font.css_icons})

    config_path = pathlib.Path(sys.prefix, "share", "pandoc_latex_tip", "config.yml")
    if config_path.exists():
        with config_path.open(encoding="utf-8") as stream:
            config = yaml.safe_load(stream)
            for collection, definition in config.items():
                if "css" not in definition:
                    break
                if "css" not in definition:
                    break
                css_file = definition["css"]
                if "ttf" not in definition:
                    break
                ttf_file = definition["ttf"]
                icon_font = IconFont(
                    css_file=pathlib.Path(
                        sys.prefix,
                        "share",
                        "pandoc_latex_tip",
                        collection,
                        css_file,
                    ),
                    ttf_file=pathlib.Path(
                        sys.prefix,
                        "share",
                        "pandoc_latex_tip",
                        collection,
                        ttf_file,
                    ),
                    prefix=definition.get("prefix", False),
                )
                icons.update({key: icon_font for key in icon_font.css_icons})

    return icons


def tip(elem: Element, doc: Doc) -> list[Element] | None:
    """
    Apply tip transformation to element.

    Parameters
    ----------
    elem
        The element
    doc
        The original document.

    Returns
    -------
    list[Element] | None
        The additional elements if any.
    """
    # Is it in the right format and is it a Span, Div?
    if doc.format in ("latex", "beamer") and isinstance(
        elem, (Span, Div, Code, CodeBlock)
    ):
        # Is there a latex-tip-icon attribute?
        if "latex-tip-icon" in elem.attributes:
            return add_latex(
                elem,
                latex_code(
                    doc,
                    elem.attributes,
                    {
                        "icon": "latex-tip-icon",
                        "position": "latex-tip-position",
                        "size": "latex-tip-size",
                        "color": "latex-tip-color",
                        "link": "latex-tip-link",
                    },
                ),
            )

        # Get the classes
        classes = set(elem.classes)

        # Loop on all font size definition
        # noinspection PyUnresolvedReferences
        for definition in doc.defined:
            # Are the classes correct?
            if classes >= definition["classes"]:
                return add_latex(elem, definition["latex"])

    return None


def add_latex(elem: Element, latex: str) -> list[Element] | None:
    """
    Add latex code.

    Parameters
    ----------
    elem
        Current element
    latex
        Latex code

    Returns
    -------
    list[Element] | None
        The additional elements if any.
    """
    # pylint: disable=too-many-return-statements
    if bool(latex):
        # Is it a Span or a Code?
        if isinstance(elem, (Span, Code)):
            return [elem, RawInline(latex, "tex")]

        # It is a CodeBlock: create a minipage to ensure the
        # _tip to be on the same page as the codeblock
        if isinstance(elem, CodeBlock):
            return [
                RawBlock(f"\\begin{{minipage}}{{\\textwidth}}{latex}", "tex"),
                elem,
                RawBlock("\\end{minipage}", "tex"),
            ]

        while elem.content and isinstance(elem.content[0], Div):
            elem = elem.content[0]

        if not elem.content or isinstance(
            elem.content[0], (HorizontalRule, Figure, RawBlock, DefinitionList)
        ):
            elem.content.insert(0, RawBlock(latex, "tex"))
            return None
        if isinstance(elem.content[0], (Plain, Para)):
            elem.content[0].content.insert(1, RawInline(latex, "tex"))
            return None
        if isinstance(elem.content[0], LineBlock):
            elem.content[0].content[0].content.insert(1, RawInline(latex, "tex"))
            return None
        if isinstance(elem.content[0], CodeBlock):
            elem.content.insert(
                0,
                RawBlock(f"\\begin{{minipage}}{{\\textwidth}}{latex}", "tex"),
            )
            elem.content.insert(2, RawBlock("\\end{minipage}", "tex"))
            return None
        if isinstance(elem.content[0], (BulletList, OrderedList)):
            elem.content[0].content[0].content[0].content.insert(  # noqa: ECE001
                1,
                RawInline(latex, "tex"),
            )
            return None
        debug("[WARNING] pandoc-latex-tip: Bad usage")
    return None


# pylint: disable=too-many-arguments,too-many-locals
def latex_code(doc: Doc, definition: dict[str, Any], keys: dict[str, str]) -> str:
    """
    Get the latex code.

    Parameters
    ----------
    doc
        The original document
    definition
        The defition
    keys
        Key mapping

    Returns
    -------
    str
        The latex code.
    """
    # Get the default color
    color = str(definition.get(keys["color"], "black"))

    # Get the size
    size = get_size(str(definition.get(keys["size"], "18")))

    # Get the prefixes
    # noinspection PyArgumentEqualDefault
    prefix_odd = get_prefix(str(definition.get(keys["position"], "")), odd=True)
    prefix_even = get_prefix(str(definition.get(keys["position"], "")), odd=False)

    # Get the link
    link = str(definition.get(keys["link"], ""))

    # Get the icons
    icons = get_icons(doc, definition, keys["icon"], color, link)

    # Get the images
    images = create_images(doc, icons, size)

    if bool(images):
        # pylint: disable=consider-using-f-string
        return f"""
\\checkoddpage%%
\\ifoddpage%%
{prefix_odd}%%
\\else%%
{prefix_even}%%
\\fi%%
\\marginnote{{{''.join(images)}}}[0pt]\\vspace{{0cm}}%%
"""

    return ""


def get_icons(
    doc: Doc,
    definition: dict[str, Any],
    key_icons: str,
    color: str,
    link: str,
) -> list[dict[str, Any]]:
    """
    Get tge icons.

    Parameters
    ----------
    doc
        The original document
    definition
        The definition
    key_icons
        A key mapping
    color
        The color
    link
        The link

    Returns
    -------
    list[dict[str, Any]]
        A list of icon definitions.
    """
    # Test the icons definition
    if key_icons in definition:
        icons: list[dict[str, str]] = []
        # pylint: disable=invalid-name
        if isinstance(definition[key_icons], list):
            for icon in definition[key_icons]:
                try:
                    icon["color"] = icon.get("color", color)
                    icon["link"] = icon.get("link", link)
                except AttributeError:
                    icon = {
                        "name": icon,
                        "color": color,
                        "link": link,
                    }

                add_icon(doc, icons, icon)
        else:
            # noinspection PyUnresolvedReferences
            if definition[key_icons] in doc.icons:
                icons = [
                    {
                        "name": definition[key_icons],
                        "color": color,
                        "link": link,
                    }
                ]
            else:
                icons = []
    else:
        icons = [
            {
                "name": "fa-exclamation-circle",
                "color": color,
                "link": link,
            }
        ]

    return icons


def add_icon(doc: Doc, icons: list[dict[str, str]], icon: dict[str, str]) -> None:
    """
    Add icon.

    Parameters
    ----------
    doc
        The original document.
    icons
        A list of icon definition
    icon
        A potential new icon
    """
    if "name" not in icon:
        # Bad formed icon
        debug("[WARNING] pandoc-latex-tip: Bad formed icon")
        return

    # Lower the color
    lower_color = icon["color"].lower()

    # Convert the color to black if unexisting
    # pylint: disable=import-outside-toplevel

    if lower_color not in PIL.ImageColor.colormap:
        debug(
            f"[WARNING] pandoc-latex-tip: {lower_color}"
            " is not a correct color name; using black"
        )
        lower_color = "black"

    # Is the icon correct?
    try:
        # noinspection PyUnresolvedReferences
        if icon["name"] in doc.icons:
            icons.append(
                {
                    "name": icon["name"],
                    "color": lower_color,
                    "link": icon["link"],
                }
            )
        else:
            debug(
                f"[WARNING] pandoc-latex-tip: {icon['name']}"
                " is not a correct icon name"
            )
    except FileNotFoundError:
        debug("[WARNING] pandoc-latex-tip: error in accessing to icons definition")


# pylint:disable=too-many-return-statements
def get_prefix(position: str, odd: bool = True) -> str:
    """
    Get the latex prefix.

    Parameters
    ----------
    position
        The icon position
    odd
        Is the page is odd ?

    Returns
    -------
    str
        The latex prefix.
    """
    if position == "right":
        if odd:
            return "\\pandoclatextipoddright"
        return "\\pandoclatextipevenright"
    if position in ("left", ""):
        if odd:
            return "\\pandoclatextipoddleft"
        return "\\pandoclatextipevenleft"
    if position == "inner":
        if odd:
            return "\\pandoclatextipoddinner"
        return "\\pandoclatextipeveninner"
    if position == "outer":
        if odd:
            return "\\pandoclatextipoddouter"
        return "\\pandoclatextipevenouter"
    debug(
        f"[WARNING] pandoc-latex-tip: {position}"
        " is not a correct position; using left"
    )
    if odd:
        return "\\pandoclatextipoddleft"
    return "\\pandoclatextipevenleft"


def get_size(size: str) -> str:
    """
    Get the correct size.

    Parameters
    ----------
    size
        The initial size

    Returns
    -------
    str
        The correct size.
    """
    try:
        int_value = int(size)
        if int_value > 0:
            size = str(int_value)
        else:
            debug(
                f"[WARNING] pandoc-latex-tip: size must be greater than 0; using {size}"
            )
    except ValueError:
        debug(f"[WARNING] pandoc-latex-tip: size must be a number; using {size}")
    return size


def create_images(doc: Doc, icons: list[dict[str, Any]], size: str) -> list[str]:
    """
    Create the images.

    Parameters
    ----------
    doc
        The original document
    icons
        A list of icon definitions
    size
        The icon size.

    Returns
    -------
    list[str]
        A list of latex code.
    """
    # Generate the LaTeX image code
    images = []

    for icon in icons:
        # Get the image from the App cache folder
        # noinspection PyUnresolvedReferences
        image = os.path.join(doc.folder, icon["color"], icon["name"] + ".png")

        # Create the image if not existing in the cache
        try:
            if not os.path.isfile(image):
                # Create the image in the cache
                # noinspection PyUnresolvedReferences
                doc.icons[icon["name"]].export_icon(
                    icon["name"],
                    512,
                    color=icon["color"],
                    export_dir=os.path.join(doc.folder, icon["color"]),
                )

            # Add the LaTeX image
            image = Image(
                url=str(image), attributes={"width": size + "pt", "height": size + "pt"}
            )
            if icon["link"] == "":
                elem = image
            else:
                elem = Link(image, url=icon["link"])
            images.append(
                convert_text(
                    Plain(elem), input_format="panflute", output_format="latex"
                )
            )
        except TypeError:
            debug(
                f"[WARNING] pandoc-latex-tip: icon name "
                f"{icon['name']} does not exist"
            )
        except FileNotFoundError:
            debug("[WARNING] pandoc-latex-tip: error in generating image")

    return images


def add_definition(doc: Doc, definition: dict[str, Any]) -> None:
    """
    Add definition to document.

    Parameters
    ----------
    doc
        The original document
    definition
        The definition
    """
    # Get the classes
    classes = definition["classes"]

    # Add a definition if correct
    if bool(classes):
        latex = latex_code(
            doc,
            definition,
            {
                "icon": "icons",
                "position": "position",
                "size": "size",
                "color": "color",
                "link": "link",
            },
        )
        if latex:
            # noinspection PyUnresolvedReferences
            doc.defined.append({"classes": set(classes), "latex": latex})


def prepare(doc: Doc) -> None:
    """
    Prepare the document.

    Parameters
    ----------
    doc
        The original document.
    """
    # Add getIconFont library to doc
    doc.icons = load_icons()

    # Prepare the definitions
    doc.defined = []

    # Prepare the folder
    try:
        # Use user cache dir if possible
        doc.folder = platformdirs.AppDirs(
            "pandoc_latex_tip",
        ).user_cache_dir
        if not pathlib.Path(doc.folder).exists():
            pathlib.Path(doc.folder).mkdir(parents=True)
    except PermissionError:
        # Fallback to a temporary dir
        doc.folder = tempfile.mkdtemp(
            prefix="pandoc_latex_tip_",
            suffix="_cache",
        )

    # Get the meta data
    # noinspection PyUnresolvedReferences
    meta = doc.get_metadata("pandoc-latex-tip")

    if isinstance(meta, list):
        # Loop on all definitions
        for definition in meta:
            # Verify the definition
            if (
                isinstance(definition, dict)
                and "classes" in definition
                and isinstance(definition["classes"], list)
            ):
                add_definition(doc, definition)


def finalize(doc: Doc) -> None:
    """
    Finalize the document.

    Parameters
    ----------
    doc
        The original document
    """
    # Add header-includes if necessary
    if "header-includes" not in doc.metadata:
        doc.metadata["header-includes"] = MetaList()
    # Convert header-includes to MetaList if necessary
    elif not isinstance(doc.metadata["header-includes"], MetaList):
        doc.metadata["header-includes"] = MetaList(doc.metadata["header-includes"])

    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\usepackage{graphicx,grffile}", "tex"))
    )
    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\usepackage{marginnote}", "tex"))
    )
    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\usepackage{etoolbox}", "tex"))
    )
    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\usepackage[strict]{changepage}", "tex"))
    )
    doc.metadata["header-includes"].append(
        MetaInlines(
            RawInline(
                r"""
\makeatletter%
\newcommand{\pandoclatextipoddinner}{\reversemarginpar}%
\newcommand{\pandoclatextipeveninner}{\reversemarginpar}%
\newcommand{\pandoclatextipoddouter}{\normalmarginpar}%
\newcommand{\pandoclatextipevenouter}{\normalmarginpar}%
\newcommand{\pandoclatextipoddleft}{\reversemarginpar}%
\newcommand{\pandoclatextipoddright}{\normalmarginpar}%
\if@twoside%
\newcommand{\pandoclatextipevenright}{\reversemarginpar}%
\newcommand{\pandoclatextipevenleft}{\normalmarginpar}%
\else%
\newcommand{\pandoclatextipevenright}{\normalmarginpar}%
\newcommand{\pandoclatextipevenleft}{\reversemarginpar}%
\fi%
\makeatother%
\checkoddpage
    """,
                "tex",
            )
        )
    )


def main(doc: Doc | None = None) -> Doc:
    """
    Transform the pandoc document.

    Arguments
    ---------
    doc
        The pandoc document

    Returns
    -------
    Doc
        The transformed document
    """
    return run_filter(tip, prepare=prepare, finalize=finalize, doc=doc)


class NewCommand(Command):
    """
    NewCommand.
    """

    name = "{format}"
    description = "Add new collection"

    def handle(self) -> int:
        """
        Handle new command.

        Returns
        -------
        int
            status code
        """
        self.line("New")
        return 0


class PandocLaTeXFilterCommand(Command):
    """
    PandocLaTeXFilterCommand.
    """

    name = "latex"
    description = "Run pandoc filter for LaTeX document"

    def handle(self) -> int:
        """
        Handle latex command.

        Returns
        -------
        int
            status code
        """
        main()
        return 0


class PandocBeamerFilterCommand(Command):
    """
    PandocBeamerFilterCommand.
    """

    name = "beamer"
    description = "Run pandoc filter for Beamer document"

    def handle(self) -> int:
        """
        Handle beamer command.

        Returns
        -------
        int
            status code
        """
        main()
        return 0


def app() -> None:
    """
    Create a cleo application.
    """
    application = Application("Pandoc LaTeX Tip Filter")
    application.add(NewCommand())
    application.add(PandocLaTeXFilterCommand())
    application.add(PandocBeamerFilterCommand())
    application.run()


if __name__ == "__main__":
    main()