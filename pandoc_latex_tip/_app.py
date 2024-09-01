"""
App module.
"""

import pathlib
import shutil
import sys
from importlib.metadata import version

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option

import platformdirs

import yaml

from ._main import get_core_icons, main  # noqa: TID252

name_arg = argument(
    "name",
    description="Collection name",
)
file_arg = argument(
    "file",
    description="File name",
)
css_opt = option(
    "CSS",
    description="CSS filename from the collection",
    flag=False,
)
ttf_opt = option(
    "TTF",
    description="TTF filename from the collection",
    flag=False,
)
prefix_opt = option(
    "prefix",
    short_name="p",
    description="Icon prefix used to replace the common prefix found in the css file",
    flag=False,
)


class InfoCommand(Command):  # type: ignore[misc]
    """
    InfoCommand.
    """

    name = "info"
    description = "Give information about pandoc-latex-tip"

    def handle(self) -> int:
        """
        Handle info command.

        Returns
        -------
        int
            status code
        """
        self.line("<b>Installation</>")
        self.line(
            f"<info>Version</>:        <comment>" f"{version('pandoc-latex-tip')}"
        )
        self.line("")
        self.line("<b>Environment</>")
        self.line(
            f"<info>Collection dir</>: <comment>"
            f"{pathlib.Path(sys.prefix, 'share', 'pandoc_latex_tip')}</>"
        )
        self.line(
            f"<info>Config file</>:    <comment>"
            f"{pathlib.Path(sys.prefix, 'share', 'pandoc_latex_tip', 'config.yml')}</>"
        )
        self.line("")
        self.line("<b>Cache</>")
        self.line(
            f"<info>Cache dir</>:      <comment>"
            f"{platformdirs.AppDirs('pandoc_latex_tip').user_cache_dir}</>"
        )
        return 0


class CollectionsAddCommand(Command):  # type: ignore[misc]
    """
    CollectionsAddCommand.
    """

    name = "collections add"
    description = "Add a file to a collection"
    arguments = (name_arg, file_arg)
    help = (
        "A collection is a space used to store all the CSS and TTF files "
        "related to one or more sets of icons."
    )

    def handle(self) -> int:
        """
        Handle collections add command.

        Returns
        -------
        int
            status code

        Raises
        ------
        ValueError
            If an error occurs.
        """
        self.add_style("warning", fg="yellow", options=["bold"])
        if self.argument("name") == "fontawesome":
            message = "You cannot modify core collection"
            raise ValueError(message)
        dir_path = pathlib.Path(
            sys.prefix, "share", "pandoc_latex_tip", self.argument("name")
        )
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        file_path = pathlib.Path(self.argument("file"))
        if file_path.suffix not in (".css", ".ttf"):
            message = "The added file must be a CSS or TTF file"
            raise ValueError(message)
        dest_path = pathlib.Path(dir_path, file_path.parts[-1])
        shutil.copy(file_path, dest_path)

        self.line(
            f"Add file <comment>'{self.argument('file')}'</> to "
            f"collection <warning>'{self.argument('name')}'</>"
        )
        return 0


class CollectionsDeleteCommand(Command):  # type: ignore[misc]
    """
    CollectionDeleteCommand.
    """

    name = "collections delete"
    description = "Delete a collection"
    arguments = (name_arg,)
    help = (
        "Deleting a collection will erase the folder containing its files. "
        "The operation cannot proceed if the collection is used by a set of icons."
    )

    def handle(self) -> int:
        """
        Handle collections delete command.

        Returns
        -------
        int
            status code

        Raises
        ------
        ValueError
            If an error occurs.
        """
        self.add_style("warning", fg="yellow", options=["bold"])
        name = self.argument("name")
        if name == "fontawesome":
            message = "You cannot modify core collection"
            raise ValueError(message)
        dir_path = pathlib.Path(sys.prefix, "share", "pandoc_latex_tip", name)
        config_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            "config.yml",
        )
        if config_path.exists():
            with config_path.open(encoding="utf-8") as stream:
                icons = yaml.safe_load(stream)
                for definition in icons:
                    if definition["collection"] == name:
                        message = f"Collection '{name}' is in use"
                        raise ValueError(message)

        if not dir_path.exists():
            message = f"Collection '{name}' does not exist"
            raise ValueError(message)

        shutil.rmtree(dir_path)
        self.line(f"Delete collection <warning>'{name}'</>")
        return 0


