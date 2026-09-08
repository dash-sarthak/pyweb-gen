"""Post rendering: front matter parsing, markdown rendering, template output."""

from pathlib import Path

import pytest

from pyweb_gen.initialize import initialize
from pyweb_gen.rendering import (
    BlogLayout,
    PostSource,
    load_post,
    render_home,
    render_post,
)


def _post_without_image(**overrides: str) -> PostSource:
    fields = {
        "id": "a_post",
        "title": "A post",
        "description": "",
        "author": "Test Author",
        "date": "2026-09-07",
        "image_path": "",
        "body_markdown": "",
    }
    fields.update(overrides)
    return PostSource(**fields)


def test_load_post_parses_front_matter_and_body(tmp_path: Path) -> None:
    source = tmp_path / "a_post.md"
    source.write_text(
        "---\n"
        "title: A post\n"
        "description: About testing\n"
        "author: Test Author\n"
        "date: 2026-09-07\n"
        "id: a_post\n"
        "img: cover.png\n"
        "---\n"
        "\n"
        "hello **world**\n",
        encoding="utf-8",
    )

    post = load_post(source)

    assert post.id == "a_post"
    assert post.title == "A post"
    assert post.description == "About testing"
    assert post.author == "Test Author"
    assert post.date == "2026-09-07"
    assert post.image_path == "cover.png"
    assert post.body_markdown.strip() == "hello **world**"


def test_load_post_without_title_raises(tmp_path: Path) -> None:
    source = tmp_path / "broken.md"
    source.write_text("just markdown, no front matter\n", encoding="utf-8")

    with pytest.raises(ValueError, match="broken"):
        load_post(source)


def test_render_post_escapes_title_and_renders_markdown(tmp_path: Path) -> None:
    initialize(tmp_path)
    post = _post_without_image(
        title="Bold <b> & breaking", body_markdown="hello **world**"
    )

    html = render_post(post, BlogLayout.from_root(tmp_path))

    assert "Bold &lt;b&gt; &amp; breaking" in html
    assert "<strong>world</strong>" in html


def test_render_post_escapes_raw_html_in_body(tmp_path: Path) -> None:
    initialize(tmp_path)
    post = _post_without_image(
        title="Raw HTML", body_markdown="hello **world** <img src=x onerror=alert(2)>"
    )

    html = render_post(post, BlogLayout.from_root(tmp_path))

    assert "&lt;img src=x onerror=alert(2)&gt;" in html
    assert "<img src=x onerror" not in html


def test_render_post_includes_image_only_when_set(tmp_path: Path) -> None:
    initialize(tmp_path)

    without_image = render_post(_post_without_image(), BlogLayout.from_root(tmp_path))
    with_image = render_post(
        _post_without_image(image_path="cover.png"), BlogLayout.from_root(tmp_path)
    )

    assert '<img src=""' not in without_image
    assert '<img src="cover.png"' in with_image


def test_render_post_formats_iso_date_for_display(tmp_path: Path) -> None:
    initialize(tmp_path)

    html = render_post(_post_without_image(), BlogLayout.from_root(tmp_path))

    assert "07 September, 2026" in html


def test_render_post_keeps_non_iso_date_verbatim(tmp_path: Path) -> None:
    initialize(tmp_path)
    post = _post_without_image(date="some old date")

    html = render_post(post, BlogLayout.from_root(tmp_path))

    assert "some old date" in html


def test_render_home_lists_posts_newest_first(tmp_path: Path) -> None:
    initialize(tmp_path)
    older = _post_without_image(id="older", title="Older", date="2026-01-01")
    newer = _post_without_image(id="newer", title="Newer", date="2026-09-07")

    html = render_home([older, newer], BlogLayout.from_root(tmp_path))

    assert "pages/newer.html" in html
    assert "pages/older.html" in html
    assert html.index("pages/newer.html") < html.index("pages/older.html")


def test_render_home_with_no_posts_renders_empty_page(tmp_path: Path) -> None:
    initialize(tmp_path)

    html = render_home([], BlogLayout.from_root(tmp_path))

    assert "Quill | Home" in html
    assert "post_preview" not in html
