"""Rendering: front matter parsing, markdown rendering, template output."""

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import frontmatter
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt
from markupsafe import Markup

DEFAULT_AUTHOR = "Sarthak Dash"

_MONTHS = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)

# html stays off: raw HTML in posts must escape; Markup() bypasses autoescape downstream.
_MARKDOWN = MarkdownIt(options_update={"html": False})


@dataclass(frozen=True)
class BlogLayout:
    templates_dir: Path
    data_dir: Path
    pages_dir: Path
    index_path: Path

    @classmethod
    def from_root(cls, root: Path) -> "BlogLayout":
        return cls(
            templates_dir=root / "templates",
            data_dir=root / "data",
            pages_dir=root / "pages",
            index_path=root / "index.html",
        )


@dataclass(frozen=True)
class PostSource:
    id: str
    title: str
    description: str
    author: str
    date: str
    image_path: str
    body_markdown: str

    @property
    def date_display(self) -> str:
        parsed = _parse_iso_date(self.date)
        if parsed is None:
            return self.date
        return f"{parsed.day:02d} {_MONTHS[parsed.month - 1]}, {parsed.year}"


def _parse_iso_date(raw: str) -> date | None:
    try:
        return date.fromisoformat(raw)
    except ValueError:
        return None


def load_post(path: Path) -> PostSource:
    """Parse one markdown file; the title is mandatory."""
    post = frontmatter.load(path)
    title = post.get("title")
    if not title:
        raise ValueError(f"{path}: front matter must set a title")

    return PostSource(
        id=str(post.get("id") or path.stem),
        title=str(title),
        description=str(post.get("description") or ""),
        author=str(post.get("author") or DEFAULT_AUTHOR),
        date=str(post.get("date") or ""),
        image_path=str(post.get("img") or ""),
        body_markdown=post.content,
    )


def sort_posts_newest_first(posts: list[PostSource]) -> list[PostSource]:
    """Order dated posts newest first; undated posts keep filename order at the end."""
    dated = [post for post in posts if _parse_iso_date(post.date) is not None]
    undated = [post for post in posts if _parse_iso_date(post.date) is None]
    dated.sort(key=lambda post: (_parse_iso_date(post.date), post.id), reverse=True)
    return dated + undated


def _environment(templates_dir: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(),
    )


def render_post(post: PostSource, layout: BlogLayout) -> str:
    """Render one post through the packaged post template."""
    template = _environment(layout.templates_dir).get_template("post_template.html")
    return template.render(
        title=post.title,
        author=post.author,
        date_display=post.date_display,
        image_path=post.image_path,
        body=Markup(_MARKDOWN.render(post.body_markdown)),
    )


def render_home(posts: list[PostSource], layout: BlogLayout) -> str:
    """Render the home page listing posts newest first."""
    template = _environment(layout.templates_dir).get_template("home_template.html")
    return template.render(posts=sort_posts_newest_first(posts))
