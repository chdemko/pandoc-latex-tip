Usage
=====

To apply the filter, use the following option with pandoc:

.. code-block:: shell

   $ pandoc --filter pandoc-latex-tip

Explanation
-----------

In the metadata block, specific set of classes can be defined to
decorate HTML ``span``, ``div``, ``code`` or ``codeblock`` elements by
icons generated from popular icon collections:

* Font-Awesome
  `Dave Gandy <https://fontawesome.com/>`__
  (`SIL OFL 1.1 <https://fontawesome.com/license/>`__)

It’s also possible to specify a tip on such an element using description
by attribute.

The metadata block add information using the ``pandoc-latex-tip`` entry
by a list of definitions:

.. code-block:: yaml

   pandoc-latex-tip:
     - classes: [tip, error]
       icons: [fa-bug]
     - classes: [tip]

The metadata block above is used to add a ``fa-bug`` icon to ``span``,
``div``, ``code`` or ``codeblock`` elements which have ``tip`` and
``error`` classes and a generic icon to ``span``, ``div``, ``code`` or
``codeblock`` elements that have only a ``tip`` class.

Each entry of ``pandoc-latex-tip`` is a YAML dictionary containing:

-  ``classes``: the set of classes of the ``span``, ``div``, ``code`` or
   ``codeblock`` elements to which the transformation will be applied.
   This parameter is mandatory.
-  ``icons``: the list of icons that will decorate the ``span``,
   ``div``, ``code`` or ``codeblock`` elements (``[fa-exclamation-circle]``
   by default)
-  ``size``: the size of the rendered icons (``18`` by default)
-  ``position``: the position of the icons (``left`` by default or
   ``right`` or ``inner`` or ``outer``)
-  ``color``: the default color for icons which do not have a color
   description by themselves

Each icon is either:

-  an icon name taken from the `Font-Awesome icons collection
   <https://fontawesome.com/>`__ (use ``fa-`` prefix for the ``solid``
   `icons <https://fontawesome.com/search?o=r&m=free&s=solid>`__,
   ``far-`` prefix for the ``regular``
   `icons <https://fontawesome.com/search?o=r&m=free&s=regular>`__
   and ``fab-`` prefix for the ``brands``
   `icons <https://fontawesome.com/search?o=r&m=free&f=brands>`__)
-  a YAML object containing

   -  a ``name`` property (for the icon)
   -  a ``color`` property taken from the `X11 color
      collection <https://www.w3.org/TR/css3-color/#svg-color>`__
   -  a ``link`` property to make the icon clickable

If only an icon name is specified (in this case, you can simply put its
name instead of inserting it in a list), the color is assumed to be
``Black``.

It’s also possible to specify a tip for individual elements using
attribute description:

-  ``latex-tip-icon``: the name of the icon
-  ``latex-tip-size``: the size of the rendered icon (``18`` by default)
-  ``latex-tip-position``: the position of the icon (``left`` by default
   or ``right`` or ``inner`` or ``outer``)
-  ``latex-tip-color``: the color for the icon (``black`` by default)
-  ``latex-tip-link``: a link for the clickable icon

The following LaTeX packages are required:

-  ``marginnote``
-  ``etoolbox``
-  ``changepage``

Extensions
----------

``pandoc-latex-tip`` can be extended by adding collections of
``CSS`` and ``TTF`` files.

Run ``pandoc-latex-tip`` for a complete explanation.

..  code-block:: shell

    $ pandoc-latex-tip
    pandoc-latex-tip filter (version number)

    Usage:
      command [options] [arguments]

    Options:
      -h, --help            Display help for the given command. When no command
    is given display help for the list command.
      -q, --quiet           Do not output any message.
      -V, --version         Display this application version.
          --ansi            Force ANSI output.
          --no-ansi         Disable ANSI output.
      -n, --no-interaction  Do not ask any interactive question.
      -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal ou
    tput, 2 for more verbose output and 3 for debug.

    Available commands:
      beamer              Run pandoc filter for Beamer document
      collections         List the collections
      help                Displays help for a command.
      icons               List the set of icons
      latex               Run pandoc filter for LaTeX document
      list                Lists commands.

     collections
      collections add     Add a file to a collection
      collections delete  Delete a collection
      collections info    Display a collection

     icons
      icons add           Add a set of icons from a collection
      icons delete        Delete a set of icons

Example
-------

Demonstration: Using
`pandoc-latex-tip-sample.txt <https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/develop/docs/images/pandoc-latex-tip-sample.txt>`__
as input gives output file in
`pdf <https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/develop/docs/images/pandoc-latex-tip-sample.pdf>`__.

..  code-block:: shell

    $ pandoc --filter pandoc-latex-tip pandoc-latex-tip-sample.txt \
    >    -o pandoc-latex-tip-sample.pdf
    [WARNING] pandoc-latex-tip: mdi-account is not a correct icon name
    [WARNING] Could not fetch resource unexisting.png: replacing image with description
    $ pandoc-latex-tip icons
    - collection: fontawesome
      CSS: fontawesome.css
      TTF: fa-solid-900.ttf
      prefix: fa-
    - collection: fontawesome
      CSS: fontawesome.css
      TTF: fa-regular-400.ttf
      prefix: far-
    - collection: fontawesome
      CSS: brands.css
      TTF: fa-brands-400.ttf
      prefix: fab-
    $ wget https://github.com/Templarian/MaterialDesign-Webfont/raw/v7.4.47/\
    > css/materialdesignicons.css
    $ wget https://github.com/Templarian/MaterialDesign-Webfont/raw/v7.4.47/\
    > fonts/materialdesignicons-webfont.ttf
    $ pandoc-latex-tip collections add materialdesign materialdesignicons.css
    Add file 'materialdesignicons.css' to collection 'materialdesign'
    $ pandoc-latex-tip collections add materialdesign materialdesignicons-webfont.ttf
    Add file 'materialdesignicons-webfont.ttf' to collection 'materialdesign'
    $ pandoc-latex-tip icons add \
    >     --CSS materialdesignicons.css \
    >     --TTF materialdesignicons-webfont.ttf \
    >     --prefix mdi- \
    >     materialdesign
    $ pandoc-latex-tip icons
    - collection: fontawesome
      CSS: fontawesome.css
      TTF: fa-solid-900.ttf
      prefix: fa-
    - collection: fontawesome
      CSS: fontawesome.css
      TTF: fa-regular-400.ttf
      prefix: far-
    - collection: fontawesome
      CSS: brands.css
      TTF: fa-brands-400.ttf
      prefix: fab-
    - collection: materialdesign
      CSS: materialdesignicons.css
      TTF: materialdesignicons-webfont.ttf
      prefix: mdi-
    $ pandoc --filter pandoc-latex-tip pandoc-latex-tip-sample.txt \
    >     -o pandoc-latex-tip-sample.pdf
    2 extra bytes in post.stringData array
    [WARNING] Could not fetch resource unexisting.png: replacing image with description




