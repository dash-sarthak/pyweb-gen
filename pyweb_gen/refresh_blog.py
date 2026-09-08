"""Rebuild the blog from markdown sources."""

from pathlib import Path

from pyweb_gen.rendering import (
    BlogLayout,
    load_post,
    load_site_config,
    render_home,
    render_post,
)


def _write_if_changed(path: Path, content: str) -> bool:
    if path.is_file() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def refresh_blog(root: Path) -> list[str]:
    """Render posts whose page is missing or stale; returns the rendered ids."""
    layout = BlogLayout.from_root(root)
    site = load_site_config(root)
    sources = sorted(layout.data_dir.glob("*.md"))
    posts = [load_post(source) for source in sources]

    rendered: list[str] = []
    for post in posts:
        page = layout.pages_dir / f"{post.id}.html"
        if _write_if_changed(page, render_post(post, layout, site)):
            rendered.append(post.id)

    _write_if_changed(layout.index_path, render_home(posts, layout, site))
    return rendered
