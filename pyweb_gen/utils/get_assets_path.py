import os


def get_assets_path(root: str) -> dict:
    """Generates and returns a dict of required path

    Args:
        root (str): path of the root directory

    Returns:
        dict: dict containing required paths
    """
    paths: dict = {
        "post_template_path": os.path.join(root, "templates/post_template.html"),
        "home_template_path": os.path.join(root, "templates/home_template.html"),
        "home_page_path": os.path.join(root, "index.html"),
        "data_source_path": os.path.join(root, "data"),
        "data_destination_path": os.path.join(root, "pages"),
    }

    return paths
