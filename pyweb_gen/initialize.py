import os

from .utils import download_from_git


def initialize():
    print("\n\t\tSetting up the directory")
    print("\t\tLoading assets")

    download_path: str = os.path.join(os.getcwd(), "blog")
    download_from_git("dash-sarthak", "pyweb-gen", "assets", download_path)

    print("\t\tCleaning up the directory")
    to_remove = [".git", ".gitignore", "data/._", "pages/._"]

    _ = [os.system(f"rm -rf {os.path.join(download_path, i)}") for i in to_remove]

    print("\t\tYour blog has been set up\n\n")
