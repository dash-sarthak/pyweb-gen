"""Blog scaffolding: init copies the packaged scaffold and writes the site config."""

from pathlib import Path

import pytest

from pyweb_gen.initialize import initialize

SCAFFOLD_FILES = [
    "templates/post_template.html",
    "templates/home_template.html",
    "styles/index.css",
    "styles/base.css",
    "styles/post.css",
    "assets/favicon.svg",
    "assets/icon.svg",
    "index.html",
]


def test_init_copies_scaffold_into_empty_directory(tmp_path: Path) -> None:
    initialize(tmp_path)

    for relative in SCAFFOLD_FILES:
        copied = tmp_path / relative
        assert copied.is_file(), f"missing scaffold file: {relative}"
        assert copied.stat().st_size > 0
    assert (tmp_path / "data").is_dir()
    assert (tmp_path / "pages").is_dir()


def test_init_refuses_to_overwrite_existing_blog(tmp_path: Path) -> None:
    initialize(tmp_path)
    index_before = (tmp_path / "index.html").read_text(encoding="utf-8")

    with pytest.raises(FileExistsError):
        initialize(tmp_path)

    assert (tmp_path / "index.html").read_text(encoding="utf-8") == index_before


def test_init_allows_directory_with_unrelated_files(tmp_path: Path) -> None:
    (tmp_path / "notes.txt").write_text("scratch", encoding="utf-8")

    initialize(tmp_path)

    assert (tmp_path / "index.html").is_file()
    assert (tmp_path / "notes.txt").read_text(encoding="utf-8") == "scratch"


def test_init_writes_default_site_name(tmp_path: Path) -> None:
    initialize(tmp_path)

    config = (tmp_path / "blog.yaml").read_text(encoding="utf-8")

    assert "name: Blog" in config


def test_init_writes_custom_site_name(tmp_path: Path) -> None:
    initialize(tmp_path, name="Inkwell")

    config = (tmp_path / "blog.yaml").read_text(encoding="utf-8")

    assert "name: Inkwell" in config


def test_init_refuses_when_only_config_exists(tmp_path: Path) -> None:
    (tmp_path / "blog.yaml").write_text("name: Blog\n", encoding="utf-8")

    with pytest.raises(FileExistsError):
        initialize(tmp_path)

    assert (tmp_path / "blog.yaml").read_text(encoding="utf-8") == "name: Blog\n"
