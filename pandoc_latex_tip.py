#!/usr/bin/env python

"""
Pandoc filter for adding tip in LaTeX
"""

from pandocfilters import RawInline, Span, stringify

import io
import os
import sys
import codecs
import json
import re

try:
    FileNotFoundError
except NameError:
    #py2
    FileNotFoundError = IOError

def toJSONFilters(actions):
    """Converts a list of actions into a filter that reads a JSON-formatted
    pandoc document from stdin, transforms it by walking the tree
    with the actions, and returns a new JSON-formatted pandoc document
    to stdout.  The argument is a list of functions action(key, value, format, meta),
    where key is the type of the pandoc object (e.g. 'Str', 'Para'),
    value is the contents of the object (e.g. a string for 'Str',
    a list of inline elements for 'Para'), format is the target
    output format (which will be taken for the first command line
    argument if present), and meta is the document's metadata.
    If the function returns None, the object to which it applies
    will remain unchanged.  If it returns an object, the object will
    be replaced.    If it returns a list, the list will be spliced in to
    the list to which the target object belongs.    (So, returning an
    empty list deletes the object.)
    """
    try:
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    except AttributeError:
        # Python 2 does not have sys.stdin.buffer.
        # REF: http://stackoverflow.com/questions/2467928/python-unicodeencodeerror-when-reading-from-stdin
        input_stream = codecs.getreader("utf-8")(sys.stdin)

    doc = json.loads(input_stream.read())
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    if 'meta' in doc:
        meta = doc['meta']
    elif doc[0]:  # old API
        meta = doc[0]['unMeta']
    else:
        meta = {}

    from functools import reduce
    altered = reduce(lambda x, action: walk(x, action, format, meta), actions, doc)
    json.dump(altered, sys.stdout)

def walk(x, action, format, meta):
    """Walk a tree, applying an action to every object.
    Returns a modified tree.
    """
    if isinstance(x, list):
        array = []
        for item in x:
            if isinstance(item, dict) and 't' in item:
                res = action(item['t'], item['c'] if 'c' in item else None, format, meta)
                if res is None:
                    array.append(walk(item, action, format, meta))
                elif isinstance(res, list):
                    for z in res:
                        array.append(walk(z, action, format, meta))
                else:
                    array.append(walk(res, action, format, meta))
            else:
                array.append(walk(item, action, format, meta))
        return array
    elif isinstance(x, dict):
        for k in x:
            x[k] = walk(x[k], action, format, meta)
        return x
    else:
        return x

def tip(key, value, format, meta):
    # Is it a Span and the right format?
    if key == 'Span' and format == 'latex':

        # Get the attributes
        [[id, classes, properties], content] = value

        # Use the Span classes as a set
        currentClasses = set(classes)

        # Loop on all tip definition
        for elt in getDefined(meta):

            # Is the classes correct?
            if currentClasses >= elt['classes']:

                # Prepend a tex block for inserting images
                return [Span([id, classes, properties], content), RawInline('tex', elt['latex'])]

def getIconFont():
    if not hasattr(getIconFont, 'value'):
        import icon_font_to_png
        getIconFont.value = icon_font_to_png.IconFont(
            os.path.dirname(os.path.realpath(__file__)) + '/pandoc_latex_tip-data/font-awesome.css',
            os.path.dirname(os.path.realpath(__file__)) + '/pandoc_latex_tip-data/fontawesome-webfont.ttf'
        )
    return getIconFont.value

def getDefined(meta):
    if not hasattr(getDefined, 'value'):
        # Prepare the values
        getDefined.value = []

        # Get the meta data
        if 'pandoc-latex-tip' in meta and meta['pandoc-latex-tip']['t'] == 'MetaList':
            tipMeta = meta['pandoc-latex-tip']['c']

            # Loop on all definitions
            for definition in tipMeta:

                # Verify the definition type
                if definition['t'] == 'MetaMap':

                     # Get the classes
                    classes = []
                    if 'classes' in definition['c'] and definition['c']['classes']['t'] == 'MetaList':
                        for klass in definition['c']['classes']['c']:
                            classes.append(stringify(klass))

                    # Get the icons
                    icons = [{'name': 'exclamation-circle', 'color': 'black'}]

                    # Test the icons definition
                    if 'icons' in definition['c'] and definition['c']['icons']['t'] == 'MetaList':
                        icons = []
                        for icon in definition['c']['icons']['c']:
                            if icon['t'] == 'MetaInlines':
                                # Simple icon
                                color = 'black'
                                name = stringify(icon['c'])
                            elif icon['t'] == 'MetaMap' and 'color' in icon['c'] and 'name' in icon['c']:
                                # Complex icon with name and color
                                color = stringify(icon['c']['color'])
                                name = stringify(icon['c']['name'])
                            else:
                                # Bad formed icon
                                break

                            # Lower the color
                            lowerColor = color.lower()

                            # Convert the color to black if unexisting
                            from PIL import ImageColor
                            if lowerColor not in ImageColor.colormap:
                                lowerColor = 'black'

                            # Is the icon correct?
                            try:
                                if name in getIconFont().css_icons:
                                    icons.append({'name': name, 'color': lowerColor})
                            except FileNotFoundError:
                                pass

                    # Add a definition if correct
                    if bool(classes) and bool(icons):

                        # Generate the LaTeX image code
                        images = []

                       # Get the size
                        size = '18'
                        if 'size' in definition['c'] and definition['c']['size']['t'] == 'MetaString':
                            try:
                                intValue = int(definition['c']['size']['c'])
                                if intValue > 0:
                                    size = str(intValue)
                            except ValueError:
                                pass

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
                                    getIconFont().export_icon(
                                        icon['name'],
                                        size = 512,
                                        color = icon['color'],
                                        export_dir = dirs.user_cache_dir + '/' + icon['color']
                                    )

                                # Add the LaTeX image
                                images.append('\\includegraphics[width=' + size + 'pt]{' + image + '}')
                            except FileNotFoundError:
                                pass

                        # Get the prefix
                        prefix = '\\reversemarginpar'

                        if 'position' in definition['c'] and\
                            definition['c']['position']['t'] == 'MetaInlines' and\
                            stringify(definition['c']['position']['c']) == 'right':

                            prefix = '\\normalmarginpar'

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
                            '}',
                        ]

                        getDefined.value.append({'classes' : set(classes), 'latex': '\n'.join(latex)})

        if 'header-includes' not in meta:
            meta['header-includes'] = {u'c': [], u't': u'MetaList'}

        meta['header-includes']['c'].append({
            'c': [{'t': 'RawInline', 'c': ['tex', '\\usepackage{graphicx,grffile}']}],
            't': 'MetaInlines'
        })
        meta['header-includes']['c'].append({
            'c': [{'t': 'RawInline', 'c': ['tex', '\\usepackage{marginnote}']}],
            't': 'MetaInlines'
        })
        meta['header-includes']['c'].append({
            'c': [{'t': 'RawInline', 'c': ['tex', '\\usepackage{etoolbox}']}],
            't': 'MetaInlines'
        })

    return getDefined.value

def main():
    toJSONFilters([tip])

if __name__ == '__main__':
    main()

