# STATE.md — live session state

Updated at session close per AGENTS.md. Facts only; history lives in git log, backlog lives in GitHub issues. omp sessions get this auto-injected; every other agent reads the file.

## Repo and location

pyweb-gen. Remote: github.com/dash-sarthak/pyweb-gen (ssh). Branch protection on main: required check `ci` (strict), pull requests required, no force pushes. Repo settings: merge commits only, squash and rebase disabled, branch deleted on merge.

## Last merged

chore/8 — state update after the v2.0.0 release. Before it, PR #7 (gh-6: escape raw HTML in post bodies, regression test landed red first) and tag v2.0.0 published pyweb-gen to PyPI.

## In flight

Nothing unmerged.

## Open questions for the user

1. File the pre-flight hardening candidates as issues? (a) front-matter `id` is unvalidated, so `id: ../../x` in hand-edited front matter writes the rendered page outside `pages/`; (b) `serve` binds 0.0.0.0, so the preview is reachable from the LAN. Both author-controlled, low severity.
2. `pyproject.toml` declares no license, so the PyPI page shows none.

## Next action

Release complete: pyweb-gen 2.0.0 is live at pypi.org/project/pyweb-gen/ (issue #2 closed). No scheduled work; next actions come from the open questions above.

## Tracker

Open: none. Closed: #1 and #2 (release), #6 (raw HTML escaping), #8 (this update).
