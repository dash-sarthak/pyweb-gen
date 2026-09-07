"""Create markdown post files from post input."""

import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from pyweb_gen.rendering import DEFAULT_AUTHOR

_SLUG_SEPARATOR = re.compile(r"[^a-z0-9]+")


@dataclass(frozen=True)
class PostInput:
    title: str
    description: str = ""
    image_path: str = ""


def _slugify(title: str) -> str:
    slug = _SLUG_SEPARATOR.sub("_", title.lower()).strip("_")
    if not slug:
        raise ValueError(f"title has no word characters: {title!r}")
    return slug


def _front_matter(post: PostInput, post_id: str, today: date) -> str:
    fields = [
        ("title", post.title),
        ("description", post.description),
        ("author", DEFAULT_AUTHOR),
        ("date", today.isoformat()),
        ("id", post_id),
        ("img", post.image_path),
    ]
    lines = ["---"]
    lines.extend(f"{name}: {json.dumps(value)}" for name, value in fields)
    lines.append("---")
    return "\n".join(lines)


def create_post(post: PostInput, data_dir: Path, today: date) -> Path:
    """Write one markdown post with front matter; returns its path."""
    if not data_dir.is_dir():
        raise FileNotFoundError(f"blog data directory does not exist: {data_dir}")

    post_id = _slugify(post.title)
    target = data_dir / f"{post_id}.md"
    if target.exists():
        raise FileExistsError(f"post already exists: {target}")

    target.write_text(f"{_front_matter(post, post_id, today)}\n", encoding="utf-8")
    return target
