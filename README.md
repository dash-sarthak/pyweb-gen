# pyweb-gen

A minimal static site generator for blogs, written in Python. Posts are Markdown
files with YAML front matter; rendering needs no external tools.

## Requirements

* Python 3.11 or newer

## Install

From PyPI once published:

    pip install pyweb-gen

From source:

    git clone https://github.com/dash-sarthak/pyweb-gen.git && cd pyweb-gen
    pip install .

## Usage

    mkdir my-blog && cd my-blog
    pyweb-gen init --name "My Blog"
    pyweb-gen new-post --title "My first post" --description "About this blog"
    pyweb-gen refresh
    pyweb-gen serve

`init` scaffolds the current directory with the default theme: templates,
styles, assets, an empty `data/` directory for posts, and `pages/` for rendered
output. It refuses to overwrite an existing blog. `--name` (or `-n`) sets the
blog name shown in the nav and browser titles; it defaults to `Blog`.

`new-post` writes a Markdown file into `data/`. Edit it with any text editor.

`refresh` renders posts that have no page in `pages/` yet and rebuilds
`index.html` with the newest post first.

`serve` previews the built blog at http://localhost:8000. Pass `--port` to
change the port.

### Front matter

`new-post` writes the metadata block; you edit the body below it:

    ---
    title: "My first post"
    description: "About this blog"
    author: "Sarthak Dash"
    date: "2026-09-07"
    id: "my_first_post"
    img: ""
    ---

`title` is required. `date` must be an ISO date (`YYYY-MM-DD`) for the home
page ordering; other formats display verbatim and sort last. `img` is
optional; the templates render the image only when it is set.

### Site config

`init` writes `blog.yaml` at the blog root:

    name: My Blog

Edit the name any time and run `refresh`; every page picks it up.

### Upgrading from 1.x

Rendering no longer uses pandoc, and templates are Jinja2 now. Bring your old
`templates/` over by hand, or scaffold a fresh directory and move your posts
across. Posts written by 1.x render fine; convert their `date` field to ISO
to get newest-first ordering on the home page.

## Development

    python3 -m venv .venv
    .venv/bin/pip install -r requirements.txt -r requirements-dev.txt
    .venv/bin/pip install -e .

    .venv/bin/python -m pytest
    ruff check .
    .venv/bin/python -m mypy pyweb_gen

CI runs the same checks on Python 3.11 through 3.14.

Runtime dependencies, and why they exist: `jinja2` for templating,
`markdown-it-py` for CommonMark rendering, `python-frontmatter` for YAML front
matter parsing, `PyYAML` for the site config file.
