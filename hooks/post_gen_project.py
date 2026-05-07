import subprocess
import shutil
from pathlib import Path
import requests
import yaml


def clean_project():
    if "{{cookiecutter.testing_type}}" == "django":
        print("REMOVE: pytest.ini")
        Path(Path().cwd(), "pytest.ini").unlink()

    if "{{cookiecutter.project_type}}" == "django":
        shutil.rmtree((Path("./apps/search")))

    if "{{cookiecutter.include_accessibility_tests}}" == "no":
        Path("./apps/{{cookiecutter.primary_app}}/tests/test_accessibility.py").unlink()

    print("Renaming .envrc")
    Path(Path().cwd(), ".envrc_template").rename(Path(Path().cwd(), ".envrc"))

    print("Creating local.py from local.example.py")
    shutil.copy(
        Path("{{cookiecutter.project_app}}/settings/local.example.py"),
        Path("{{cookiecutter.project_app}}/settings/local.py")
    )


def setup_node():
    print("Setting up Bun")
    # Install Bun if not already installed
    subprocess.run(['/bin/bash', '-i', '-c', f'curl -fsSL https://bun.sh/install | bash'])

    # Install all dependencies from package.json
    subprocess.run(['bun', 'install'])


def setup_python():
    print("Setting up Python")
    subprocess.run(['just', 'update-requirements'])


def main():
    print("Running post generation tasks.")
    clean_project()
    setup_node()
    setup_python()


if __name__ == "__main__":
    main()
