import os


def get_existing_pages() -> list:
    existing_pages_listing_path: str = os.path.join(
        os.path.dirname(__file__), "created_pages.txt"
    )
    with open(existing_pages_listing_path, "r", encoding="utf-8") as file_data:
        exisiting_pages: list = list(
            map(lambda line: line.strip(), file_data.readlines())
        )

    return exisiting_pages
