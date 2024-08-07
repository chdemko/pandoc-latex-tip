"""
App module.
"""

import pathlib
import shutil
import sys

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option

import yaml

from ._main import get_core_icons, main

name_arg = argument(
    "name",
    description="Collection name",
)
file_arg = argument(
    "file",
    description="File name",
)
css_opt = option(
    "css",
    flag=False,
    description="css filename from the collection",
)
ttf_opt = option(
    "ttf",
    flag=False,
    description="ttf filename from the collection",
)
prefix_opt = option(
    "prefix",
    flag=False,
    description="icon prefix used to replace the common prefix found in the css file",
)


class CollectionsAddCommand(Command):
    """
    CollectionsAddCommand.
    """

    name = "collections add"
    description = "Add a file to a collection"
    arguments = [name_arg, file_arg]

    def handle(self) -> int:
        """
        Handle collections add command.

        Returns
        -------
        int
            status code
        """
        if self.argument("name") == "fontawesome":
            self.line("<error>You cannot modify core collection</error>")
            return 1

        try:
            dir_path = pathlib.Path(
                sys.prefix, "share", "pandoc_latex_tip", self.argument("name")
            )
            if not dir_path.exists():
                dir_path.mkdir(parents=True)
            file_path = pathlib.Path(self.argument("file"))
            dest_path = pathlib.Path(dir_path, file_path.parts[-1])
            shutil.copy(file_path, dest_path)

            self.line(
                f"Add file '{self.argument('file')}' to "
                f"collection '{self.argument('name')}'"
            )

        except PermissionError as error:
            self.line(f"<error>{error}</error>")
            return 1
        return 0


class CollectionsDeleteCommand(Command):
    """
    CollectionDeleteCommand.
    """

    name = "collections delete"
    description = "Delete a collection"
    arguments = [name_arg]

    def handle(self) -> int:
        """
        Handle collections delete command.

        Returns
        -------
        int
            status code
        """
        if self.argument("name") == "fontawesome":
            self.line("<error>You cannot modify core collection</error>")
            return 1
        try:
            dir_path = pathlib.Path(
                sys.prefix, "share", "pandoc_latex_tip", self.argument("name")
            )
            config_path = pathlib.Path(
                sys.prefix,
                "share",
                "pandoc_latex_tip",
                "config.yml",
            )
            try:
                if config_path.exists():
                    with config_path.open(encoding="utf-8") as stream:
                        icons = yaml.safe_load(stream)
                        for definition in icons:
                            if definition["collection"] == self.argument("name"):
                                self.line(
                                    f"<error>Collection '{self.argument('name')}' "
                                    f"is in use</error>"
                                )
                                return 1
            except PermissionError as error:
                self.line(f"<error>{error}</error>")
                return 1

            if dir_path.exists():
                shutil.rmtree(dir_path)
                self.line(f"Delete collection '{self.argument('name')}'")
            else:
                self.line(
                    f"<error>Collection '{self.argument('name')}' "
                    f"does not exist</error>"
                )
                return 1
        except PermissionError as error:
            self.line(f"<error>{error}</error>")
            return 1
        return 0


class CollectionsListCommand(Command):
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
        dir_path = pathlib.Path(sys.prefix, "share", "pandoc_latex_tip")
        for folder in dir_path.iterdir():
            if folder.parts[-1] == "fontawesome":
                self.line("<info>fontawesome *</info>")
            elif folder.is_dir():
                self.line(folder.parts[-1])
        return 0


class CollectionsInfoCommand(Command):
    """
    CollectionsInfoCommand.
    """

    name = "collections info"
    description = "Display a collection"
    arguments = [name_arg]

    def handle(self) -> int:
        """
        Handle collections info command.

        Returns
        -------
        int
            status code
        """
        dir_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            self.argument("name"),
        )
        if dir_path.exists():
            for filename in dir_path.iterdir():
                self.line(filename.parts[-1])
        else:
            self.line(
                f"<error>Collection '{self.argument('name')}' "
                f"does not exist</error>"
            )
            return 1
        return 0


