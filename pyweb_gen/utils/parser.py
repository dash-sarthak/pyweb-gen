import argparse
import sys


class Parser:
    def __init__(self) -> None:
        self._parent_parser = argparse.ArgumentParser(
            prog="pyweb-gen",
            usage="%(prog)s [command] [arguments]",
            description="Creates a minimal blog from markdown files",
        )
        self._command_sub_parsers = self._parent_parser.add_subparsers(
            title="command", dest="command", required=True
        )
        self._init_command()
        self._new_post_command()
        self._refresh_command()

    def _init_command(self):
        _ = self._command_sub_parsers.add_parser("init", usage="pyweb-gen init")

    def _new_post_command(self):
        new_post_command = self._command_sub_parsers.add_parser(
            "new-post", usage="pyweb-gen new-post [--title / --description / --image]"
        )

        new_post_command.add_argument(
            "--title",
            "-t",
            nargs="?",
            required=True,
            type=str,
            help="Title of the new post",
        )

        new_post_command.add_argument(
            "--description",
            "-d",
            nargs="?",
            required=False,
            type=str,
            help="Description of the post",
        )

        new_post_command.add_argument(
            "--image",
            "-i",
            nargs="?",
            required=False,
            type=str,
            help="Path of any image associated with the post",
        )

    def _refresh_command(self):
        _ = self._command_sub_parsers.add_parser("refresh", usage="pyweb-gen refresh")

    def parse(self) -> argparse.Namespace:
        try:
            args = self._parent_parser.parse_args()
            return args
        except argparse.ArgumentError:
            print("Error while parsing arguments")
            sys.exit(-1)
