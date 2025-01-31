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


def setup_node():
    print("Setting up Bun")
    base_deps = [
        "alpinejs",
        "tailwindcss",
    ]

    dev_deps = [
        "esbuild"
    ]

    subprocess.run(['/bin/bash', '-i', '-c', f'curl -fsSL https://bun.sh/install | bash'])

    for dep in base_deps:
        subprocess.run(['bun', 'add', dep])

    for dep in dev_deps:
        subprocess.run(['bun', 'add', '--development', dep])


def setup_python():
    print("Setting up Python")
    subprocess.run(['make', 'update_requirements'])


def main():
    print("Running post generation tasks.")
    clean_project()
    setup_node()
    setup_python()


if __name__ == "__main__":
    main()
