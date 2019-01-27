.. pandoc-numbering documentation master file, created by
   sphinx-quickstart on Mon Dec 17 11:33:59 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pandoc-numbering's documentation!
============================================

Explanation
-----------

In the metadata block, specific set of classes can be defined to
decorate HTML ``span``, ``div``, ``code`` or ``codeblock`` elements by
icons generated from popular icon collections:

+-----------------+----------+----------------------------------------------------------------+------------------------------------------------------------------------------------+
| Collection      | Version  | Author                                                         | License                                                                            |
+=================+==========+================================================================+====================================================================================+
| Font-Awesome    | 4.7, 5.x | `Dave Gandy <https://fontawesome.com/>`__                      | `SIL OFL 1.1 <https://fontawesome.com/license/>`__                                 |
+-----------------+----------+----------------------------------------------------------------+------------------------------------------------------------------------------------+
| Glyphicons      | 3.3      | `Jan Kovarik <https://glyphicons.com/>`__                      | `MIT <https://github.com/twbs/bootstrap/blob/v3.3.7/LICENSE>`__                    |
+-----------------+----------+----------------------------------------------------------------+------------------------------------------------------------------------------------+
| Material Design | 2.x      | `Austin Andrews & Google <https://materialdesignicons.com/>`__ | `SIL OFL 1.1 <https://github.com/Templarian/MaterialDesign/blob/master/LICENSE>`__ +
+-----------------+----------+----------------------------------------------------------------+------------------------------------------------------------------------------------+

It’s also possible to specify a tip on such an element using description
by attribute.

The metadata block add information using the ``pandoc-latex-tip`` entry
by a list of definitions:

.. code:: yaml

   pandoc-latex-tip:
     - classes: [tip, error]
       icons: [bug]
     - classes: [tip]

The metadata block above is used to add a ``bug`` icon to ``span``,
``div``, ``code`` or ``codeblock`` elements which have ``tip`` and
``error`` classes and a generic icon to ``span``, ``div``, ``code`` or
``codeblock`` elements that have only a ``tip`` class.

Each entry of ``pandoc-latex-tip`` is a YAML dictionary containing:

-  ``classes``: the set of classes of the ``span``, ``div``, ``code`` or
   ``codeblock`` elements to which the transformation will be applied.
   This parameter is mandatory.
-  ``icons``: the list of icons that will decorate the ``span``,
   ``div``, ``code`` or ``codeblock`` elements (``[exclamation-circle]``
   by default)
-  ``size``: the size of the rendered icons (``18`` by default)
-  ``position``: the position of the icons (``left`` by default or
   ``right``)
-  ``color``: the default color for icons which do not have a color
   description by themselves

Each icon is either:

-  an icon name taken from the `Font-Awesome icons collection
   4.7.0 <https://fontawesome.com/v4.7.0/>`__
-  a YAML object containing

   -  a ``name`` property (for the icon)
   -  a ``color`` property taken from the `X11 color
      collection <https://www.w3.org/TR/css3-color/#svg-color>`__
   -  an icon ``collection`` property (either ``fontawesome``,
      ``glyphicons`` or ``materialdesign``)
   -  an icon collection ``version`` property (``4.7`` or ``5.x`` for
      ``fontawesome``, ``3.3`` for ``glyphicons`` and ``2.x`` for
      ``materialdesign``)
   -  an icon collection ``variant`` property (Font-Awesome ``5.x``
      version define 3 variants ``brands``, ``regular``, ``solid``)
   -  a ``link`` property to make the icon clickable

If only an icon name is specified (in this case, you can simply put its
name instead of inserting it in a list), the color is assumed to be
``Black``, the version is assumed to be ``4.7`` and the variant is
assumed to be ``regular``.

It’s also possible to specify a tip for individual elements using
attribute description:

-  ``latex-tip-icon``: the name of the icon
-  ``latex-tip-size``: the size of the rendered icon (``18`` by default)
-  ``latex-tip-position``: the position of the icon (``left`` by default
   or ``right``)
-  ``latex-tip-color``: the color for the icon (``black`` by default)
-  ``latex-tip-name``: the collection name property (``fontawesome``
   by default)
-  ``latex-tip-version``: the collection version property (``4.7``
   by default)
-  ``latex-tip-variant``: the collection variant property
   (``regular`` by default)
-  ``latex-tip-link``: a link for the clickable icon

The following LaTeX packages are required:

-  ``marginnote``
-  ``etoolbox``

Example
-------

Demonstration: Using
`pandoc-latex-tip-sample.txt <https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/2.0.2/docs/images/pandoc-latex-tip-sample.txt>`__
as input gives output file in
`pdf <https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/2.0.2/docs/images/pandoc-latex-tip-sample.pdf>`__.

