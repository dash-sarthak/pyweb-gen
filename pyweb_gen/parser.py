"""Argument parser for the pyweb-gen command line interface."""

from argparse import ArgumentParser
from importlib.metadata import PackageNotFoundError, version

from pyweb_gen.rendering import DEFAULT_SITE_NAME

PROG = "pyweb-gen"


def package_version() -> str:
    try:
        return version("pyweb-gen")
    except PackageNotFoundError:
        return "unknown"


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog=PROG,
        description="Creates a minimal blog from markdown files",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {package_version()}",
    )
    commands = parser.add_subparsers(title="command", dest="command", required=True)

    init = commands.add_parser(
        "init", help="Scaffold a new blog in the current directory"
    )
    init.add_argument(
        "--name",
        "-n",
        default=DEFAULT_SITE_NAME,
        help=f"Name of the blog (default: {DEFAULT_SITE_NAME})",
    )

    new_post = commands.add_parser("new-post", help="Create a new post")
    new_post.add_argument("--title", "-t", required=True, help="Title of the new post")
    new_post.add_argument(
        "--description", "-d", default=None, help="Description of the post"
    )
    new_post.add_argument(
        "--image", "-i", default=None, help="Path of any image associated with the post"
    )

    commands.add_parser("refresh", help="Render new posts and rebuild the home page")
    serve = commands.add_parser(
        "serve", help="Preview the built blog on a local web server"
    )
    serve.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to serve on (default: 8000)",
    )

    return parser
