## Welcome

Thanks for your interest in contributing to StegoSphere.

## Development Setup

1. Fork and clone the repository.
2. Create a virtual environment and install dependencies.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the app locally.

```bash
python main.py
```

## Branching and Commits

* Use feature branches for all changes.
* Keep commits focused and descriptive.
* Avoid committing generated files or credentials.

## Pull Requests

* Describe what changed and why.
* Include screenshots for UI changes where useful.
* Reference related issues when applicable.
* Ensure your branch is up to date with the target branch before requesting review.

## Code Quality

* Follow PEP 8 for Python code.
* Prefer clear function names and small focused functions.
* Add docstrings for new public functions or classes.
* Handle edge cases and invalid inputs with clear errors.

## Security

* Never commit real SMTP or account credentials.
* Use environment variables (`STEGOSPHERE_*`) for local secrets.
* Report security concerns privately to the maintainer.