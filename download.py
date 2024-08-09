"""
Download the icons.
"""

import pathlib
import shutil
import sys
import urllib.error
import urllib.request


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
    download(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.6.0/"
        "css/fontawesome.css",
        folder,
        "fontawesome.css",
    )
    download(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.6.0/"
        "css/brands.css",
        folder,
        "brands.css",
    )
    download(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.6.0/"
        "webfonts/fa-brands-400.ttf",
        folder,
        "fa-brands-400.ttf",
    )
    download(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.6.0/"
        "webfonts/fa-regular-400.ttf",
        folder,
        "fa-regular-400.ttf",
    )
    download(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.6.0/"
        "webfonts/fa-solid-900.ttf",
        folder,
        "fa-solid-900.ttf",
    )


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
    print(f"Download '{url}' to {folder}/{filename}")
    try:
        with urllib.request.urlopen(url) as response, pathlib.Path(
            folder, filename
        ).open("wb") as out_file:
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
