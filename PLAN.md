# pyweb-gen — plan

Dated planning entries, newest first. One `## YYYY-MM-DD` heading per planning session. Planning precedes implementation for non-trivial work: state the goal, the approach, and how the result gets verified. Entries are append-only after the session closes; corrections arrive as new dated entries.

## Entries

## 2026-09-08 — Site naming, skeuomorphic restyle, demo blog

Goal. The scaffold hardcodes the blog name "Quill" in six places, so users cannot name their blog. The user wants a naming mechanism (default "Blog"), a cleaner look with a slight skeuomorphic design, and a dummy blog with tech posts about the tool to exercise it all.

Decisions. The name lives in `blog.yaml` at the blog root (`name: Blog`), written by `init` (with an `--name` flag) and read by `refresh`; templates render `site_name` from it. Parsing uses PyYAML, promoted from transitive to declared dependency since the config reads it directly. The restyle is CSS-only: the Google Fonts import goes away for a system serif stack, and the shared nav/paper rules move into one `base.css` instead of being duplicated across the two stylesheets. The demo blog lives in gitignored `demo/`.

Approach. One issue, one branch, one PR: config mechanism with boundary tests first, then template and CSS rework, then demo content.

Verification. pytest, ruff, ruff format, and strict mypy green; demo site built with the new scaffold and inspected in a real browser (home and post screenshots); full wheel build before opening the PR; CI green before merge.

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

## 2026-09-07 — Modernization executed: outcome and deviations

The 2026-09-07 plan above is implemented. All units landed as local commits on main
(gh-0, pre-tracker); no remote exists yet, so the issue/branch/PR flow starts after
push. Verification: 34 pytest tests, ruff, ruff format, and mypy --strict all green;
wheel builds clean; a smoke run in a temp directory exercised init, new-post,
refresh (including re-render after an edit), and serve over loopback HTTP.

Deviations from the plan, in commit order:

1. Scaffold and renderer units merged into one commit for a clean cutover: shipping
   Jinja2 templates while `refresh` still shelled out to pandoc would have broken
   the tree between commits. Same for renderer and state: pandoc and
   beautifulsoup4 could only be removed once `refresh_blog.py` was rewritten.
2. Refresh went one step beyond the existence diff the plan described: a page
   re-renders when its rendered output differs from the stored file, so editing a
   post and refreshing updates the site. Pure existence diffing would have kept the
   v1 gotcha where edits never appear.
3. Unit 5 (determinism and hygiene) dissolved into the rewrites rather than being a
   separate pass: injected clock at the composition edge (`datetime.now(UTC).date()`
   in `cli.py` only), pathlib throughout, no `os.system`, no `sys.exit` in library
   code, type-annotated under mypy strict.
4. The `main()` CLI returns a status code instead of raising; the pip console
   wrapper converts it to an exit code. Errors print one `error: ...` line to
   stderr and exit 1.
5. CI gained a mypy step and the publish workflow uses PyPI trusted publishing
   (`environment: pypi`, id-token write); the PyPI side of trusted publishing still
   needs a one-time setup by the repo owner after the remote exists.

Dependency changes and reasons: added `jinja2==3.1.6` (templating),
`markdown-it-py==4.2.0` (CommonMark rendering), `python-frontmatter==1.3.0` (YAML
front matter); removed `beautifulsoup4` (its only job was splicing HTML at line 26
of index.html, replaced by template rendering) and dropped the pandoc binary
dependency. `requirements-dev.txt` pins build, mypy, pytest, ruff.

Remaining before release: create the GitHub remote, push, open issues for follow-up
work, enable branch protection with `ci` as the required check, and configure the
PyPI trusted publisher once, then tag v2.0.0.
