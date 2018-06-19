#!/usr/bin/env python

"""
Pandoc filter for adding tip in LaTeX
"""

from panflute import *
import os

try:
    FileNotFoundError
except NameError:
    #py2
    FileNotFoundError = IOError

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
                    'latex-tip-color'
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

def add_latex(elem, latex):
    if bool(latex):
        # Is it a Span or a Code?
        if isinstance(elem, Span) or isinstance(elem, Code):
            return [RawInline(latex, 'tex'), elem]

        # It is a CodeBlock: create a minipage to ensure the tip to be on the same page as the codeblock
        elif isinstance(elem, CodeBlock):
            return [RawBlock('\\begin{minipage}{\\textwidth}' + latex, 'tex'), elem, RawBlock('\\end{minipage}', 'tex')]
        # It is a Div: try to insert an inline raw before the first inline element
        else:
            inserted = [False]
            def insert(elem, doc):
                if not inserted[0] and isinstance(elem, Inline) and not isinstance(elem.parent, Inline):
                    inserted[0] = True
                    return [RawInline(latex, 'tex'), elem]
            elem.walk(insert)
            if not inserted[0]:
                return [RawBlock(latex, 'tex'), elem]

def latex_code(doc, definition, key_icon, key_position, key_size, key_color):
    # Get the default color
    color = get_color(doc, definition, key_color)

    # Get the size
    size = get_size(doc, definition, key_size)

    # Get the prefix
    prefix = get_prefix(doc, definition, key_position)

    # Get the icons
    icons = get_icons(doc, definition, key_icon, color)

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
    else:
        return ''


def get_icons(doc, definition, key_icons, color):
    icons = [{
        'name': 'exclamation-circle',
        'color': color,
        'version': '4.7',
        'variant': 'regular'
    }]

    # Test the icons definition
    if key_icons in definition:
        icons = []
        if isinstance(definition[key_icons], str) or isinstance(definition[key_icons], unicode):
            check_icon(doc, icons, definition[key_icons], color)
        elif isinstance(definition[key_icons], list):
            for icon in definition[key_icons]:
                check_icon(doc, icons, icon, color)

    return icons

# Fix unicode for python3
try:
    unicode = unicode
except (NameError):
    unicode = str

def check_icon(doc, icons, icon, color):
    version = '4.7'
    variant = 'regular'
    if isinstance(icon, str) or isinstance(icon, unicode):
        # Simple icon
        name = icon
    elif isinstance(icon, dict) and 'color' in icon and 'name' in icon:
        # Complex icon with name and color
        color = str(icon['color'])
        name = str(icon['name'])
        version
        if 'version' in icon:
            version = str(icon['version'])
        if 'variant' in icon:
            variant = str(icon['variant'])
    else:
        # Bad formed icon
        debug('[WARNING] pandoc-latex-tip: Bad formed icon')
        return

    add_icon(doc, icons, color, name, version, variant)

def add_icon(doc, icons, color, name, version, variant):
    # Lower the color
    lowerColor = color.lower()

    # Convert the color to black if unexisting
    from PIL import ImageColor
    if lowerColor not in ImageColor.colormap:
        debug('[WARNING] pandoc-latex-tip: ' + lowerColor + ' is not a correct color name; using black')
        lowerColor = 'black'

    # Is the icon correct?
    try:
        category = version + '-' + variant
        if category in doc.get_icon_font:
            if name in doc.get_icon_font[category].css_icons:
                icons.append({'name': name, 'color': lowerColor, 'version': version, 'variant': variant})
            else:
                debug('[WARNING] pandoc-latex-tip: ' + name + ' is not a correct icon name')
        else:
            debug('[WARNING] pandoc-latex-tip: ' + variant + ' does not exist in version ' + version)
    except FileNotFoundError:
        debug('[WARNING] pandoc-latex-tip: error in accessing to icons definition')

def get_color(doc, definition, key):
    if key in definition:
        return str(definition[key])
    else:
        return 'black'

def get_prefix(doc, definition, key):
    if key in definition:
        if definition[key] == 'right':
            return '\\normalmarginpar'
        elif definition[key] == 'left':
            return '\\reversemarginpar'
        else:
            debug('[WARNING] pandoc-latex-tip: ' + str(definition[key]) + ' is not a correct position; using left')
            return '\\reversemarginpar'
    return '\\reversemarginpar'

def get_size(doc, definition, key):
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
        dirs = AppDirs('pandoc_latex_tip', version = get_distribution('pandoc_latex_tip').version)

        # Get the image from the App cache folder
        image_dir = os.path.join(dirs.user_cache_dir, icon['version'], icon['variant'], icon['color'])
        image = os.path.join(image_dir, icon['name'] + '.png')

        # Create the image if not existing in the cache
        try:
            if not os.path.isfile(image):
                # Create the image in the cache
                doc.get_icon_font[icon['version'] + '-' + icon['variant']].export_icon(
                    icon['name'],
                    512,
                    color = icon['color'],
                    export_dir = image_dir
                )

            # Add the LaTeX image
            images.append('\\includegraphics[width=' + size + 'pt]{' + image + '}')
        except TypeError:
            debug('[WARNING] pandoc-latex-tip: icon name ' + icon['name'] + ' does not exist in variant ' + icon['variant'])
        except FileNotFoundError:
            debug('[WARNING] pandoc-latex-tip: error in generating image')

    return images

def add_definition(doc, definition):
    # Get the classes
    classes = definition['classes']

    # Add a definition if correct
    if bool(classes):
        latex = latex_code(doc, definition, 'icons', 'position', 'size', 'color')
        if latex:
            doc.defined.append({'classes' : set(classes), 'latex': latex})

def prepare(doc):
    # Add getIconFont library to doc
    import icon_font_to_png
    from pkg_resources import get_distribution
    from appdirs import AppDirs
    dirs = AppDirs('pandoc_latex_tip', version = get_distribution('pandoc_latex_tip').version)
    doc.get_icon_font = {
        '4.7-regular': icon_font_to_png.IconFont(
            os.path.join(dirs.user_data_dir, '4.7', 'font-awesome.css'),
            os.path.join(dirs.user_data_dir, '4.7', 'fontawesome-webfont.ttf')
        ),
        '5.0-brands': icon_font_to_png.IconFont(
            os.path.join(dirs.user_data_dir, '5.0', 'fontawesome.css'),
            os.path.join(dirs.user_data_dir, '5.0', 'fa-brands-400.ttf')
        ),
        '5.0-regular': icon_font_to_png.IconFont(
            os.path.join(dirs.user_data_dir, '5.0', 'fontawesome.css'),
            os.path.join(dirs.user_data_dir, '5.0', 'fa-regular-400.ttf')
        ),
        '5.0-solid': icon_font_to_png.IconFont(
            os.path.join(dirs.user_data_dir, '5.0', 'fontawesome.css'),
            os.path.join(dirs.user_data_dir, '5.0', 'fa-solid-900.ttf')
        )
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

def main(doc = None):
    return run_filter(tip, prepare = prepare, finalize = finalize, doc = doc)

if __name__ == '__main__':
    main()

