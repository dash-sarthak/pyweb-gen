"""Blog scaffolding from packaged assets."""

import shutil
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING

import yaml

from pyweb_gen.rendering import DEFAULT_SITE_NAME

if TYPE_CHECKING:
    from importlib.abc import Traversable

SCAFFOLD_TARGETS = (
    "blog.yaml",
    "index.html",
    "templates",
    "styles",
    "assets",
    "data",
    "pages",
)


def _copy_tree(source: "Traversable", destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.iterdir():
        target = destination / item.name
        if item.is_dir():
            _copy_tree(item, target)
        else:
            with item.open("rb") as source_file, target.open("wb") as target_file:
                shutil.copyfileobj(source_file, target_file)


def initialize(root: Path, name: str = DEFAULT_SITE_NAME) -> None:
    """Copy the packaged blog scaffold into root and write the site config."""
    present = [target for target in SCAFFOLD_TARGETS if (root / target).exists()]
    if present:
        raise FileExistsError(
            f"refusing to scaffold into {root}: {present[0]} already exists"
        )

    _copy_tree(files("pyweb_gen.scaffold"), root)

    (root / "data").mkdir()
    (root / "pages").mkdir()
    (root / "blog.yaml").write_text(
        yaml.safe_dump({"name": name}, sort_keys=False), encoding="utf-8"
    )
