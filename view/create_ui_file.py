import os.path
import subprocess
import sys




if __name__ == "__main__":
    exe = os.path.abspath("../venv/Scripts/pyside6-uic.exe")
    filename = "look_triples_view"

    cmd = f"{exe} ui/{filename}.ui -o {filename}.py"

    cp = subprocess.run(cmd, capture_output=True, universal_newlines=True)

    if cp.returncode != 0:
        print(cp.stderr)












