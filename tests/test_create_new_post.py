"""Post creation: slugified ids, front matter writing, deterministic dates."""

from datetime import date
from pathlib import Path

import pytest

from pyweb_gen.create_new_post import PostInput, create_post
from pyweb_gen.rendering import load_post

TODAY = date(2026, 9, 7)


def test_create_post_writes_markdown_with_front_matter(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    target = create_post(
        PostInput(title="My first post", description="Hello there"),
        data_dir,
        TODAY,
    )

    assert target == data_dir / "my_first_post.md"
    post = load_post(target)
    assert post.title == "My first post"
    assert post.description == "Hello there"
    assert post.id == "my_first_post"
    assert post.date == "2026-09-07"


def test_create_post_slugs_punctuation_out_of_title(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    target = create_post(PostInput(title="Hello, Blog World!"), data_dir, TODAY)

    assert target.name == "hello_blog_world.md"


def test_create_post_refuses_duplicate_id(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    create_post(PostInput(title="Same title"), data_dir, TODAY)

    with pytest.raises(FileExistsError):
        create_post(PostInput(title="Same title"), data_dir, TODAY)


def test_create_post_requires_existing_data_directory(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="data"):
        create_post(PostInput(title="A post"), tmp_path / "data", TODAY)


def test_create_post_refuses_title_without_word_characters(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    with pytest.raises(ValueError, match="title"):
        create_post(PostInput(title="!!!"), data_dir, TODAY)