class CollectionsListCommand(Command):  # type: ignore[misc]
    """
    CollectionsListCommand.
    """

    name = "collections"
    description = "List the collections"

    def handle(self) -> int:
        """
        Handle collections command.

        Returns
        -------
        int
            status code
        """
        self.add_style("warning", fg="yellow", options=["bold"])
        dir_path = pathlib.Path(sys.prefix, "share", "pandoc_latex_tip")
        self.line("<b>Collections</>")
        for folder in dir_path.iterdir():
            if folder.parts[-1] == "fontawesome":
                self.line("<error>fontawesome</>")
            elif folder.is_dir():
                self.line(f"<warning>{folder.parts[-1]}</>")
        return 0


class CollectionsInfoCommand(Command):  # type: ignore[misc]
    """
    CollectionsInfoCommand.
    """

    name = "collections info"
    description = "Display a collection"
    arguments = (name_arg,)
    help = (
        "Displaying a collection allows listing all the "
        "CSS and TTF files it contains."
    )

    def handle(self) -> int:
        """
        Handle collections info command.

        Returns
        -------
        int
            status code

        Raises
        ------
        ValueError
            If an error occurs.
        """
        self.add_style("warning", fg="yellow", options=["bold"])
        name = self.argument("name")
        dir_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            name,
        )
        if not dir_path.exists():
            message = f"Collection '{name}' does not exist"
            raise ValueError(message)

        self.line("<b>Information</>")
        if name == "fontawesome":
            self.line(f"<info>Name</>: <error>{name}</>")
            self.line("<info>Type</>: <error>core</>")
        else:
            self.line(f"<info>Name</>: <warning>{name}</>")
            self.line("<info>Type</>: <warning>additional</>")

        self.line("")
        self.line("<b>CSS files</>")
        for filename in dir_path.iterdir():
            if filename.suffix == ".css":
                self.line(f"- <comment>{filename.parts[-1]}</>")

        self.line("")
        self.line("<b>TTF files</>")
        for filename in dir_path.iterdir():
            if filename.suffix == ".ttf":
                self.line(f"- <comment>{filename.parts[-1]}</>")

        return 0


class IconsAddCommand(Command):  # type: ignore[misc]
    """
    IconsAddCommand.
    """

    name = "icons add"
    description = "Add a set of icons from a collection"
    arguments = (name_arg,)
    options = (css_opt, ttf_opt, prefix_opt)
    help = (
        "A set of icons is created from a CSS file and a TTF file from a collection. "
        "The prefix ensures that the icons are unique. "
        "It replaces the common prefix detected in the CSS file."
    )

    # pylint: disable=too-many-return-statements, too-many-branches
    def handle(self) -> int:
        """
        Handle icons add command.

        Returns
        -------
        int
            status code

        Raises
        ------
        ValueError
            If an error occurs.
        """
        name = self.argument("name")
        if name == "fontawesome":
            message = "You cannot modify core collection"
            raise ValueError(message)
        dir_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            self.argument("name"),
        )
        if dir_path.exists():
            if not self.option("CSS"):
                message = "CSS option is mandatory"
                raise ValueError(message)
            css = self.option("CSS")
            css_file = pathlib.Path(dir_path, css)
            if not css_file.exists():
                message = f"Collection '{name}' does not contain '{css}'"
                raise ValueError(message)
            if not self.option("TTF"):
                message = "TTF option is mandatory"
                raise ValueError(message)
            ttf = self.option("TTF")
            ttf_file = pathlib.Path(dir_path, ttf)
            if not ttf_file.exists():
                message = f"Collection '{name}' does not contain '{ttf}'"
                raise ValueError(message)
            if not self.option("prefix"):
                message = "prefix option is mandatory"
                raise ValueError(message)
            prefix = self.option("prefix")
            config_path = pathlib.Path(
                sys.prefix,
                "share",
                "pandoc_latex_tip",
                "config.yml",
            )
            if config_path.exists():
                with config_path.open(encoding="utf-8") as stream:
                    icons = yaml.safe_load(stream)
                    for definition in icons:
                        if definition["prefix"] == prefix:
                            message = f"Prefix '{prefix}' is already used"
                            raise ValueError(message)
            else:
                icons = []
            icons.append(
                {
                    "collection": name,
                    "CSS": css,
                    "TTF": ttf,
                    "prefix": prefix,
                },
            )
            with config_path.open(mode="w", encoding="utf-8") as stream:
                stream.write(yaml.dump(icons, sort_keys=False))

        else:
            message = f"Collection '{name}' does not exist"
            raise ValueError(message)
        return 0


