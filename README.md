# pandoc-latex-tip
[![Build Status](https://img.shields.io/travis/chdemko/pandoc-latex-tip/1.5.0.svg)](https://travis-ci.org/chdemko/pandoc-latex-tip/branches)
[![Coveralls](https://img.shields.io/coveralls/github/chdemko/pandoc-latex-tip/1.5.0.svg)](https://coveralls.io/github/chdemko/pandoc-latex-tip?branch=1.5.0)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/chdemko/pandoc-latex-tip.svg)](https://scrutinizer-ci.com/g/chdemko/pandoc-latex-tip/)
[![PyPI version](https://img.shields.io/pypi/v/pandoc-latex-tip.svg)](https://pypi.org/project/pandoc-latex-tip/)
[![PyPI format](https://img.shields.io/pypi/format/pandoc-latex-tip/1.5.0.svg)](https://pypi.org/project/pandoc-latex-tip/1.5.0/)
[![License](https://img.shields.io/pypi/l/pandoc-latex-tip/1.5.0.svg)](https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/1.5.0/LICENSE)
[![Python version](https://img.shields.io/pypi/pyversions/pandoc-latex-tip.svg)](https://pypi.org/project/pandoc-latex-tip/)
[![Development Status](https://img.shields.io/pypi/status/pandoc-latex-tip.svg)](https://pypi.org/project/pandoc-latex-tip/)

*pandoc-latex-tip* is a [pandoc] filter for adding icon tooltips in the margin using popular icon collections:

Collection name | Versions  | Author                                                          | License
--------------- | ----------|-----------------------------------------------------------------|--------
Font-Awesome    | 4.7, 5.0  |[Dave Gandy - https://fontawesome.com/](https://fontawesome.com/)|[SIL OFL 1.1](https://fontawesome.com/license/)
Glyphicons      | 3.3       |[Jan Kovarik - https://glyphicons.com/](https://glyphicons.com/) |[MIT](https://github.com/twbs/bootstrap/blob/v3.3.7/LICENSE)
Material Design | 2.4       |[Austin Andrews & Google - https://materialdesignicons.com/](https://materialdesignicons.com/) |[SIL OFL 1.1](https://github.com/Templarian/MaterialDesign/blob/master/LICENSE)

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

To upgrade the icon collections add the `--force` and `--no-cache` flags

    pip install --upgrade --force --no-cache pandoc-latex-tip

To upgrade to the current code, use

    pip install --upgrade --force --no-cache git+https://github.com/chdemko/pandoc-latex-tip

`pip` is a script that downloads and installs modules from the Python Package Index, [PyPI].  It should come installed with your python distribution. If you are running linux, `pip` may be bundled separately. On a Debian-based system (including Ubuntu), you can install it as root using

    apt-get update
    apt-get install python-pip

Make sure you have required packages for [Pillow installation](https://pillow.readthedocs.org/en/3.1.x/installation.html). On linux you have to install some extra libraries **before** *pandoc-latex-tip*. On a Debian-based system (including Ubuntu), you can install it as root using

	apt-get build-dep python-imaging
	apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

[python]: https://www.python.org
[on Windows]: https://www.python.org/downloads/windows
[PyPI]: https://pypi.org


Getting Help
------------

If you have any difficulties with pandoc-latex-tip, please feel welcome to [file an issue] on github so that we can help.

[file an issue]: https://github.com/chdemko/pandoc-latex-tip/issues

