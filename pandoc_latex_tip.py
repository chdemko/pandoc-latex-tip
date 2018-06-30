#!/usr/bin/env python

"""
Pandoc filter for adding tip in LaTeX
"""

import os

from panflute import run_filter, convert_text, debug, Span, Code, CodeBlock, Inline, RawBlock, RawInline, Image, Link, Plain, MetaList, MetaInlines

try:
    FileNotFoundError
except NameError:
    # py2
    FileNotFoundError = IOError  # pylint: disable=redefined-builtin


def tip(elem, doc):
    # Is it in the right format and is it a Span, Div?
    if doc.format in ['latex', 'beamer'] and elem.tag in ['Span', 'Div', 'Code', 'CodeBlock']:

        # Is there a latex-tip-icon attribute?
        if 'latex-tip-icon' in elem.attributes:
            return add_latex(
                elem,
                latex_code(
                    doc,
                    elem.attributes,
                    'latex-tip-icon',
                    'latex-tip-position',
                    'latex-tip-size',
                    'latex-tip-color',
                    'latex-tip-collection',
                    'latex-tip-version',
                    'latex-tip-variant',
                    'latex-tip-link'
                )
            )
        else:
            # Get the classes
            classes = set(elem.classes)

            # Loop on all fontsize definition
            for definition in doc.defined:

                # Are the classes correct?
                if classes >= definition['classes']:
                    return add_latex(elem, definition['latex'])

    return None


def add_latex(elem, latex):
    if bool(latex):
        # Is it a Span or a Code?
        if isinstance(elem, (Span, Code)):
            return [RawInline(latex, 'tex'), elem]

        # It is a CodeBlock: create a minipage to ensure the tip to be on the same page as the codeblock
        elif isinstance(elem, CodeBlock):
            return [RawBlock('\\begin{minipage}{\\textwidth}' + latex, 'tex'), elem, RawBlock('\\end{minipage}', 'tex')]
        # It is a Div: try to insert an inline raw before the first inline element
        else:
            inserted = [False]

            def insert(elem, _):
                if not inserted[0] and isinstance(elem, Inline) and not isinstance(elem.parent, Inline):
                    inserted[0] = True
                    return [RawInline(latex, 'tex'), elem]
                return None

            elem.walk(insert)
            if not inserted[0]:
                return [RawBlock(latex, 'tex'), elem]

    return None


# pylint: disable=too-many-arguments,too-many-locals
def latex_code(doc, definition, key_icon, key_position, key_size, key_color, key_collection, key_version, key_variant, key_link):
    # Get the default color
    color = get_color(doc, definition, key_color)

    # Get the size
    size = get_size(doc, definition, key_size)

    # Get the prefix
    prefix = get_prefix(doc, definition, key_position)

    # Get the collection
    collection = get_collection(doc, definition, key_collection)

    # Get the version
    version = get_version(doc, definition, key_version)

    # Get the variant
    variant = get_variant(doc, definition, key_variant)

    # Get the link
    link = get_link(doc, definition, key_link)

    # Get the icons
    icons = get_icons(doc, definition, key_icon, color, collection, version, variant, link)

    # Get the images
    images = create_images(doc, icons, size)

    if bool(images):
        # Prepare LaTeX code
        latex = [
            '{',
            '\\makeatletter',
            '\\patchcmd{\\@mn@margintest}{\\@tempswafalse}{\\@tempswatrue}{}{}',
            '\\patchcmd{\\@mn@margintest}{\\@tempswafalse}{\\@tempswatrue}{}{}',
            '\\makeatother',
            prefix,
            '\\marginnote{'
        ] + images + [
            '}[0pt]',
            '\\vspace{0cm}',
            '}',
        ]

        # Return LaTeX code
        return ''.join(latex)
    return ''


def get_icons(doc, definition, key_icons, color, collection, version, variant, link):
    icons = [{
        'extended-name': 'fa-exclamation-circle',
        'name': 'exclamation-circle',
        'color': color,
        'collection': collection,
        'version': version,
        'variant': variant,
        'link': link
    }]

    # Test the icons definition
    if key_icons in definition:
        icons = []
        # pylint: disable=invalid-name
        if isinstance(definition[key_icons], (str, unicode)):
            check_icon(doc, icons, definition[key_icons], color, collection, version, variant, link)
        elif isinstance(definition[key_icons], list):
            for icon in definition[key_icons]:
                check_icon(doc, icons, icon, color, collection, version, variant, link)

    return icons


# Fix unicode for python3
# pylint: disable=invalid-name
try:
    # pylint: disable=redefined-builtin
    unicode = unicode
