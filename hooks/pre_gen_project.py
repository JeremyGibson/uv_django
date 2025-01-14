import sys

import requests
from cookiecutter.main import cookiecutter

PRE_COMMIT_REPOS = {
    "black": {
        "url": "https://api.github.com/repos/psf/black/releases",
        "default_version": "24.10.0"
    },
    "ruff": {
        "url": "https://api.github.com/repos/psf/ruff/releases",
        "default_version": "0.9.1"
    },
    "isort": {
        "url": "https://api.github.com/repos/pycqa/isort/releases/latest",
        "default_version": "5.11.2"
    },
    "pre-commit-hooks": {
        "url": "https://api.github.com/repos/pre-commit/pre-commit-hooks",
        "default_version": "5.0.0"
    }
}

def set_pre_commit_config():
    extra_context = {}
    for key, value in PRE_COMMIT_REPOS.items():
        response = requests.get(value["url"])
        if response.status_code != 200:
            version = value["default_version"]
        else:
            try:
                version = response.json()[0]['tag_name']
            except (KeyError, IndexError):
                version = value["default_version"]
        extra_context[key] = version
    breakpoint()
    cookiecutter(
        "uv_django",
        extra_context=extra_context,
    )

if __name__ == '__main__':
    set_pre_commit_config()