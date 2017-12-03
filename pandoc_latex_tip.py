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

def add_latex(elem, latex):
    # Is it a Span or a Code?
    if isinstance(elem, Span) or isinstance(elem, Code):
        return [RawInline(latex, 'tex'), elem]

    # It is a Div or a CodeBlock
    else:
        return [RawBlock(latex, 'tex'), elem]

def tip(elem, doc):
    # Is it in the right format and is it a Span, Div?
    if doc.format == 'latex' and elem.tag in ['Span', 'Div', 'Code', 'CodeBlock']:

        # Is there a latex-tip-icon attribute?
        if 'latex-tip-icon' in elem.attributes:
            return add_latex(elem, latex_code(elem.attributes))
        else:
            # Get the classes
            classes = set(elem.classes)

            # Loop on all fontsize definition
            for definition in doc.defined:

                # Are the classes correct?
                if classes >= definition['classes']:
                    return add_latex(elem, definition['latex'])

def prepare(doc):
    # Add getIconFont library to doc
    import icon_font_to_png
    from pkg_resources import get_distribution
    from appdirs import AppDirs
    dirs = AppDirs('pandoc_latex_tip', version = get_distribution('pandoc_latex_tip').version)
    doc.getIconFont = icon_font_to_png.IconFont(
        dirs.user_data_dir + '/font-awesome.css',
        dirs.user_data_dir + '/fontawesome-webfont.ttf'
    )

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
    if 'header-includes' not in doc.metadata:
        doc.metadata['header-includes'] = []
    doc.metadata['header-includes'].append(MetaInlines(RawInline('\\usepackage{graphicx,grffile}', 'tex')))
    doc.metadata['header-includes'].append(MetaInlines(RawInline('\\usepackage{marginnote}', 'tex')))
    doc.metadata['header-includes'].append(MetaInlines(RawInline('\\usepackage{etoolbox}', 'tex')))

def latex_code(prefix, images):
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
    return ''.join(latex)

def get_icons(doc, definition):
    icons = [{'name': 'exclamation-circle', 'color': 'black'}]

    # Test the icons definition
    if 'icons' in definition and isinstance(definition['icons'], list):
        icons = []
        for icon in definition['icons']:
        	add_icon(doc, icons, icon)

    return icons

def add_icon(doc, icons, icon):
    if isinstance(icon, str) or isinstance(icon, unicode):
        # Simple icon
        color = 'black'
        name = icon
    elif isinstance(icon, dict) and 'color' in icon and 'name' in icon:
        # Complex icon with name and color
        color = str(icon['color'])
        name = str(icon['name'])
    else:
        # Bad formed icon
        debug('[WARNING] pandoc-latex-tip: Bad formed icon')
        return

    # Lower the color
    lowerColor = color.lower()

    # Convert the color to black if unexisting
    from PIL import ImageColor
    if lowerColor not in ImageColor.colormap:
        debug('[WARNING] pandoc-latex-tip: ' + lowerColor + ' is not a correct color name; using black')
        lowerColor = 'black'

    # Is the icon correct?
    try:
        if name in doc.getIconFont.css_icons:
            icons.append({'name': name, 'color': lowerColor})
        else:
            debug('[WARNING] pandoc-latex-tip: ' + name + ' is not a correct icon name')
    except FileNotFoundError:
        debug('[WARNING] pandoc-latex-tip: error in accessing to icons definition')

def get_prefix(definition):
    if 'position' in definition:
        if definition['position'] == 'right':
            return '\\normalmarginpar'
        elif definition['position'] == 'left':
            return '\\reversemarginpar'
        else:
            debug('[WARNING] pandoc-latex-tip: ' + position + ' is not a correct position; using left')
            return '\\reversemarginpar'
    return '\\reversemarginpar'

def get_size(definition):
   # Get the size
    size = '18'
    if 'size' in definition:
        try:
            intValue = int(definition['size'])
            if intValue > 0:
                size = str(intValue)
            else:
                debug('[WARNING] pandoc-latex-tip: size must be greater than 0; using ' + size)
        except ValueError:
            debug('[WARNING] pandoc-latex-tip: size must be a number; using ' + size)
    return size

def get_images(icons, size):
    # Generate the LaTeX image code
    images = []

    for icon in icons:

        # Get the apps dirs
        from pkg_resources import get_distribution
        from appdirs import AppDirs
        dirs = AppDirs('pandoc_latex_tip', version = get_distribution('pandoc_latex_tip').version)

        # Get the image from the App cache folder
        image = dirs.user_cache_dir + '/' + icon['color'] + '/' + icon['name'] + '.png'

        # Create the image if not existing in the cache
        try:
            if not os.path.isfile(image):

                # Create the image in the cache
                doc.getIconFont.export_icon(
                    icon['name'],
                    size = 512,
                    color = icon['color'],
                    export_dir = dirs.user_cache_dir + '/' + icon['color']
                )

            # Add the LaTeX image
            images.append('\\includegraphics[width=' + size + 'pt]{' + image + '}')
        except FileNotFoundError:
            debug('[WARNING] pandoc-latex-tip: error in generating image')

    return images

def add_definition(doc, definition):
    # Get the classes
    classes = definition['classes']

    # Get the icons
    icons = get_icons(doc, definition)

    # Add a definition if correct
    if bool(classes) and bool(icons):

        # Get the images
        images = get_images(icons, get_size(definition))

        # Get the prefix
        prefix = get_prefix(definition)

        doc.defined.append({'classes' : set(classes), 'latex': latex_code(prefix, images)})

def main(doc = None):
    run_filter(tip, prepare = prepare, finalize = finalize, doc = doc)

if __name__ == '__main__':
    main()