class IconsAddCommand(Command):
    """
    IconsAddCommand.
    """

    name = "icons add"
    description = "Add a set of icons from a collection"
    arguments = [name_arg]
    options = [css_opt, ttf_opt, prefix_opt]

    # pylint: disable=too-many-return-statements
    def handle(self) -> int:
        """
        Handle icons add command.

        Returns
        -------
        int
            status code
        """
        if self.argument("name") == "fontawesome":
            self.line("<error>You cannot modify core collection</error>")
            return 1
        dir_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            self.argument("name"),
        )
        if dir_path.exists():
            css_file = pathlib.Path(dir_path, self.option("css"))
            if not css_file.exists():
                self.line(
                    f"<error>Collection '{self.argument('name')}' "
                    f"does not contain '{self.option('css')}'</error>"
                )
                return 1
            ttf_file = pathlib.Path(dir_path, self.option("ttf"))
            if not ttf_file.exists():
                self.line(
                    f"<error>Collection '{self.argument('name')}' "
                    f"does not contain '{self.option('ttf')}'</error>"
                )
                return 1
            config_path = pathlib.Path(
                sys.prefix,
                "share",
                "pandoc_latex_tip",
                "config.yml",
            )
            try:
                if config_path.exists():
                    with config_path.open(encoding="utf-8") as stream:
                        icons = yaml.safe_load(stream)
                        for definition in icons:
                            if definition["prefix"] == self.option("prefix"):
                                self.line(
                                    f"<error>Prefix '{self.option('prefix')}' "
                                    f"is already used</error>"
                                )
                                return 1
                else:
                    icons = []
                icons.append(
                    {
                        "collection": self.argument("name"),
                        "css": self.option("css"),
                        "ttf": self.option("ttf"),
                        "prefix": self.option("prefix"),
                    },
                )
                with config_path.open(mode="w", encoding="utf-8") as stream:
                    stream.write(yaml.dump(icons, sort_keys=False))
            except PermissionError as error:
                self.line(f"<error>{error}</error>")
                return 1

        else:
            self.line(
                f"<error>Collection '{self.argument('name')}' "
                f"does not exist</error>"
            )
            return 1
        return 0


class IconsDeleteCommand(Command):
    """
    IconsDeleteCommand.
    """

    name = "icons delete"
    description = "Delete a set of icons"
    options = [prefix_opt]

    def handle(self) -> int:
        """
        Handle icons delete command.

        Returns
        -------
        int
            status code
        """
        if self.option("prefix") in ("fa-", "far-", "fab-"):
            self.line("<error>You cannot modify core icons</error>")
            return 1
        config_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            "config.yml",
        )
        try:
            if config_path.exists():
                with config_path.open(encoding="utf-8") as stream:
                    icons = yaml.safe_load(stream)
                keep = [
                    definition
                    for definition in icons
                    if definition["prefix"] != self.option("prefix")
                ]
                if keep != icons:
                    with config_path.open(mode="w", encoding="utf-8") as stream:
                        stream.write(yaml.dump(keep, sort_keys=False))
                else:
                    self.line("<error>Unexisting prefix</error>")
                    return 1
            else:
                self.line("<error>Unexisting config file</error>")
                return 1

        except PermissionError as error:
            self.line(f"<error>{error}</error>")
            return 1
        return 0


class IconsListCommand(Command):
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
        icons = get_core_icons()
        config_path = pathlib.Path(
            sys.prefix,
            "share",
            "pandoc_latex_tip",
            "config.yml",
        )
        try:
            if config_path.exists():
                with config_path.open(encoding="utf-8") as stream:
                    icons.extend(yaml.safe_load(stream))
        except PermissionError as error:
            self.line(f"<error>{error}</error>")
            return 1

        self.line(yaml.dump(icons, sort_keys=False))

        return 0


class PandocLaTeXFilterCommand(Command):
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


class PandocBeamerFilterCommand(Command):
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
    application = Application("pandoc-latex-tip filter")
    application.set_display_name("pandoc-latex-tip filter")
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
