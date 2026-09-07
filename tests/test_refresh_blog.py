"""Blog refresh: renders new posts, rebuilds the home page, stays idempotent."""

from pathlib import Path

import pytest

from pyweb_gen.initialize import initialize
from pyweb_gen.refresh_blog import refresh_blog


def _make_blog(tmp_path: Path) -> Path:
    initialize(tmp_path)
    return tmp_path


def _write_post(root: Path, post_id: str, title: str, date: str) -> None:
    (root / "data" / f"{post_id}.md").write_text(
        f"---\ntitle: {title}\ndate: {date}\nid: {post_id}\n---\n\nhello **world**\n",
        encoding="utf-8",
    )


def test_refresh_renders_new_posts_and_rebuilds_home(tmp_path: Path) -> None:
    root = _make_blog(tmp_path)
    _write_post(root, "a_post", "A post", "2026-09-07")

    new_pages = refresh_blog(root)

    assert new_pages == ["a_post"]
    page = (root / "pages" / "a_post.html").read_text(encoding="utf-8")
    assert "<strong>world</strong>" in page
    index = (root / "index.html").read_text(encoding="utf-8")
    assert "pages/a_post.html" in index


def test_refresh_without_new_posts_changes_nothing(tmp_path: Path) -> None:
    root = _make_blog(tmp_path)
    _write_post(root, "a_post", "A post", "2026-09-07")
    refresh_blog(root)
    index_before = (root / "index.html").read_text(encoding="utf-8")
    page_before = (root / "pages" / "a_post.html").read_text(encoding="utf-8")

    new_pages = refresh_blog(root)

    assert new_pages == []
    assert (root / "index.html").read_text(encoding="utf-8") == index_before
    assert (root / "pages" / "a_post.html").read_text(encoding="utf-8") == page_before


def test_refresh_renders_only_missing_pages(tmp_path: Path) -> None:
    root = _make_blog(tmp_path)
    _write_post(root, "a_post", "A post", "2026-09-07")
    _write_post(root, "b_post", "B post", "2026-09-06")
    refresh_blog(root)
    (root / "pages" / "b_post.html").unlink()

    new_pages = refresh_blog(root)

    assert new_pages == ["b_post"]
    assert (root / "pages" / "b_post.html").is_file()


def test_refresh_lists_home_newest_first(tmp_path: Path) -> None:
    root = _make_blog(tmp_path)
    _write_post(root, "older_post", "Older", "2026-01-01")
    _write_post(root, "newer_post", "Newer", "2026-09-07")

    refresh_blog(root)

    index = (root / "index.html").read_text(encoding="utf-8")
    assert index.index("pages/newer_post.html") < index.index("pages/older_post.html")


def test_refresh_on_fresh_blog_renders_empty_home(tmp_path: Path) -> None:
    root = _make_blog(tmp_path)

    new_pages = refresh_blog(root)

    assert new_pages == []
    index = (root / "index.html").read_text(encoding="utf-8")
    assert "Quill | Home" in index


def test_refresh_ignores_non_markdown_files(tmp_path: Path) -> None:
    root = _make_blog(tmp_path)
    (root / "data" / "notes.txt").write_text("not a post", encoding="utf-8")

    new_pages = refresh_blog(root)

    assert new_pages == []


def test_refresh_names_file_missing_front_matter_title(tmp_path: Path) -> None:
    root = _make_blog(tmp_path)
    (root / "data" / "broken.md").write_text("no front matter\n", encoding="utf-8")

    with pytest.raises(ValueError, match="broken"):
        refresh_blog(root)
