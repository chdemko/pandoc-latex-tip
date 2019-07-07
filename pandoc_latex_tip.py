#!/usr/bin/env python

"""
Pandoc filter for adding tip in LaTeX
"""

# pylint: disable=bad-continuation

import os

from panflute import (
    run_filter,
    convert_text,
    debug,
    Span,
    Code,
    CodeBlock,
    Inline,
    RawBlock,
    RawInline,
    Image,
    Link,
    Plain,
    MetaList,
    MetaInlines,
)

try:
    FileNotFoundError
except NameError:
    # py2
    FileNotFoundError = IOError  # pylint: disable=redefined-builtin


def _icon_font(collection, version, css, ttf):
    import appdirs
    from pkg_resources import get_distribution

    folder = appdirs.AppDirs(
        "pandoc_latex_tip", version=get_distribution("pandoc_latex_tip").version
    ).user_data_dir
    import icon_font_to_png

    try:
        return icon_font_to_png.IconFont(
            os.path.join(folder, collection, version, css),
            os.path.join(folder, collection, version, ttf),
            True,
        )
    except FileNotFoundError as exception:
        debug("[ERROR] pandoc-latex-tip: " + str(exception))


_ICON_FONTS = {
    "fontawesome-4.7-regular": {
        "font": _icon_font(
            "fontawesome", "4.7", "font-awesome.css", "fontawesome-webfont.ttf"
        ),
        "prefix": "fa-",
    },
    "fontawesome-5.x-brands": {
        "font": _icon_font(
            "fontawesome", "5.x", "fontawesome.css", "fa-brands-400.ttf"
        ),
        "prefix": "fa-",
    },
    "fontawesome-5.x-regular": {
        "font": _icon_font(
            "fontawesome", "5.x", "fontawesome.css", "fa-regular-400.ttf"
        ),
        "prefix": "fa-",
    },
    "fontawesome-5.x-solid": {
        "font": _icon_font("fontawesome", "5.x", "fontawesome.css", "fa-solid-900.ttf"),
        "prefix": "fa-",
    },
    "glyphicons-3.3-regular": {
        "font": _icon_font(
            "glyphicons",
            "3.3",
            "bootstrap-modified.css",
            "glyphicons-halflings-regular.ttf",
        ),
        "prefix": "glyphicon-",
    },
    "materialdesign-3.x-regular": {
        "font": _icon_font(
            "materialdesign",
            "3.x",
            "materialdesignicons.css",
            "materialdesignicons-webfont.ttf",
        ),
        "prefix": "mdi-",
    },
}


def _tip(elem, doc):
    # Is it in the right format and is it a Span, Div?
    if doc.format in ["latex", "beamer"] and elem.tag in [
        "Span",
        "Div",
        "Code",
        "CodeBlock",
    ]:

        # Is there a latex-tip-icon attribute?
        if "latex-tip-icon" in elem.attributes:
            return _add_latex(
                elem,
                _latex_code(
                    doc,
                    elem.attributes,
                    {
                        "icon": "latex-tip-icon",
                        "position": "latex-tip-position",
                        "size": "latex-tip-size",
                        "color": "latex-tip-color",
                        "collection": "latex-tip-collection",
                        "version": "latex-tip-version",
                        "variant": "latex-tip-variant",
                        "link": "latex-tip-link",
                    },
                ),
            )

        # Get the classes
        classes = set(elem.classes)

        # Loop on all font size definition
        for definition in doc.defined:

            # Are the classes correct?
            if classes >= definition["classes"]:
                return _add_latex(elem, definition["latex"])

    return None


def _add_latex(elem, latex):
    if bool(latex):
        # Is it a Span or a Code?
        if isinstance(elem, (Span, Code)):
            return [elem, RawInline(latex, "tex")]

        # It is a CodeBlock: create a minipage to ensure the _tip to be on the same page as the codeblock
        if isinstance(elem, CodeBlock):
            return [
                RawBlock("\\begin{minipage}{\\textwidth}" + latex, "tex"),
                elem,
                RawBlock("\\end{minipage}", "tex"),
            ]

        # It is a Div: try to insert an inline raw before the first inline element
        inserted = [False]

        def insert(element, _):
            if (
                not inserted[0]
                and isinstance(element, Inline)
                and not isinstance(element.parent, Inline)
            ):
                inserted[0] = True
                return [RawInline("\\needspace{5em}", "tex"), RawInline(latex, "tex"), element]
            return None

        elem.walk(insert)
        if not inserted[0]:
            return [RawBlock(latex, "tex"), elem]

    return None


