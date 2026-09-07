"""Command line entry point for pyweb-gen."""

from collections.abc import Sequence
from pathlib import Path

from pyweb_gen.create_new_post import NewPost
from pyweb_gen.initialize import initialize
from pyweb_gen.refresh_blog import RefreshBlog
from pyweb_gen.utils.parser import build_parser


def main(argv: Sequence[str] | None = None) -> None:
    """Dispatch one command."""
    args = build_parser().parse_args(argv)

    if args.command == "init":
        initialize(Path.cwd())
    elif args.command == "new-post":
        NewPost(title=args.title, description=args.description, image_path=args.image)
    elif args.command == "refresh":
        RefreshBlog()
