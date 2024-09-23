import subprocess
import sys

def test_for_uv():
    try:
        subprocess.run(['uv', '--version'], capture_output=True, check=True)
        return True
    except FileNotFoundError:
        return False

def main():
    if not test_for_uv():
        print('Please install uv')
        sys.exit(1)

if __name__ == "__main__":
    main()