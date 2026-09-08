# STATE.md — live session state

Updated at session close per AGENTS.md. Facts only; history lives in git log, backlog lives in GitHub issues. omp sessions get this auto-injected; every other agent reads the file.

## Repo and location

pyweb-gen. Remote: github.com/dash-sarthak/pyweb-gen (ssh). Branch protection on main: required check `ci` (strict), pull requests required, no force pushes. Repo settings: merge commits only, squash and rebase disabled, branch deleted on merge.

## Last merged

chore/12 — state update after the site naming and restyle feature. Before it, PR #11 (gh-10: blog.yaml site name with `init --name`, paper-and-ink scaffold restyle, demo blog in gitignored `demo/`).

## In flight

Nothing unmerged.

## Open questions for the user

1. File the pre-flight hardening candidates as issues? (a) front-matter `id` is unvalidated, so `id: ../../x` in hand-edited front matter writes the rendered page outside `pages/`; (b) `serve` binds 0.0.0.0, so the preview is reachable from the LAN. Both author-controlled, low severity.
2. `pyproject.toml` declares no license, so the PyPI page shows none.
3. Tag a follow-up release? The published 2.0.0 predates gh-10; shipping the restyle needs a version bump in `pyproject.toml` and a new tag.

## Next action

pyweb-gen 2.0.0 is live at pypi.org/project/pyweb-gen/. No scheduled work; next actions come from the open questions above.

## Tracker

Open: none. Closed: #1, #2 (release), #6 (raw HTML escaping), #8 (state update), #10 (naming and restyle), #12 (this update).
