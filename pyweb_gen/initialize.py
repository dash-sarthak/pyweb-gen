import os

from .utils import download_from_git


def initialize():
    print("\n\t\tSetting up the directory")
    print("\t\tLoading assets")
    download_from_git("dash-sarthak", "pyweb-gen", "assets", os.getcwd())
    print("\t\tYour blog has been set up")