# pylint: disable=too-many-arguments,too-many-locals
def _latex_code(doc, definition, keys):
    # Get the default color
    color = str(definition.get(keys["color"], "black"))

    # Get the size
    size = _get_size(str(definition.get(keys["size"], "18")))

    # Get the prefixes
    prefix_odd = _get_prefix(str(definition.get(keys["position"], "")), True)
    prefix_even = _get_prefix(str(definition.get(keys["position"], "")), False)

    # Get the collection
    collection = str(definition.get(keys["collection"], "fontawesome"))

    # Get the version
    version = str(definition.get(keys["version"], "4.7"))

    # Get the variant
    variant = str(definition.get(keys["variant"], "regular"))

    # Get the link
    link = str(definition.get(keys["link"], ""))

    # Get the icons
    icons = _get_icons(
        doc, definition, keys["icon"], color, collection, version, variant, link
    )

    # Get the images
    images = _create_images(doc, icons, size)

    if bool(images):
        return r"""
\checkoddpage%%
\ifoddpage%%
%s%%
\else%%
%s%%
\fi%%
\marginnote{%s}[0pt]\vspace{0cm}%%
""" % (
            prefix_odd,
            prefix_even,
            "".join(images),
        )

    return ""


def _get_icons(doc, definition, key_icons, color, collection, version, variant, link):
    # Test the icons definition
    if key_icons in definition:
        icons = []
        # pylint: disable=invalid-name
        if isinstance(definition[key_icons], (str, unicode)):
            def_icons = [
                {
                    "name": definition[key_icons],
                    "color": color,
                    "collection": collection,
                    "version": version,
                    "variant": variant,
                    "link": link,
                }
            ]
        else:
            def_icons = definition[key_icons]
        if isinstance(def_icons, list):
            for icon in def_icons:
                try:
                    icon["color"] = icon.get("color", color)
                    icon["collection"] = icon.get("collection", collection)
                    icon["version"] = icon.get("version", version)
                    icon["variant"] = icon.get("variant", variant)
                    icon["link"] = icon.get("link", link)
                except AttributeError:
                    icon = {"name": icon}
                    icon["color"] = color
                    icon["collection"] = collection
                    icon["version"] = version
                    icon["variant"] = variant
                    icon["link"] = link

                _add_icon(doc, icons, icon)
    else:
        icons = [
            {
                "extended-name": "fa-exclamation-circle",
                "name": "exclamation-circle",
                "color": color,
                "collection": collection,
                "version": version,
                "variant": variant,
                "link": link,
            }
        ]

    return icons


# Fix unicode for python3
# pylint: disable=invalid-name
try:
    # pylint: disable=redefined-builtin
    unicode = unicode
except NameError:
    unicode = str


def _add_icon(doc, icons, icon):
    if "name" not in icon:
        # Bad formed icon
        debug("[WARNING] pandoc-latex-tip: Bad formed icon")
        return

    # Lower the color
    lower_color = icon["color"].lower()

    # Convert the color to black if unexisting
    from PIL import ImageColor

    if lower_color not in ImageColor.colormap:
        debug(
            "[WARNING] pandoc-latex-tip: "
            + lower_color
            + " is not a correct color name; using black"
        )
        lower_color = "black"

    # Is the icon correct?
    try:
        category = _category(icon["collection"], icon["version"], icon["variant"])
        if category in doc.get_icon_font:
            extended_name = doc.get_icon_font[category]["prefix"] + icon["name"]
            if extended_name in doc.get_icon_font[category]["font"].css_icons:
                icons.append(
                    {
                        "name": icon["name"],
                        "extended-name": extended_name,
                        "color": lower_color,
                        "collection": icon["collection"],
                        "version": icon["version"],
                        "variant": icon["variant"],
                        "link": icon["link"],
                    }
                )
            else:
                debug(
                    "[WARNING] pandoc-latex-tip: "
                    + icon["name"]
                    + " is not a correct icon name"
                )
        else:
            debug(
                "[WARNING] pandoc-latex-tip: "
                + icon["variant"]
                + " does not exist in version "
                + icon["version"]
            )
    except FileNotFoundError:
        debug("[WARNING] pandoc-latex-tip: error in accessing to icons definition")


def _category(collection, version, variant):
    return collection + "-" + version + "-" + variant


# pylint:disable=too-many-return-statements
def _get_prefix(position, odd=True):
    if position == "right":
        if odd:
            return "\\oddrighttip"
        return "\\evenrighttip"
    if position in ["left", ""]:
        if odd:
            return "\\oddlefttip"
        return "\\evenlefttip"
    if position == "inner":
        if odd:
            return "\\oddinnertip"
        return "\\eveninnertip"
    if position == "outer":
        if odd:
            return "\\oddoutertip"
        return "\\evenoutertip"
    debug(
        "[WARNING] pandoc-latex-tip: "
        + position
        + " is not a correct position; using left"
    )
    if odd:
        return "\\oddlefttip"
    return "\\evenlefttip"


def _get_size(size):
    try:
        int_value = int(size)
        if int_value > 0:
            size = str(int_value)
        else:
            debug(
                "[WARNING] pandoc-latex-tip: size must be greater than 0; using " + size
            )
    except ValueError:
        debug("[WARNING] pandoc-latex-tip: size must be a number; using " + size)
    return size


