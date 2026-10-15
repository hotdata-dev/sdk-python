# Releasing

Every release uses `./scripts/release.sh`. Do not bump versions, tag, or create GitHub Releases manually.

## One-time setup

- Install [GitHub CLI](https://cli.github.com/) (`gh`) and authenticate.
- Ensure PyPI [trusted publishing](https://docs.pypi.org/trusted-publishers/) is configured for this repo (`publish.yml` uses the `pypi` GitHub environment).

## Release steps

Releases are cut in CI by the `Cut Release` workflow (`cut-release.yml`). It runs
the same `./scripts/release.sh` a person would, as the Hotdata automation app.

1. Make sure `## [Unreleased]` in `CHANGELOG.md` has user-facing notes.
2. Trigger the workflow with the bump kind or an explicit version:

   ```bash
   gh workflow run cut-release.yml -f bump=minor   # or patch | major | 1.2.3
   ```

   The `prepare` job runs `release.sh prepare`, which opens the
   `release/vX.Y.Z` PR with auto-merge enabled.
3. The PR merges on its own once CI and the review gate pass. Merging it runs
   the `publish` job, which runs `release.sh publish` and pushes the `vX.Y.Z`
   tag.

That is the whole process. Running the script locally still works and does the
same thing, but is not the normal path.

## What happens automatically

Pushing the `vX.Y.Z` tag triggers two workflows:

| Workflow | Purpose |
|----------|---------|
| `publish.yml` | Build wheel/sdist and publish to PyPI |
| `release.yml` | Create the GitHub Release with notes from `CHANGELOG.md` |

## Retry a failed PyPI publish

If the publish workflow failed *before* PyPI accepted the upload — a stale action
pin, a PyPI outage — re-run it against the same tag rather than deleting the tag
or burning a version number:

```bash
gh workflow run "Publish to PyPI" --ref main -f tag=vX.Y.Z
```

`--ref main` selects the workflow *definition*, so a fix landed since the tag is
picked up; the `tag` input selects what gets built and published.

Only safe while the version is unpublished. PyPI refuses to replace an existing
file, so a retry after a successful upload fails at the upload step rather than
overwriting. Check first:

```bash
curl -s -o /dev/null -w '%{http_code}' https://pypi.org/pypi/hotdata/X.Y.Z/json
```

404 means the version is still free.

## Recover a missing GitHub Release

If PyPI publish succeeded but the GitHub Release workflow failed, rerun it from `main`
without retagging:

```bash
gh workflow run "GitHub Release" --ref main -f tag=vX.Y.Z
```

The tag must already exist on the remote. The workflow checks out that tag, extracts the
matching `CHANGELOG.md` section, and creates or updates the GitHub Release.

## Enforcement

- **PR check** (`check-release.yml`): if `pyproject.toml` version changes, `CHANGELOG.md` must contain a matching `## [X.Y.Z]` section.
- **Tag check** (`publish.yml`): the tag (without `v`) must match `[project].version` in `pyproject.toml`.
- **Publish guard** (`release.sh publish`): refuses to tag if the changelog section is missing.

Together, these make it hard to ship a version without changelog notes or a GitHub Release.