except NameError:
    unicode = str


def check_icon(doc, icons, icon, color, collection, version, variant, link):
    if isinstance(icon, (str, unicode)):
        # Simple icon
        name = icon
    elif isinstance(icon, dict) and 'color' in icon and 'name' in icon:
        # Complex icon with name and color
        color = str(icon['color'])
        name = str(icon['name'])
        if 'collection' in icon:
            collection = str(icon['collection'])
        if 'version' in icon:
            version = str(icon['version'])
        if 'variant' in icon:
            variant = str(icon['variant'])
        if 'link' in icon:
            link = str(icon['link'])
    else:
        # Bad formed icon
        debug('[WARNING] pandoc-latex-tip: Bad formed icon')
        return

    add_icon(doc, icons, color, name, collection, version, variant, link)


def add_icon(doc, icons, color, name, collection, version, variant, link):
    # Lower the color
    lower_color = color.lower()

    # Convert the color to black if unexisting
    from PIL import ImageColor
    if lower_color not in ImageColor.colormap:
        debug('[WARNING] pandoc-latex-tip: ' + lower_color + ' is not a correct color name; using black')
        lower_color = 'black'

    # Is the icon correct?
    try:
        category = collection + '-' + version + '-' + variant
        if category in doc.get_icon_font:
            extended_name = doc.get_icon_font[category]['prefix'] + name
            if extended_name in doc.get_icon_font[category]['font'].css_icons:
                icons.append({
                    'name': name,
                    'extended-name': extended_name,
                    'color': lower_color,
                    'collection': collection,
                    'version': version,
                    'variant': variant,
                    'link': link
                })
            else:
                debug('[WARNING] pandoc-latex-tip: ' + name + ' is not a correct icon name')
        else:
            debug('[WARNING] pandoc-latex-tip: ' + variant + ' does not exist in version ' + version)
    except FileNotFoundError:
        debug('[WARNING] pandoc-latex-tip: error in accessing to icons definition')


def get_color(_, definition, key):
    if key in definition:
        return str(definition[key])
    return 'black'


def get_prefix(_, definition, key):
    if key in definition:
        if definition[key] == 'right':
            return '\\normalmarginpar'
        elif definition[key] == 'left':
            return '\\reversemarginpar'
        debug('[WARNING] pandoc-latex-tip: ' + str(definition[key]) + ' is not a correct position; using left')

    return '\\reversemarginpar'


def get_version(_, definition, key):
    if key in definition:
        return str(definition[key])
    return '4.7'


def get_collection(_, definition, key):
    if key in definition:
        return str(definition[key])
    return 'fontawesome'


def get_variant(_, definition, key):
    if key in definition:
        return str(definition[key])
    return 'regular'


def get_link(_, definition, key):
    if key in definition:
        return str(definition[key])
    return None


def get_size(_, definition, key):
    # Get the size
    size = '18'
    if key in definition:
        try:
            intValue = int(definition[key])
            if intValue > 0:
                size = str(intValue)
            else:
                debug('[WARNING] pandoc-latex-tip: size must be greater than 0; using ' + size)
        except ValueError:
            debug('[WARNING] pandoc-latex-tip: size must be a number; using ' + size)
    return size


def create_images(doc, icons, size):
    # Generate the LaTeX image code
    images = []

    for icon in icons:

        # Get the apps dirs
        from pkg_resources import get_distribution
        from appdirs import AppDirs
        dirs = AppDirs('pandoc_latex_tip', version=get_distribution('pandoc_latex_tip').version)

        # Get the image from the App cache folder
        image_dir = os.path.join(
            dirs.user_cache_dir,
            icon['collection'],
            icon['version'],
            icon['variant'],
            icon['color']
        )
        image = os.path.join(image_dir, icon['extended-name'] + '.png')

        # Create the image if not existing in the cache
        try:
            if not os.path.isfile(image):
                # Create the image in the cache
                category = icon['collection'] + '-' + icon['version'] + '-' + icon['variant']
                doc.get_icon_font[category]['font'].export_icon(
                    icon['extended-name'],
                    512,
                    color=icon['color'],
                    export_dir=image_dir
                )

            # Add the LaTeX image
            image = Image(url=image, attributes={'width': size + 'pt', 'height': size + 'pt'})
            if icon['link'] is None:
                elem = image
            else:
                elem = Link(image, url=icon['link'])
            images.append(convert_text(Plain(elem), input_format='panflute', output_format='latex'))
        except TypeError:
            debug('[WARNING] pandoc-latex-tip: icon name ' + icon['name'] + ' does not exist in variant ' + icon['variant'] + ' for collection ' + icon['collection'] + '-' + icon['version'])
        except FileNotFoundError:
            debug('[WARNING] pandoc-latex-tip: error in generating image')

    return images


