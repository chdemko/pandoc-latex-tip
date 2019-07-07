"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/chdemko/pandoc-latex-tip
"""

# pylint: disable=bad-continuation

# To use a consistent encoding
import codecs
import os
import re

# pylint: disable=no-name-in-module,import-error
from distutils.version import LooseVersion

from pkg_resources import get_distribution

# Always prefer setuptools over distutils
from setuptools import setup
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py

HERE = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc

    LONG_DESCRIPTION = pypandoc.convert("README.md", "rst")
except (IOError, ImportError):
    with codecs.open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()


# pylint: disable=too-many-locals,too-many-branches,too-many-statements
def _post():
    _post_fontawesome_47()
    _post_fontawesome_5x()
    _post_glyphicons_33()
    _post_material_design_3x()


def _post_fontawesome_47():
    # fontawesome 4.7
    directory = _directory("fontawesome", "4.7")
    _download(
        "https://cdn.jsdelivr.net/gh/FortAwesome/Font-Awesome@v4.7.0/css/font-awesome.css",
        directory,
        "font-awesome.css",
    )
    _download(
        "https://cdn.jsdelivr.net/gh/FortAwesome/Font-Awesome@v4.7.0/fonts/fontawesome-webfont.ttf",
        directory,
        "fontawesome-webfont.ttf",
    )


def _post_fontawesome_5x():
    # fontawesome 5.x
    directory = _directory("fontawesome", "5.x")

    versions = _versions(
        "https://api.github.com/repos/FortAwesome/Font-Awesome/tags",
        "Unable to get the last version number of the Font-Awesome package on github\n",
    )

    latest = _latest("^5.", versions, "5.9.0")

    _download(
        "https://cdn.jsdelivr.net/gh/FortAwesome/Font-Awesome@"
        + latest
        + "/css/fontawesome.css",
        directory,
        "fontawesome.css",
    )
    for ttf in ["fa-brands-400", "fa-regular-400", "fa-solid-900"]:
        _download(
            "https://cdn.jsdelivr.net/gh/FortAwesome/Font-Awesome@"
            + latest
            + "/webfonts/"
            + ttf
            + ".ttf",
            directory,
            ttf + ".ttf",
        )


def _post_glyphicons_33():
    # glyphicons 3.3
    directory = _directory("glyphicons", "3.3")

    _download(
        "https://cdn.jsdelivr.net/gh/twbs/bootstrap@v3.3.7/dist/css/bootstrap.css",
        directory,
        "bootstrap.css",
    )

    _download(
        "https://cdn.jsdelivr.net/gh/twbs/bootstrap@v3.3.7/dist/fonts/glyphicons-halflings-regular.ttf",
        directory,
        "glyphicons-halflings-regular.ttf",
    )

    original = open(os.path.join(directory, "bootstrap.css"), "rt")
    modified = open(os.path.join(directory, "bootstrap-modified.css"), "w")
    index = 0
    for line in original:
        if index >= 1067:
            break
        elif index >= 280:
            modified.write(line)
        index = index + 1
    original.close()
    modified.close()


def _post_material_design_3x():
    # material design 3.x
    directory = _directory("materialdesign", "3.x")

    versions = _versions(
        "https://api.github.com/repos/Templarian/MaterialDesign-Webfont/tags",
        "Unable to get the last version number of the MaterialDesign-Webfont package on github\n",
    )

    latest = _latest("^v3.", versions, "v3.7.95")

    _download(
        "https://cdn.jsdelivr.net/gh/Templarian/MaterialDesign-Webfont@"
        + latest
        + "/css/materialdesignicons.css",
        directory,
        "materialdesignicons.css",
    )

    _download(
        "https://cdn.jsdelivr.net/gh/Templarian/MaterialDesign-Webfont@"
        + latest
        + "/fonts/materialdesignicons-webfont.ttf",
        directory,
        "materialdesignicons-webfont.ttf",
    )


def _download(url, directory, filename):
    import urllib
    import shutil
    import sys

    try:
        with urllib.request.urlopen(url) as response, open(
            os.path.join(directory, filename), "wb"
        ) as out_file:
            shutil.copyfileobj(response, out_file)
    except urllib.error.HTTPError as exception:
        sys.stderr.write(str(exception))


def _latest(match, versions, latest):
    try:
        for version in versions:
            if re.match(match, version["name"]) and LooseVersion(
                version["name"]
            ) > LooseVersion(latest):
                latest = version["name"]
    except TypeError:
        pass
    return latest


def _directory(collection, version):
    import appdirs

    dirs = appdirs.AppDirs(
        os.path.join(
            "pandoc_latex_tip",
            get_distribution("pandoc_latex_tip").version,
            collection,
            version,
        )
    )
    directory = dirs.user_data_dir
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def _versions(url, message):
    import requests
    import sys

    try:
        return requests.get(url).json()
    except ValueError:
        sys.stderr.write(message)
        return []


class BuildPy(build_py):
    def run(self):
        super().run()
        self.execute(_post, (), msg="Running post build task")


class BuildExt(build_ext):
    def run(self):
        super().run()
        self.execute(_post, (), msg="Running post build task")


setup(
    cmdclass={"build_py": BuildPy, "build_ext": BuildExt},
    name="pandoc-latex-tip",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version="2.1.2",
    # The project's description
    description="A pandoc filter for adding tip in LaTeX",
    long_description=LONG_DESCRIPTION,
    # The project's main homepage.
    url="https://github.com/chdemko/pandoc-latex-tip",
    # The project's download page
    download_url="https://github.com/chdemko/pandoc-latex-tip/archive/develop.zip",
    # Author details
    author="Christophe Demko",
    author_email="chdemko@gmail.com",
    # Maintainer details
    maintainer="Christophe Demko",
    maintainer_email="chdemko@gmail.com",
    # Choose your license
    license="BSD-3-Clause",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Specify the OS
        "Operating System :: OS Independent",
        # Indicate who your project is intended for
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Filters",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 3.6",
    ],
    # What does your project relate to?
    keywords="pandoc filters latex tip Font-Awesome icon",
    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    py_modules=["pandoc_latex_tip"],
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": ["pandoc-latex-tip = pandoc_latex_tip:main"]},
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "panflute>=1.10",
        "icon_font_to_png>=0.4",
        "pillow>=5.2",
        "appdirs>=1.4",
        "pypandoc>=1.4",
        "requests>=2",
    ],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={"dev": ["check-manifest"], "test": ["tox"]},
    # packages=find_packages(),
    # include_package_data = True,
    setup_requires=["pytest-runner", "icon_font_to_png>=0.4", "appdirs>=1.4"],
    tests_require=["pytest"],
)
