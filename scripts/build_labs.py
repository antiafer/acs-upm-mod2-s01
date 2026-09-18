"""Builds the student and instructor notebooks from the master notebooks.

    python scripts/build_labs.py

The master notebooks live in master/ and hold the answers, so that folder is not
published. Edit them like any other notebook, in Jupyter or in Colab, wrapping
each answer in the nbgrader marker pair:

    ### BEGIN SOLUTION
    result = frame.groupby(key).mean()
    ### END SOLUTION

This script then writes two versions of every master notebook:

    notebooks/<name>.ipynb            published; each answer becomes a gap
    solutions/<name>_SOLUTION.ipynb   kept private; the markers are removed

Outputs are stripped from both, so no execution result is ever published.
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER = os.path.join(BASE, "master")
STUDENT = os.path.join(BASE, "notebooks")
INSTRUCTOR = os.path.join(BASE, "solutions")

BLOCK = re.compile(r"^[ \t]*### BEGIN SOLUTION[ \t]*\n(.*?)^[ \t]*### END SOLUTION[ \t]*\n?",
                   re.S | re.M)
MARKER = re.compile(r"^[ \t]*### (?:BEGIN|END) SOLUTION[ \t]*\n?", re.M)


def gap(match):
    """Replace one answer with the gap, keeping the indentation of its first line."""
    first = next((l for l in match.group(1).split("\n") if l.strip()), "")
    indent = first[: len(first) - len(first.lstrip())]
    return f"{indent}# YOUR CODE HERE\n{indent}raise NotImplementedError\n"


def build(path, student):
    nb = json.load(open(path, encoding="utf-8"))
    n = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        cell["outputs"], cell["execution_count"] = [], None
        src = cell["source"]
        src = "".join(src) if isinstance(src, list) else src
        n += len(BLOCK.findall(src))
        cell["source"] = BLOCK.sub(gap, src) if student else MARKER.sub("", src)
    name = os.path.basename(path)
    if student:
        out = os.path.join(STUDENT, name)
    else:
        out = os.path.join(INSTRUCTOR, name.replace(".ipynb", "_SOLUTION.ipynb"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return out, n


def main():
    if not os.path.isdir(MASTER):
        sys.exit(f"No master/ folder at {MASTER}. It holds the source notebooks.")
    masters = sorted(f for f in os.listdir(MASTER) if f.endswith(".ipynb"))
    if not masters:
        sys.exit("master/ has no notebooks.")
    for name in masters:
        path = os.path.join(MASTER, name)
        for student in (True, False):
            out, n = build(path, student)
            print(f"{os.path.relpath(out, BASE):<50} {n} exercises")


if __name__ == "__main__":
    main()
