# Publishing

Releases use GitHub Actions and PyPI Trusted Publishing. No PyPI token belongs
in GitHub secrets or repository files.

## One-time PyPI setup

Before the first tag, sign in to PyPI and create a pending trusted publisher
with these exact values:

- PyPI project name: `broute-j11`
- GitHub owner: `jethac`
- GitHub repository: `broute-j11`
- Workflow filename: `publish.yml`
- Environment name: `pypi`

The repository's GitHub environment is already named `pypi`. PyPI creates the
project when the pending publisher successfully handles the first release.

## Release

1. Confirm `main` is green and the version in `pyproject.toml` matches the
   changelog.
2. Create and push the matching annotated tag, for example `v0.1.0`.
3. Wait for the `Publish to PyPI` workflow. It reruns all CI, checks that the
   tagged commit belongs to `main`, checks tag/version equality, inspects both
   distributions, and publishes through OIDC.
4. Install the exact release from PyPI in a clean environment and run a public-
   API import smoke test.
5. Create the matching GitHub release and attach the wheel and sdist SHA-256
   hashes.

Do not push a release tag until the pending publisher exists: a failed first
publication consumes time without increasing confidence and the tag should
remain an immutable release identifier.
