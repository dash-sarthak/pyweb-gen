"""Blog scaffolding from packaged assets."""

import shutil
from importlib.resources import as_file, files
from pathlib import Path

SCAFFOLD_TARGETS = ("index.html", "templates", "styles", "assets", "data", "pages")


def initialize(root: Path) -> None:
    """Copy the packaged blog scaffold into root."""
    present = [target for target in SCAFFOLD_TARGETS if (root / target).exists()]
    if present:
        raise FileExistsError(
            f"refusing to scaffold into {root}: {present[0]} already exists"
        )

    with as_file(files("pyweb_gen.scaffold")) as scaffold:
        shutil.copytree(scaffold, root, dirs_exist_ok=True)

    (root / "data").mkdir()
    (root / "pages").mkdir()
