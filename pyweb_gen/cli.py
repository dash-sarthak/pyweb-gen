"""Command line entry point for pyweb-gen."""

from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from pyweb_gen.create_new_post import PostInput, create_post
from pyweb_gen.initialize import initialize
from pyweb_gen.parser import build_parser
from pyweb_gen.refresh_blog import refresh_blog


def main(argv: Sequence[str] | None = None) -> None:
    """Dispatch one command."""
    args = build_parser().parse_args(argv)

    if args.command == "init":
        initialize(Path.cwd())
    elif args.command == "new-post":
        create_post(
            PostInput(
                title=args.title,
                description=args.description or "",
                image_path=args.image or "",
            ),
            Path.cwd() / "data",
            datetime.now(UTC).date(),
        )
    elif args.command == "refresh":
        refresh_blog(Path.cwd())