class IconsDeleteCommand(Command):  # type: ignore[misc]
    """
    IconsDeleteCommand.
    """

    name = "icons delete"
    description = "Delete a set of icons"
    options = (prefix_opt,)

    def handle(self) -> int:
        """
        Handle icons delete command.

        Returns
        -------
        int
            status code

        Raises
        ------
        ValueError
            If an error occurs.
        """
        if not self.option("prefix"):
            message = "prefix option is mandatory"
            raise ValueError(message)
        prefix = self.option("prefix")
        if prefix in ("fa-", "far-", "fab-"):
            message = "You cannot modify core icons"
            raise ValueError(message)
        config_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            "config.yml",
        )
        if config_path.exists():
            with config_path.open(encoding="utf-8") as stream:
                icons = yaml.safe_load(stream)
            keep = [
                definition for definition in icons if definition["prefix"] != prefix
            ]
            if keep != icons:
                with config_path.open(mode="w", encoding="utf-8") as stream:
                    stream.write(yaml.dump(keep, sort_keys=False))
            else:
                message = "Unexisting prefix"
                raise ValueError(message)
        else:
            message = "Unexisting config file"
            raise ValueError(message)
        return 0


class IconsListCommand(Command):  # type: ignore[misc]
    """
    IconsListCommand.
    """

    name = "icons"
    description = "List the set of icons"

    def handle(self) -> int:
        """
        Handle icons command.

        Returns
        -------
        int
            status code
        """
        self.add_style("warning", fg="yellow", options=["bold"])
        icons = get_core_icons()
        config_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            "config.yml",
        )
        if config_path.exists():
            with config_path.open(encoding="utf-8") as stream:
                icons.extend(yaml.safe_load(stream))
        for element in icons:
            if element["collection"] == "fontawesome":
                self.line("- <info>collection</>: <error>fontawesome</>")
            else:
                self.line(f"- <info>collection</>: <warning>{element['collection']}</>")
            self.line(f"  <info>CSS</>: <comment>{element['CSS']}</>")
            self.line(f"  <info>TTF</>: <comment>{element['TTF']}</>")
            self.line(f"  <info>prefix</>: <comment>{element['prefix']}</>")
        return 0


class PandocLaTeXFilterCommand(Command):  # type: ignore[misc]
    """
    PandocLaTeXFilterCommand.
    """

    name = "latex"
    description = "Run pandoc filter for LaTeX document"

    def handle(self) -> int:
        """
        Handle latex command.

        Returns
        -------
        int
            status code
        """
        main()
        return 0


class PandocBeamerFilterCommand(Command):  # type: ignore[misc]
    """
    PandocBeamerFilterCommand.
    """

    name = "beamer"
    description = "Run pandoc filter for Beamer document"

    def handle(self) -> int:
        """
        Handle beamer command.

        Returns
        -------
        int
            status code
        """
        main()
        return 0


def app() -> None:
    """
    Create a cleo application.
    """
    application = Application(
        name="pandoc-latex-tip filter",
        version=version("pandoc-latex-tip"),
    )
    application.set_display_name("pandoc-latex-tip filter")
    application.add(InfoCommand())
    application.add(CollectionsAddCommand())
    application.add(CollectionsDeleteCommand())
    application.add(CollectionsListCommand())
    application.add(CollectionsInfoCommand())
    application.add(IconsAddCommand())
    application.add(IconsDeleteCommand())
    application.add(IconsListCommand())
    application.add(PandocLaTeXFilterCommand())
    application.add(PandocBeamerFilterCommand())
    application.run()
