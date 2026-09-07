# STATE.md — live session state

Updated at session close per AGENTS.md. Facts only; history lives in git log, backlog lives in GitHub issues. omp sessions get this auto-injected; every other agent reads the file.

## Repo and location

pyweb-gen. Remote: none yet — add `origin`, then enable branch protection (required status check `ci`, pull requests required, merge commits, no squash) before the first PR.

## Last merged

Nothing yet (no remote). Modernization landed as eight gh-0 commits on local main, all checks green.

## In flight

Nothing uncommitted. Post-remote follow-ups: open issues, configure the PyPI trusted publisher, tag v2.0.0.

## Open questions for the user

Which GitHub repository to use as `origin`.

## Next action

1. Create the GitHub repo and add it as `origin`, push main.
2. Open issues for follow-up work, enable branch protection with `ci` as the required check.
3. Configure the PyPI trusted publisher on the `pypi` environment, then tag v2.0.0 to publish.
