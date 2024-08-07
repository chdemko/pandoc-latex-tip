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

* Font-Awesome (4.7, 5.x)
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

The metadata block above is used to add a ``bug`` icon to ``span``,
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
   <https://fontawesome.com/>`__
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

Example
-------

Demonstration: Using
`pandoc-latex-tip-sample.txt <https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/develop/docs/images/pandoc-latex-tip-sample.txt>`__
as input gives output file in
`pdf <https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/develop/docs/images/pandoc-latex-tip-sample.pdf>`__.

Extensions
----------

``pandoc-latex-tip`` can be extended by adding additional ``css`` and
``ttf`` files.

Run ``pandoc-latex-tip`` for a complete explanation.

.. code-block:: shell

   $ pandoc-latex-tip