def add_definition(doc, definition):
    # Get the classes
    classes = definition['classes']

    # Add a definition if correct
    if bool(classes):
        latex = latex_code(
            doc,
            definition,
            'icons',
            'position',
            'size',
            'color',
            'collection',
            'version',
            'variant',
            'link'
        )
        if latex:
            doc.defined.append({'classes': set(classes), 'latex': latex})


def prepare(doc):
    # Add getIconFont library to doc
    import icon_font_to_png
    from pkg_resources import get_distribution
    from appdirs import AppDirs
    dirs = AppDirs('pandoc_latex_tip', version=get_distribution('pandoc_latex_tip').version)
    doc.get_icon_font = {
        'fontawesome-4.7-regular': {
            'font': icon_font_to_png.IconFont(
                os.path.join(dirs.user_data_dir, 'fontawesome', '4.7', 'font-awesome.css'),
                os.path.join(dirs.user_data_dir, 'fontawesome', '4.7', 'fontawesome-webfont.ttf'),
                True
            ),
            'prefix': 'fa-'
        },
        'fontawesome-5.0-brands': {
            'font': icon_font_to_png.IconFont(
                os.path.join(dirs.user_data_dir, 'fontawesome', '5.0', 'fontawesome.css'),
                os.path.join(dirs.user_data_dir, 'fontawesome', '5.0', 'fa-brands-400.ttf'),
                True
            ),
            'prefix': 'fa-'
        },
        'fontawesome-5.0-regular': {
            'font': icon_font_to_png.IconFont(
                os.path.join(dirs.user_data_dir, 'fontawesome', '5.0', 'fontawesome.css'),
                os.path.join(dirs.user_data_dir, 'fontawesome', '5.0', 'fa-regular-400.ttf'),
                True
            ),
            'prefix': 'fa-'
        },
        'fontawesome-5.0-solid': {
            'font': icon_font_to_png.IconFont(
                os.path.join(dirs.user_data_dir, 'fontawesome', '5.0', 'fontawesome.css'),
                os.path.join(dirs.user_data_dir, 'fontawesome', '5.0', 'fa-solid-900.ttf'),
                True
            ),
            'prefix': 'fa-'
        },
        'glyphicons-3.3-regular': {
            'font': icon_font_to_png.IconFont(
                os.path.join(dirs.user_data_dir, 'glyphicons', '3.3', 'bootstrap-modified.css'),
                os.path.join(dirs.user_data_dir, 'glyphicons', '3.3', 'glyphicons-halflings-regular.ttf'),
                True
            ),
            'prefix': 'glyphicon-'
        },
        'materialdesign-2.4-regular': {
            'font': icon_font_to_png.IconFont(
                os.path.join(dirs.user_data_dir, 'materialdesign', '2.4', 'materialdesignicons.css'),
                os.path.join(dirs.user_data_dir, 'materialdesign', '2.4', 'materialdesignicons-webfont.ttf'),
                True
            ),
            'prefix': 'mdi-'
        }
    }

    # Prepare the definitions
    doc.defined = []

    # Get the meta data
    meta = doc.get_metadata('pandoc-latex-tip')

    if isinstance(meta, list):

        # Loop on all definitions
        for definition in meta:

            # Verify the definition
            if isinstance(definition, dict) and 'classes' in definition and isinstance(definition['classes'], list):
                add_definition(doc, definition)


def finalize(doc):
    # Add header-includes if necessary
    if 'header-includes' not in doc.metadata:
        doc.metadata['header-includes'] = MetaList()
    # Convert header-includes to MetaList if necessary
    elif not isinstance(doc.metadata['header-includes'], MetaList):
        doc.metadata['header-includes'] = MetaList(doc.metadata['header-includes'])

    doc.metadata['header-includes'].append(MetaInlines(RawInline('\\usepackage{graphicx,grffile}', 'tex')))
    doc.metadata['header-includes'].append(MetaInlines(RawInline('\\usepackage{marginnote}', 'tex')))
    doc.metadata['header-includes'].append(MetaInlines(RawInline('\\usepackage{etoolbox}', 'tex')))


def main(doc=None):
    return run_filter(tip, prepare=prepare, finalize=finalize, doc=doc)


if __name__ == '__main__':
    main()
