import os
import subprocess
import sys
from typing import Union

from bs4 import BeautifulSoup

from .utils import get_existing_pages
from .utils import get_assets_path


class RefreshBlog:
    def __init__(self) -> None:
        self._root = os.getcwd()
        self._data_dir: str = os.path.join(self._root, "data")
        self._existing_pages: list = get_existing_pages()
        to_update, new_pages = self._check_for_new_posts()

        if to_update:
            self._assets_path: dict = get_assets_path(self._root)
            for page in new_pages:
                self.create_new_page(page)

    def _check_for_new_posts(self) -> Union[bool, list]:
        pages: list = os.listdir(self._data_dir)
        pages_to_update: list = list(
            filter(lambda page: page.split(".")[0] not in self._existing_pages, pages)
        )

        return len(pages_to_update) != 0, pages_to_update

    def create_new_page(self, page: str):
        if os.path.isfile(f"{self._data_dir}/{page}.html"):
            print("\n\n\tPost already exists.")
            sys.exit()

        file_name = f"{page}.html"
        create_post_command: list = [
            "pandoc",
            "--standalone",
            "--template",
            self._assets_path["post_template_path"],
            f"{self._assets_path['data_source_path']}/{page}.md",
            "-o",
            f"{self._assets_path['data_destination_path']}/{file_name}",
        ]
        subprocess.run(create_post_command, check=True)
        self.create_post_preview(page)

    def create_post_preview(self, page: str):
        """Create a post preview in home page

        Args:
            post_title (str): title of the created post
        """
        temp_homepage_command: list = [
            "pandoc",
            "--standalone",
            "--template",
            self._assets_path["home_template_path"],
            f"{self._assets_path['data_source_path']}/{page}.md",
            "-o",
            f"{self._root}/temp_home.html",
        ]
        subprocess.run(temp_homepage_command, check=True)

        with open(f"{self._root}/temp_home.html", "r", encoding="utf-8") as temp_html:
            html_snippet: str = str(
                BeautifulSoup(temp_html, "html.parser").select("body>div>div")[0]
            )

        with open(
            self._assets_path["home_page_path"], "r", encoding="utf-8"
        ) as home_page_html:
            content = home_page_html.readlines()
            content.insert(26, html_snippet)

        with open(self._assets_path["home_page_path"], "w", encoding="utf-8") as index:
            index.writelines(content)

        os.system(f"rm {self._root}/temp_home.html")
