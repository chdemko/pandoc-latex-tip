# pandoc-latex-tip
[![Build Status](https://img.shields.io/travis/chdemko/pandoc-latex-tip.svg)](http://travis-ci.org/chdemko/pandoc-latex-tip)
[![Coveralls](https://img.shields.io/coveralls/chdemko/pandoc-latex-tip.svg)](https://coveralls.io/github/chdemko/pandoc-latex-tip)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/chdemko/pandoc-latex-tip.svg)](https://scrutinizer-ci.com/g/chdemko/pandoc-latex-tip/)
[![PyPI version](https://img.shields.io/pypi/v/pandoc-latex-tip.svg)](https://pypi.python.org/pypi/pandoc-latex-tip/)
[![License](https://img.shields.io/pypi/l/pandoc-latex-tip.svg)](http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html)
[![Downloads](https://img.shields.io/pypi/dm/pandoc-latex-tip.svg)](https://pypi.python.org/pypi/pandoc-latex-tip/)
[![Python version](https://img.shields.io/pypi/pyversions/pandoc-latex-tip.svg)](https://pypi.python.org/pypi/pandoc-latex-tip/)
[![Development Status](https://img.shields.io/pypi/status/pandoc-latex-tip.svg)](https://pypi.python.org/pypi/pandoc-latex-tip/)

*pandoc-latex-tip* is a [pandoc] filter for adding icon tooltips in the margin using the [Font-Awesome icons collection](http://fontawesome.io/).
It uses the *icon_font_to_png* package to generate on-fly images.

[pandoc]: http://pandoc.org/

Documentation
-------------

See the [wiki pages](https://github.com/chdemko/pandoc-latex-tip/wiki).

Usage
-----

To apply the filter, use the following option with pandoc:

    --filter pandoc-latex-tip

Installation
------------

*pandoc-latex-tip* requires [python], a programming language that comes pre-installed on linux and Mac OS X, and which is easily installed [on Windows]. Either python 2.7 or 3.x will do.

Install *pandoc-latex-tip* as root using the bash command

    pip install pandoc-latex-tip

To upgrade to the most recent release, use

    pip install --upgrade pandoc-latex-tip

To upgrade the Font-Awesome icons collection add the `--force` flag

    pip install --upgrade --force pandoc-latex-tip

`pip` is a script that downloads and installs modules from the Python Package Index, [PyPI].  It should come installed with your python distribution. If you are running linux, `pip` may be bundled separately. On a Debian-based system (including Ubuntu), you can install it as root using

    apt-get update
    apt-get install python-pip

Make sure you have required packages for [Pillow installation](https://pillow.readthedocs.org/en/3.1.x/installation.html). On linux you have to install some extra libraries **before** *pandoc-latex-tip*. On a Debian-based system (including Ubuntu), you can install it as root using

	apt-get build-dep python-imaging
	apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

[python]: https://www.python.org/pandoc-latex-tip
[on Windows]: https://www.python.org/downloads/windows/
[PyPI]: https://pypi.python.org/pypi


Getting Help
------------

If you have any difficulties with pandoc-latex-tip, please feel welcome to [file an issue] on github so that we can help.

[file an issue]: https://github.com/chdemko/pandoc-latex-tip/issues

