import argparse

from .create_new_post import NewPost
from .initialize import initialize
from .refresh_blog import RefreshBlog

from .utils import Parser


class CLIHandler:
    def __init__(self) -> None:
        args: argparse.Namespace = Parser().parse()
        print(args)
        command: str = args.command

        if command == "init":
            initialize()
        elif command == "new-post":
            title: str = args.title
            description: str = args.description
            image: str = args.image

            NewPost(title=title, description=description, image_path=image)
        elif command == "refresh":
            RefreshBlog()
