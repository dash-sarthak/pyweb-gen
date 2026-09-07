"""Command line entry point for pyweb-gen."""

import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

from pyweb_gen.create_new_post import PostInput, create_post
from pyweb_gen.initialize import initialize
from pyweb_gen.parser import build_parser
from pyweb_gen.refresh_blog import refresh_blog
from pyweb_gen.server import serve_blog

_COMMAND_ERRORS = (FileNotFoundError, FileExistsError, ValueError)


def main(argv: Sequence[str] | None = None) -> int:
    """Dispatch one command; returns a process status code."""
    args = build_parser().parse_args(argv)
    root = Path.cwd()

    try:
        if args.command == "init":
            initialize(root)
            print(f"Scaffolded a new blog in {root}")
        elif args.command == "new-post":
            post = create_post(
                PostInput(
                    title=args.title,
                    description=args.description or "",
                    image_path=args.image or "",
                ),
                root / "data",
                datetime.now(UTC).date(),
            )
            print(f"Created {post}")
        elif args.command == "refresh":
            new_pages = refresh_blog(root)
            if new_pages:
                print(f"Rendered: {', '.join(new_pages)}")
            else:
                print("Up to date")
        elif args.command == "serve":
            serve_blog(root, port=args.port)
    except _COMMAND_ERRORS as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    return 0
