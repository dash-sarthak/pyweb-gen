"""Rebuild the blog from markdown sources."""

from pathlib import Path

from pyweb_gen.rendering import BlogLayout, load_post, render_home, render_post


def refresh_blog(root: Path) -> list[str]:
    """Render posts missing from pages/, rebuild the home page; returns new ids."""
    layout = BlogLayout.from_root(root)
    sources = sorted(layout.data_dir.glob("*.md"))
    posts = [load_post(source) for source in sources]

    new_pages: list[str] = []
    for post in posts:
        page = layout.pages_dir / f"{post.id}.html"
        if not page.exists():
            page.write_text(render_post(post, layout), encoding="utf-8")
            new_pages.append(post.id)

    layout.index_path.write_text(render_home(posts, layout), encoding="utf-8")
    return new_pages
