"""
pandoc_latex_tip package.
"""

from ._app import app
from ._main import main


__all__ = ("main", "app")

if __name__ == "__main__":
    main()