def _create_images(doc, icons, size):
    # Generate the LaTeX image code
    images = []

    for icon in icons:

        # Get the apps dirs
        from pkg_resources import get_distribution
        import appdirs

        folder = appdirs.AppDirs(
            "pandoc_latex_tip", version=get_distribution("pandoc_latex_tip").version
        ).user_cache_dir

        # Get the image from the App cache folder
        image_dir = os.path.join(
            folder, icon["collection"], icon["version"], icon["variant"], icon["color"]
        )
        image = os.path.join(image_dir, icon["extended-name"] + ".png")

        # Create the image if not existing in the cache
        try:
            if not os.path.isfile(image):
                # Create the image in the cache
                category = _category(
                    icon["collection"], icon["version"], icon["variant"]
                )
                doc.get_icon_font[category]["font"].export_icon(
                    icon["extended-name"],
                    512,
                    color=icon["color"],
                    export_dir=image_dir,
                )

            # Add the LaTeX image
            image = Image(
                url=image, attributes={"width": size + "pt", "height": size + "pt"}
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
                "[WARNING] pandoc-latex-tip: icon name "
                + icon["name"]
                + " does not exist in variant "
                + icon["variant"]
                + " for collection "
                + icon["collection"]
                + "-"
                + icon["version"]
            )
        except FileNotFoundError:
            debug("[WARNING] pandoc-latex-tip: error in generating image")

    return images


def _add_definition(doc, definition):
    # Get the classes
    classes = definition["classes"]

    # Add a definition if correct
    if bool(classes):
        latex = _latex_code(
            doc,
            definition,
            {
                "icon": "icons",
                "position": "position",
                "size": "size",
                "color": "color",
                "collection": "collection",
                "version": "version",
                "variant": "variant",
                "link": "link",
            },
        )
        if latex:
            doc.defined.append({"classes": set(classes), "latex": latex})


def _prepare(doc):
    # Add getIconFont library to doc
    doc.get_icon_font = _ICON_FONTS

    # Prepare the definitions
    doc.defined = []

    # Get the meta data
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
                _add_definition(doc, definition)


def _finalize(doc):
    # Add header-includes if necessary
    if "header-includes" not in doc.metadata:
        doc.metadata["header-includes"] = MetaList()
    # Convert header-includes to MetaList if necessary
    elif not isinstance(doc.metadata["header-includes"], MetaList):
        doc.metadata["header-includes"] = MetaList(doc.metadata["header-includes"])

    doc.metadata["header-includes"].append(
        MetaInlines(RawInline("\\usepackage{needspace}", "tex"))
    )
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
        MetaInlines(RawInline("\\usepackage{changepage}\n\\strictpagecheck", "tex"))
    )
    doc.metadata["header-includes"].append(
        MetaInlines(
            RawInline(
                r"""
\makeatletter%
\@ifpackagelater{marginnote}{2018/04/12}%
{%
\newcommand{\oddinnertip}{\reversemarginpar}%
\newcommand{\eveninnertip}{\reversemarginpar}%
\newcommand{\oddoutertip}{\normalmarginpar}%
\newcommand{\evenoutertip}{\normalmarginpar}%
\newcommand{\oddlefttip}{\reversemarginpar}%
\newcommand{\evenlefttip}{\normalmarginpar}%
\newcommand{\oddrighttip}{\normalmarginpar}%
\newcommand{\evenrighttip}{\reversemarginpar}%
}%
{%
\if@twoside%
\newcommand{\oddinnertip}{\reversemarginpar}%
\newcommand{\eveninnertip}{\reversemarginpar}%
\newcommand{\oddoutertip}{\normalmarginpar}%
\newcommand{\evenoutertip}{\normalmarginpar}%
\newcommand{\oddlefttip}{\reversemarginpar}%
\newcommand{\evenlefttip}{\normalmarginpar}%
\newcommand{\oddrighttip}{\reversemarginpar}%
\newcommand{\evenrighttip}{\normalmarginpar}%
\else%
\newcommand{\oddinnertip}{\reversemarginpar}%
\newcommand{\eveninnertip}{\reversemarginpar}%
\newcommand{\oddoutertip}{\normalmarginpar}%
\newcommand{\evenoutertip}{\normalmarginpar}%
\newcommand{\oddlefttip}{\reversemarginpar}%
\newcommand{\evenlefttip}{\reversemarginpar}%
\newcommand{\oddrighttip}{\normalmarginpar}%
\newcommand{\evenrighttip}{\normalmarginpar}%
\fi%
}%
\makeatother%
    """,
                "tex",
            )
        )
    )


def main(doc=None):
    return run_filter(_tip, prepare=_prepare, finalize=_finalize, doc=doc)


if __name__ == "__main__":
    main()
