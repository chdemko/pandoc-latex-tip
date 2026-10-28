"""
Download the icons.
"""

import pathlib
import shutil
import sys
import urllib.error
import urllib.request

FONTAWESOME = "7.3.1"


def get_icons() -> None:
    """
    Download the icons.
    """
    get_fontawesome()


def get_fontawesome() -> None:
    """
    Get the fontawesome icons.
    """
    folder = get_folder("fontawesome")
    base = f"https://raw.githubusercontent.com/FortAwesome/Font-Awesome/{FONTAWESOME}/"
    for filename in ("fontawesome.css", "brands.css"):
        download(f"{base}css/{filename}", folder, filename)
    for filename in (
        "fa-brands-400.woff2",
        "fa-regular-400.woff2",
        "fa-solid-900.woff2",
    ):
        download(f"{base}webfonts/{filename}", folder, filename)


def download(url: str, folder: pathlib.Path, filename: str) -> None:
    """
    Download an url to a folder/filename.

    Arguments
    ---------
    url
        An url
    folder
        A folder
    filename
        A filename
    """
    print(f"Download '{url}' to {folder}/{filename}")  # noqa: T201
    try:
        with (
            urllib.request.urlopen(url) as response,  # noqa: S310
            pathlib.Path(folder, filename).open("wb") as out_file,
        ):
            shutil.copyfileobj(response, out_file)
    except urllib.error.HTTPError as exception:
        sys.stderr.write(str(exception))


def get_folder(collection: str) -> pathlib.Path:
    """
    Get a folder.

    Arguments
    ---------
    collection
        The collection name

    Returns
    -------
    pathlib.Path
        The folder
    """
    folder = pathlib.Path(
        "share",
        "pandoc_latex_tip",
        collection,
    )

    if not folder.exists():
        folder.mkdir(parents=True)

    return folder


if __name__ == "__main__":
    get_icons()
