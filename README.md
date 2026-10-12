# Task 1: Checking PyPI Dependencies

A Python script that audits dependencies in a `requirements.txt` file against the official [PyPI JSON API](https://docs.pypi.org/api/json) to detect hallucinated or non-existent packages and versions.

## Features

- **Total Dependencies Checked**: Counts the number of dependency entries.
- **Packages Not on PyPI**: Identifies package names that do not exist on PyPI (HTTP 404).
- **Versions Not on PyPI**: Identifies cases where the package exists but the specific pinned version does not (HTTP 404).
- **Oldest Pinned Release**: Finds the oldest valid pinned release based on the upload timestamp of the first file listed under `urls`.

## Usage

Run with the default assignment input:
```bash
python project.py
```

Or pass any `requirements.txt` file as an argument:
```bash
python project.py requirements.txt
```
