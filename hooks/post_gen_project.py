import subprocess
import shutil
from pathlib import Path


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
        "tailwindcss"
        "@tailwindcss/cli"
    ]

    subprocess.run(['/bin/bash', '-i', '-c', f'curl -fsSL https://bun.sh/install | bash'])

    for dep in base_deps:
        subprocess.run(['bun', 'add', dep])


def setup_python():
    print("Setting up Python")
    subprocess.run(['make', 'update_requirements'])


def setup_local_py():
    print("Setting up local.py")
    Path("./{{cookiecutter.project_app}}/settings/local.example.py")\
        .rename("./{{cookiecutter.project_app}}/settings/local.py")


def main():
    print("Running post generation tasks.")
    clean_project()
    setup_local_py()
    setup_node()
    setup_python()


if __name__ == "__main__":
    main()
