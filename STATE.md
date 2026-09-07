# STATE.md — live session state

Updated at session close per AGENTS.md. Facts only; history lives in git log, backlog lives in GitHub issues. omp sessions get this auto-injected; every other agent reads the file.

## Repo and location

pyweb-gen. Remote: github.com/dash-sarthak/pyweb-gen (ssh). Branch protection on main: required check `ci` (strict), pull requests required, no force pushes. Repo settings: merge commits only, squash and rebase disabled, branch deleted on merge.

## Last merged

chore/1 — first PR after modernization; main holds eight gh-0 commits (packaging, pure-Python renderer, project-local state, serve command, publish workflow) plus this state update.

## In flight

Nothing unmerged.

## Open questions for the user

(none)

## Next action

1. Configure the PyPI trusted publisher (issue #1): add dash-sarthak/pyweb-gen, workflow publish.yml, environment pypi.
2. Tag v2.0.0 to publish (issue #2), then verify pypi.org/project/pyweb-gen/.

## Tracker

Issues #1 and #2 track the release steps.
