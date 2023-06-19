"""
download the icons.
"""

import contextlib
import os
import pathlib
import re
import shutil
import sys
import urllib.error
import urllib.request

from packaging.version import Version

import requests


def get_icons():
    """
    Download the icons.
    """
    get_fontawesome_47()
    get_fontawesome_5x()
    get_glyphicons_33()
    get_material_design_3x()


def get_fontawesome_47():
    """
    Download the fontawesome 4.7 icons.
    """
    # fontawesome 4.7
    folder = get_folder("fontawesome", "4.7")
    download(
        "https://raw.githubusercontent.com/FortAwesome/"
        "Font-Awesome/v4.7.0/css/font-awesome.css",
        folder,
        "font-awesome.css",
    )
    download(
        "https://github.com/FortAwesome/Font-Awesome/"
        "blob/v4.7.0/fonts/fontawesome-webfont.ttf?raw=true",
        folder,
        "fontawesome-webfont.ttf",
    )


def get_fontawesome_5x():
    """
    Download the fontawesome 5.x icons.
    """
    # fontawesome 5.x
    folder = get_folder("fontawesome", "5.x")

    versions = get_versions(
        "https://api.github.com/repos/FortAwesome/Font-Awesome/tags",
        "Unable to get the last version number of the Font-Awesome package on github\n",
    )

    latest = get_latest("^5.", versions, "5.14.0")

    download(
        "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/"
        + latest
        + "/css/fontawesome.css",
        folder,
        "fontawesome.css",
    )
    for ttf in ("fa-brands-400", "fa-regular-400", "fa-solid-900"):
        download(
            "https://github.com/FortAwesome/Font-Awesome/blob/"
            + latest
            + "/webfonts/"
            + ttf
            + ".ttf?raw=true",
            folder,
            ttf + ".ttf",
        )


def get_glyphicons_33():
    """
    Download the glyphicons 3.3 icons.
    """
    # glyphicons 3.3
    folder = get_folder("glyphicons", "3.3")

    download(
        "https://github.com/twbs/bootstrap/raw/v3.3.7/dist/css/bootstrap.css",
        folder,
        "bootstrap.css",
    )

    download(
        "https://github.com/twbs/bootstrap/"
        "blob/v3.3.7/dist/fonts/glyphicons-halflings-regular.ttf?raw=true",
        folder,
        "glyphicons-halflings-regular.ttf",
    )

    with open(
        os.path.join(folder, "bootstrap.css"), "rt", encoding="utf-8"
    ) as original, open(
        os.path.join(folder, "bootstrap-modified.css"), "w", encoding="utf-8"
    ) as modified:
        index = 0
        for line in original:
            if index >= 1067:
                break
            if index >= 280:
                modified.write(line)
            index = index + 1
        original.close()
        modified.close()


def get_material_design_3x():
    """
    Download the material design 3.x icons.
    """
    # material design 3.x
    folder = get_folder("materialdesign", "3.x")

    versions = get_versions(
        "https://api.github.com/repos/Templarian/MaterialDesign-Webfont/tags",
        "Unable to get the last version number"
        "of the MaterialDesign-Webfont package on github\n",
    )

    latest = get_latest("^v3.", versions, "v5.9.55")

    download(
        "https://github.com/Templarian/MaterialDesign-Webfont/blob/"
        + latest
        + "/css/materialdesignicons.css",
        folder,
        "materialdesignicons.css",
    )

    download(
        "https://github.com/Templarian/MaterialDesign-Webfont/blob/"
        + latest
        + "/fonts/materialdesignicons-webfont.ttf?raw=true",
        folder,
        "materialdesignicons-webfont.ttf",
    )


def download(url, folder, filename):
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
        with urllib.request.urlopen(url) as response, open(
            os.path.join(folder, filename), "wb"
        ) as out_file:
            shutil.copyfileobj(response, out_file)
    except urllib.error.HTTPError as exception:
        sys.stderr.write(str(exception))


def get_latest(match, versions, latest):
    """
    Get the latest version.

    Arguments
    ---------
    match
        A regular expression
    versions
        A list of versions
    latest
        Last known version

    Returns
    -------
        The latest version
    """
    with contextlib.suppress(TypeError):
        for version in versions:
            if re.match(match, version["name"]) and Version(version["name"]) > Version(
                latest
            ):
                latest = version["name"]
    return latest


def get_folder(collection, icon_version):
    """
    Get a folder.

    Arguments
    ---------
    collection
        The collection name
    icon_version
        The icon version

    Returns
    -------
        The folder
    """
    folder = os.path.join(
        "share",
        "pandoc_latex_tip",
        collection,
        icon_version,
    )

    if not pathlib.Path(folder).exists():
        pathlib.Path(folder).mkdir(parents=True)

    return folder


def get_versions(url, message):
    """
    Get all versions from an URL.

    Arguments
    ---------
    url
        An url
    message
        A mesasge

    Returns
    -------
        The list of versions.
    """
    try:
        return requests.get(url, timeout=300).json()
    except ValueError:
        sys.stderr.write(message)
        return []


if __name__ == "__main__":
    get_icons()
