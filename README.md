Installation
============

[![Python package](https://github.com/chdemko/pandoc-latex-tip/workflows/Python%20package/badge.svg?branch=develop)](https://github.com/chdemko/pandoc-latex-tip/actions/workflows/python-package.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)
[![Coveralls](https://img.shields.io/coveralls/github/chdemko/pandoc-latex-tip/develop.svg?logo=Codecov&logoColor=white)](https://coveralls.io/github/chdemko/pandoc-latex-tip?branch=develop)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/chdemko/pandoc-latex-tip.svg?logo=scrutinizer)](https://scrutinizer-ci.com/g/chdemko/pandoc-latex-tip/)
[![Code Climate](https://codeclimate.com/github/chdemko/pandoc-latex-tip/badges/gpa.svg)](https://codeclimate.com/github/chdemko/pandoc-latex-tip/)
[![CodeFactor](https://img.shields.io/codefactor/grade/github/chdemko/pandoc-latex-tip/develop.svg?logo=codefactor)](https://www.codefactor.io/repository/github/chdemko/pandoc-latex-tip)
[![Codacy](https://img.shields.io/codacy/grade/de425638e13b4ceab3bfad1c4557aa6c.svg?logo=codacy&logoColor=white)](https://app.codacy.com/gh/chdemko/pandoc-latex-tip/dashboard)
[![PyPI version](https://img.shields.io/pypi/v/pandoc-latex-tip.svg?logo=pypi&logoColor=white)](https://pypi.org/project/pandoc-latex-tip/)
[![PyPI format](https://img.shields.io/pypi/format/pandoc-latex-tip.svg?logo=pypi&logoColor=white)](https://pypi.org/project/pandoc-latex-tip/)
[![License](https://img.shields.io/pypi/l/pandoc-latex-tip.svg?logo=pypi&logoColor=white)](https://raw.githubusercontent.com/chdemko/pandoc-latex-tip/develop/LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/pandoc-latex-tip?logo=pypi&logoColor=white)](https://pepy.tech/project/pandoc-latex-tip)
[![Development Status](https://img.shields.io/pypi/status/pandoc-latex-tip.svg?logo=pypi&logoColor=white)](https://pypi.org/project/pandoc-numbering/)
[![Python version](https://img.shields.io/pypi/pyversions/pandoc-latex-tip.svg?logo=Python&logoColor=white)](https://pypi.org/project/pandoc-latex-tip/)
[![Poetry version](https://img.shields.io/badge/poetry-1.5%20|%201.6%20|%201.7%20|%201.8-blue.svg?logo=poetry)](https://python-poetry.org/)
[![Pandoc version](https://img.shields.io/badge/pandoc-2.11%20|%202.12%20|%202.13%20|%202.14%20|%202.15%20|%202.16%20|%202.17%20|%202.18%20|%202.19%20|%203.0%20|%203.1%20|%203.2%20|%203.3-blue.svg?logo=markdown)](https://pandoc.org/)
[![Latest release](https://img.shields.io/github/release-date/chdemko/pandoc-latex-tip.svg?logo=github)](https://github.com/chdemko/pandoc-latex-tip/releases)
[![Last commit](https://img.shields.io/github/last-commit/chdemko/pandoc-latex-tip/develop?logo=github)](https://github.com/chdemko/pandoc-latex-tip/commit/develop/)
[![Repo Size](https://img.shields.io/github/repo-size/chdemko/pandoc-latex-tip.svg?logo=github)](http://pandoc-latex-tip.readthedocs.io/en/latest/)
[![Code Size](https://img.shields.io/github/languages/code-size/chdemko/pandoc-latex-tip.svg?logo=github)](http://pandoc-latex-tip.readthedocs.io/en/latest/)
[![Source Rank](https://img.shields.io/librariesio/sourcerank/pypi/pandoc-latex-tip.svg?logo=libraries.io&logoColor=white)](https://libraries.io/pypi/pandoc-latex-tip)
[![Docs](https://img.shields.io/readthedocs/pandoc-latex-tip.svg?logo=read-the-docs&logoColor=white)](http://pandoc-latex-tip.readthedocs.io/en/latest/)

![Standard conversion](https://github.com/chdemko/pandoc-latex-tip/blob/develop/docs/images/help.png?raw=true)

*pandoc-latex-tip*, designed to used in conjuction with
[*pandoc-latex-admonition*](https://github.com/chdemko/pandoc-latex-admonition),
is a [pandoc] filter for adding icon tooltips in the margin
using popular icon collections.

[pandoc]: http://pandoc.org/

Instructions
------------

*pandoc-latex-tip* requires [python], a programming language that comes
pre-installed on linux and Mac OS X, and which is easily installed
[on Windows].

Install *pandoc-latex-tip* using the bash command

~~~{prompt} bash
pipx install pandoc-latex-tip
~~~

To upgrade to the most recent release, use

~~~{prompt} bash
pipx upgrade pandoc-latex-tip
~~~

`pipx` is a script to install and run python applications in isolated
environments from the Python Package Index, [PyPI]. It can be installed
using instructions given [here](https://pipx.pypa.io/stable/).

Make sure you have required packages for
[Pillow installation](https://pillow.readthedocs.io/en/stable/installation/index.html).
On linux you have to install some extra libraries
**before** *pandoc-latex-tip*.  On a Debian-based system (including Ubuntu),
you can install it as root using

~~~{prompt} bash
sudo apt-get install python3-pil
~~~

[python]: https://www.python.org
[on Windows]: https://www.python.org/downloads/windows
[PyPI]: https://pypi.org


Getting Help
------------

If you have any difficulties with pandoc-latex-tip, please feel welcome to
[file an issue] on github so that we can help.

[file an issue]: https://github.com/chdemko/pandoc-latex-tip/issues

Contribute
==========

Instructions
------------

Install `poetry`, then run

~~~{prompt} bash
poetry self add poeblix
poetry self add "poetry-dynamic-versioning[plugin]"
poetry install
poetry shell
poetry run python download.py
poetry blixbuild
poetry run pip install \
   dist/pandoc_latex_tip-`poetry version -s`-py3-none-any.whl
poetry shell
~~~

And submit your changes. When you commit, hooks will be executed
to check your code.

