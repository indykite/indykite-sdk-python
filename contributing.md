# Contributing to IndyKite

We want your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

* Reporting a bug
* Discussing the current state of the code
* Submitting a fix
* Proposing new features
* Becoming a maintainer

## We Develop with GitHub

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [GitHub Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests

Pull requests are the best way to propose changes to the codebase (we use [GitHub Flow](https://guides.github.com/introduction/flow/index.html)). We actively welcome your pull requests:

1. Fork the repo and create your branch from `main / master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Create that pull request!

## Any contributions you make will be under the Apache-2.0 Software License

In short, when you submit code changes, your submissions are understood to be under the same [Apache-2.0](https://choosealicense.com/licenses/apache-2.0/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issues](https://github.com/indykite/indykite-sdk-python/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/indykite/indykite-sdk-python/issues); it's that easy!

## Write bug reports with detail, background, and sample code

Including the following information will tend to make a better bug report:

* A quick summary and/or background
* Steps to reproduce. Be specific!
* Give sample code if you can.
* What you expected would happen
* What actually happens
* Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)
* Version information: SDK version (`python -c "import indykite_sdk; print(indykite_sdk.__version__)"`), Python version, and platform
* Never include credential tokens or credential files

Please provide as much information as possible in your bug reports.

## Development Setup

```sh
pipenv install --dev
pipenv run pytest                  # unit tests (mocked, no credentials needed)
pipenv run pytest -m integration   # live tests (needs credentials, see tests/integration/conftest.py)
pre-commit run --all-files         # linting and formatting
```

Python 3.14+ is required.

## Use a Consistent Coding Style

Formatting and linting are enforced by [pre-commit](https://pre-commit.com/) hooks (ruff is the
primary formatter and linter; configuration lives in `pyproject.toml`). Install the hooks once with
`pre-commit install` and they will keep your changes consistent automatically.

## Pull Request Titles

PR titles must follow [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`,
`chore:`, ...). The squash-merged title becomes the commit message that drives automated releases
(release-please), so a `feat!:` or `BREAKING CHANGE:` marker is what produces a major version bump.

## License

By contributing, you agree that your contributions will be licensed under its Apache-2.0 License.
