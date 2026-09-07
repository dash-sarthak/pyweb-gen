# pyweb-gen — plan

Dated planning entries, newest first. One `## YYYY-MM-DD` heading per planning session. Planning precedes implementation for non-trivial work: state the goal, the approach, and how the result gets verified. Entries are append-only after the session closes; corrections arrive as new dated entries.

## Entries

## 2026-09-07 — Modernization: pure-Python rendering, PyPI, tests, CI

Goal. Bring this 2022 codebase up to the standards the repo's own manual sets: installable from PyPI, no external pandoc binary, user state kept in the blog project instead of site-packages, a real test suite, CI that can actually pass, and tagged releases.

Decisions (user, this session). The renderer becomes pure Python, so pandoc goes away. Distribution moves to PyPI; `pyweb-gen` and the normalized `pywebgen` both returned 404 from the PyPI JSON API on this date, so the name is free. Scope includes small wins (`serve` command, better CLI errors) alongside the overhaul.

Approach, as a PR sequence. Each item is one issue, one branch, one PR. Issues require a remote, so item 1 creates it first.

1. chore: remote and packaging skeleton. Create the GitHub remote and push main (gh-0 commits). Replace the metadata split (`setup.cfg` plus a bare `pyproject.toml`) with full PEP 621 metadata: `requires-python >= 3.11` (3.9 is EOL, 3.10 EOLs Oct 2026), runtime deps separated from dev deps, entry point as a plain function instead of the `pyweb_gen:CLIHandler` class instantiated for side effects. Fix CI to install the package editable and add the missing `requirements-dev.txt`.
2. feat: package-embedded scaffold. Move templates and starter content from the cloned `assets` branch into `pyweb_gen/` as package data. `init` copies from the installed package; the `git clone` dependency and the `os.system("rm -rf ...")` cleanup disappear. No network at init.
3. feat: pure-Python renderer. Port the post and home templates to Jinja2, render posts with markdown-it-py, parse the `---` metadata block with python-frontmatter. Reasons over lighter options: front matter holds YAML-shaped values that need real YAML parsing, and markdown-it-py is CommonMark compliant. Remove pandoc and beautifulsoup4. `index.html` renders from post metadata instead of splicing a snippet at line 26.
4. fix: project-local state. Delete both `created_pages.txt` files. Refresh derives new posts by diffing `data/*.md` against `pages/*.html`. This removes the runtime mutation of site-packages and the existing read/write mismatch (refresh writes `pyweb_gen/created_pages.txt`, refresh reads `pyweb_gen/utils/created_pages.txt`, and each write clobbers the file with a single page name).
5. refactor: determinism and hygiene. Inject a clock into `NewPost` (currently `datetime.now()` in library code). Replace `os.system` calls with pathlib/shutil. Fix the wrong `Union[bool, list]` annotation (the method returns a tuple) and `str = None` defaults. No `sys.exit()` inside library classes; raise, and let the CLI translate to exit codes.
6. test: pytest suite covering parser, new-post with a fake clock, init from package data, and refresh boundaries: empty blog, first post, idempotent second refresh, invalid front matter. No network, no real clock, per the manual.
7. feat: serve command and CLI polish. `pyweb-gen serve` previews the built blog via `http.server`. Clear error messages and exit codes. README rewritten for `pip install pyweb-gen` with no pandoc prerequisite.
8. ci/publish: publish workflow using PyPI trusted publishing on tag, version bumped to 2.0.0 (breaking: renderer and install model change), branch protection on main with CI as the required check.

Verification. Every PR runs `ruff check .` and the full pytest suite. After item 7, a smoke run in a temp directory exercises init, new-post, refresh, and serve end to end. A built wheel installed into a fresh venv repeats the flow before the publish workflow is enabled.
