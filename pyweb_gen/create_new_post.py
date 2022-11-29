from datetime import datetime
import os


class NewPost:
    def __init__(
        self, title: str, description: str = None, image_path: str = None
    ) -> None:
        self._title: str = title
        self._description: str = "" if description is None else description

        # TODO: Option to specify and store author name during initialisation
        self._author: str = "Sarthak Dash"
        self._date: str = str(datetime.now().date().strftime("%d %B, %Y"))
        self._image_path: str = "" if image_path is None else image_path
        self._id: str = self.create_post_id()

        self.create_post_file()

    def create_post_file(self):
        markdown_metadata_specifier: str = "-" * 3
        file_content = [
            markdown_metadata_specifier,
            f"title: {self._title}",
            f"description: {self._description}",
            f"author: {self._author}",
            f"date: {self._date}",
            f"id: {self._id}",
            f"img: {self._image_path}",
            markdown_metadata_specifier,
        ]
        with open(
            os.path.join(os.getcwd(), "data", f"{self._id}.md"), "w", encoding="utf-8"
        ) as md_file:
            md_file.write("\n".join(file_content))
            md_file.write("\n")

    def create_post_id(self) -> str:
        return "_".join([i.lower() for i in self._title.split(" ")])
