"""
pandoc_latex_tip package.
"""

from ._app import app  # noqa: TID252
from ._main import main  # noqa: TID252

__all__ = ("main", "app")

if __name__ == "__main__":
    main()
