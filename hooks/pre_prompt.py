import subprocess
import sys
from cookiecutter.config import get_config

def update_config(uv_version):
    config = get_config("cookiecutter.json")
    config["uv_version"] = uv_version.split(" ")[1]

def test_for_uv():
    try:
        result = subprocess.run(['uv', '--version'], capture_output=True, check=True)
        return result.stdout.decode().strip()
    except FileNotFoundError:
        return False

def main():
    if uv_version := test_for_uv():
        update_config(uv_version)
    else:
        print('Please install uv')
        sys.exit(1)

if __name__ == "__main__":
    main()