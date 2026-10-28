"""
App module.
"""

import pathlib
import shutil
import sys
from importlib.metadata import version

import click
import platformdirs
import yaml

from ._main import get_core_icons, main  # noqa: TID252


def _share_path(*parts: str) -> pathlib.Path:
    return pathlib.Path(sys.prefix, "share", "pandoc_latex_tip", *parts)


def _config_path() -> pathlib.Path:
    return _share_path("config.yml")


def _info(text: str) -> str:
    return click.style(text, fg="green")


def _comment(text: str) -> str:
    return click.style(text, fg="yellow")


def _warning(text: str) -> str:
    return click.style(text, fg="yellow", bold=True)


def _error(text: str) -> str:
    return click.style(text, fg="red")


def _bold(text: str) -> str:
    return click.style(text, bold=True)


@click.group(
    name="pandoc-latex-tip",
    help="pandoc-latex-tip filter (run as a pandoc filter when no command is given)",
    invoke_without_command=True,
)
@click.version_option(version=version("pandoc-latex-tip"), prog_name="pandoc-latex-tip")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    Root command group.

    Parameters
    ----------
    ctx : click.Context
        The click context.
    """
    if ctx.invoked_subcommand is None:
        main()


@cli.command(name="info", help="Give information about pandoc-latex-tip")
def info_command() -> None:
    """
    Handle info command.
    """
    click.echo(_bold("Installation"))
    click.echo(f"{_info('Version')}:        {_comment(version('pandoc-latex-tip'))}")
    click.echo("")
    click.echo(_bold("Environment"))
    click.echo(f"{_info('Collection dir')}: {_comment(str(_share_path()))}")
    click.echo(f"{_info('Config file')}:    {_comment(str(_config_path()))}")
    click.echo("")
    click.echo(_bold("Cache"))
    click.echo(
        f"{_info('Cache dir')}:      "
        f"{_comment(platformdirs.AppDirs('pandoc_latex_tip').user_cache_dir)}"
    )


@cli.group(
    name="collections",
    help="List the collections",
    invoke_without_command=True,
)
@click.pass_context
def collections_group(ctx: click.Context) -> None:
    """
    Handle collections command.

    Parameters
    ----------
    ctx : click.Context
        The click context.
    """
    if ctx.invoked_subcommand is not None:
        return
    click.echo(_bold("Collections"))
    for folder in _share_path().iterdir():
        if folder.parts[-1] == "fontawesome":
            click.echo(_error("fontawesome"))
        elif folder.is_dir():
            click.echo(_warning(folder.parts[-1]))


@collections_group.command(
    name="add",
    help=(
        "Add a file to a collection. A collection is a space used to store all "
        "the CSS, TTF and WOFF2 files related to one or more sets of icons."
    ),
)
@click.argument("name")
@click.argument("file")
def collections_add(name: str, file: str) -> None:
    """
    Handle collections add command.

    Parameters
    ----------
    name : str
        Collection name.
    file : str
        File name.

    Raises
    ------
    click.ClickException
        If an error occurs.
    """
    if name == "fontawesome":
        message = "You cannot modify core collection"
        raise click.ClickException(message)
    dir_path = _share_path(name)
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
    file_path = pathlib.Path(file)
    if file_path.suffix not in (".css", ".ttf", ".woff2"):
        message = "The added file must be a CSS, TTF or WOFF2 file"
        raise click.ClickException(message)
    dest_path = pathlib.Path(dir_path, file_path.parts[-1])
    shutil.copy(file_path, dest_path)

    click.echo(f"Add file {_comment(repr(file))} to collection {_warning(repr(name))}")


@collections_group.command(
    name="delete",
    help=(
        "Delete a collection. Deleting a collection will erase the folder "
        "containing its files. The operation cannot proceed if the collection "
        "is used by a set of icons."
    ),
)
@click.argument("name")
def collections_delete(name: str) -> None:
    """
    Handle collections delete command.

    Parameters
    ----------
    name : str
        Collection name.

    Raises
    ------
    click.ClickException
        If an error occurs.
    """
    if name == "fontawesome":
        message = "You cannot modify core collection"
        raise click.ClickException(message)
    dir_path = _share_path(name)
    config_path = _config_path()
    if config_path.exists():
        with config_path.open(encoding="utf-8") as stream:
            icons = yaml.safe_load(stream)
            for definition in icons:
                if definition["collection"] == name:
                    message = f"Collection '{name}' is in use"
                    raise click.ClickException(message)

    if not dir_path.exists():
        message = f"Collection '{name}' does not exist"
        raise click.ClickException(message)

    shutil.rmtree(dir_path)
    click.echo(f"Delete collection {_warning(repr(name))}")


@collections_group.command(
    name="info",
    help=(
        "Display a collection. Displaying a collection allows listing all "
        "the CSS, TTF and WOFF2 files it contains."
    ),
)
@click.argument("name")
def collections_info(name: str) -> None:
    """
    Handle collections info command.

    Parameters
    ----------
    name : str
        Collection name.

    Raises
    ------
    click.ClickException
        If an error occurs.
    """
    dir_path = _share_path(name)
    if not dir_path.exists():
        message = f"Collection '{name}' does not exist"
        raise click.ClickException(message)

    click.echo(_bold("Information"))
    if name == "fontawesome":
        click.echo(f"{_info('Name')}: {_error(name)}")
        click.echo(f"{_info('Type')}: {_error('core')}")
    else:
        click.echo(f"{_info('Name')}: {_warning(name)}")
        click.echo(f"{_info('Type')}: {_warning('additional')}")

    click.echo("")
    click.echo(_bold("CSS files"))
    for filename in dir_path.iterdir():
        if filename.suffix == ".css":
            click.echo(f"- {_comment(filename.parts[-1])}")

    click.echo("")
    click.echo(_bold("TTF/WOFF2 files"))
    for filename in dir_path.iterdir():
        if filename.suffix in (".ttf", ".woff2"):
            click.echo(f"- {_comment(filename.parts[-1])}")


@cli.group(
    name="icons",
    help="List the set of icons",
    invoke_without_command=True,
)
@click.pass_context
def icons_group(ctx: click.Context) -> None:
    """
    Handle icons command.

    Parameters
    ----------
    ctx : click.Context
        The click context.
    """
    if ctx.invoked_subcommand is not None:
        return
    icons = get_core_icons()
    config_path = _config_path()
    if config_path.exists():
        with config_path.open(encoding="utf-8") as stream:
            icons.extend(yaml.safe_load(stream))
    for element in icons:
        if element["collection"] == "fontawesome":
            click.echo(f"- {_info('collection')}: {_error('fontawesome')}")
        else:
            click.echo(f"- {_info('collection')}: {_warning(element['collection'])}")
        click.echo(f"  {_info('CSS')}: {_comment(element['CSS'])}")
        click.echo(
            f"  {_info('ICONS')}: {_comment(element.get('ICONS', element.get('TTF', '')))}"
        )
        click.echo(f"  {_info('prefix')}: {_comment(element['prefix'])}")


@icons_group.command(
    name="add",
    help=(
        "Add a set of icons from a collection. A set of icons is created from "
        "a CSS file and a TTF or WOFF2 file from a collection. The prefix ensures that "
        "the icons are unique. It replaces the common prefix detected in the "
        "CSS file."
    ),
)
@click.argument("name")
@click.option("--CSS", "css", help="CSS filename from the collection")
@click.option("--ICONS", "icons_file", help="TTF or WOFF2 filename from the collection")
@click.option(
    "-p",
    "--prefix",
    help="Icon prefix used to replace the common prefix found in the css file",
)
def icons_add(
    name: str, css: str | None, icons_file: str | None, prefix: str | None
) -> None:
    """
    Handle icons add command.

    Parameters
    ----------
    name : str
        Collection name.
    css : str | None
        CSS filename from the collection.
    icons_file : str | None
        TTF or WOFF2 filename from the collection.
    prefix : str | None
        Icon prefix.

    Raises
    ------
    click.ClickException
        If an error occurs.
    """
    if name == "fontawesome":
        message = "You cannot modify core collection"
        raise click.ClickException(message)
    dir_path = _share_path(name)
    if not dir_path.exists():
        message = f"Collection '{name}' does not exist"
        raise click.ClickException(message)
    if not css:
        message = "CSS option is mandatory"
        raise click.ClickException(message)
    if not pathlib.Path(dir_path, css).exists():
        message = f"Collection '{name}' does not contain '{css}'"
        raise click.ClickException(message)
    if not icons_file:
        message = "ICONS option is mandatory"
        raise click.ClickException(message)
    if not pathlib.Path(dir_path, icons_file).exists():
        message = f"Collection '{name}' does not contain '{icons_file}'"
        raise click.ClickException(message)
    if not prefix:
        message = "prefix option is mandatory"
        raise click.ClickException(message)
    config_path = _config_path()
    if config_path.exists():
        with config_path.open(encoding="utf-8") as stream:
            icons = yaml.safe_load(stream)
            for definition in icons:
                if definition["prefix"] == prefix:
                    message = f"Prefix '{prefix}' is already used"
                    raise click.ClickException(message)
    else:
        icons = []
    icons.append(
        {
            "collection": name,
            "CSS": css,
            "ICONS": icons_file,
            "prefix": prefix,
        },
    )
    with config_path.open(mode="w", encoding="utf-8") as stream:
        stream.write(yaml.dump(icons, sort_keys=False))


@icons_group.command(name="delete", help="Delete a set of icons")
@click.option(
    "-p",
    "--prefix",
    help="Icon prefix used to replace the common prefix found in the css file",
)
def icons_delete(prefix: str | None) -> None:
    """
    Handle icons delete command.

    Parameters
    ----------
    prefix : str | None
        Icon prefix.

    Raises
    ------
    click.ClickException
        If an error occurs.
    """
    if not prefix:
        message = "prefix option is mandatory"
        raise click.ClickException(message)
    if prefix in ("fa-", "far-", "fab-"):
        message = "You cannot modify core icons"
        raise click.ClickException(message)
    config_path = _config_path()
    if not config_path.exists():
        message = "Unexisting config file"
        raise click.ClickException(message)
    with config_path.open(encoding="utf-8") as stream:
        icons = yaml.safe_load(stream)
    keep = [definition for definition in icons if definition["prefix"] != prefix]
    if keep == icons:
        message = "Unexisting prefix"
        raise click.ClickException(message)
    with config_path.open(mode="w", encoding="utf-8") as stream:
        stream.write(yaml.dump(keep, sort_keys=False))


def app() -> None:
    """
    Run the click application.
    """
    # Pandoc calls filters with the output format as first argument
    if len(sys.argv) > 1 and sys.argv[1] not in cli.commands and sys.argv[1][0] != "-":
        main()
    else:
        cli()  # pylint: disable=no-value-for-parameter
