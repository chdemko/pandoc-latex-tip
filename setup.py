"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/chdemko/pandoc-latex-tip
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path, makedirs

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

from distutils.command.build_py import build_py as _build_py
from distutils.command.build_ext import build_ext as _build_ext

def _post():
    import icon_font_to_png
    from pkg_resources import get_distribution
    from appdirs import AppDirs
    dirs = AppDirs('pandoc_latex_tip', version = get_distribution('pandoc_latex_tip').version)
    directory = dirs.user_data_dir
    if not path.exists(directory):
        makedirs(directory)
        downloader = icon_font_to_png.FontAwesomeDownloader(directory)
        downloader.css_url = 'https://cdn.rawgit.com/FortAwesome/Font-Awesome/v4.7.0/css/font-awesome.css'
        downloader.ttf_url = 'https://cdn.rawgit.com/FortAwesome/Font-Awesome/v4.7.0/fonts/fontawesome-webfont.ttf'
        downloader.download_files()

class build_py(_build_py):
    def run(self):
        _build_py.run(self)
        self.execute(_post, (), msg="Running post build task")

class build_ext(_build_ext):
    def run(self):
        _build_ext.run(self)
        self.execute(_post, (), msg="Running post build task")

setup(
    cmdclass={'build_py': build_py, 'build_ext': build_ext},
    name='pandoc-latex-tip',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.3.1',

    # The project's description
    description='A pandoc filter for adding tip in LaTeX',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/chdemko/pandoc-latex-tip',

    # The project's download page
    download_url = 'https://github.com/chdemko/pandoc-latex-tip/archive/master.zip',

    # Author details
    author='Christophe Demko',
    author_email='chdemko@gmail.com',

    # Maintainer details
    maintainer='Christophe Demko',
    maintainer_email='chdemko@gmail.com',

    # Choose your license
    license='BSD-3-Clause',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Specify the OS
        'Operating System :: OS Independent',
        
        # Indicate who your project is intended for
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Documentation',
        'Topic :: Text Processing :: Filters',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='pandoc filters latex tip Font-Awesome icon',

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    py_modules=["pandoc_latex_tip"],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'pandoc-latex-tip = pandoc_latex_tip:main',
        ],
    },
    
    
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        'panflute>=1.10',
        'icon_font_to_png>=0.4',
        'pillow>=4.3.0',
        'appdirs>=1.4.0',
        'pypandoc>=1.4'
    ],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # packages=find_packages(),
    # include_package_data = True,

    setup_requires=[
        'pytest-runner',
        'icon_font_to_png>=0.4',
        'appdirs>=1.4.0'
    ],
    tests_require=['pytest', 'coverage'],
)
