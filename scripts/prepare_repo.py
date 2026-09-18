"""Stamps the GitHub repository URL across the material and rebuilds what depends on it.

    python scripts/prepare_repo.py https://github.com/ORG/acs-upm-mod2-s01

It rewrites REPO in the master notebooks, rebuilds both versions of each lab, and writes the
"Open in Colab" links into README.md and DEPLOY.md. Run it once, before the first push.
"""
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOKS = ["Lab_1_1_reading_files.ipynb", "Lab_1_2_object_and_field.ipynb"]
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"


def normalise(url):
    url = url.strip().rstrip("/")
    url = re.sub(r"\.git$", "", url)
    url = re.sub(r"^git@github\.com:", "https://github.com/", url)
    if not url.startswith("http"):
        url = re.sub(r"^(www\.)?github\.com/", "", url)
        url = "https://github.com/" + url.lstrip("/")
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)$", url)
    if not m:
        sys.exit(f"Not a GitHub repository URL: {url}")
    return url, m.group(1), m.group(2)


def colab_link(org, repo, notebook, branch="main"):
    return (f"https://colab.research.google.com/github/{org}/{repo}/blob/{branch}/"
            f"notebooks/{notebook}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    url, org, repo = normalise(sys.argv[1])
    branch = sys.argv[2] if len(sys.argv) > 2 else "main"

    master = os.path.join(BASE, "master")
    if not os.path.isdir(master):
        sys.exit(f"No master/ folder at {master}. It holds the source notebooks.")
    stamped = 0
    for name in sorted(os.listdir(master)):
        if not name.endswith(".ipynb"):
            continue
        path = os.path.join(master, name)
        src = open(path, encoding="utf-8").read()
        if not re.search(r'REPO = \\"[^"]*\\"', src):
            continue
        open(path, "w", encoding="utf-8").write(
            re.sub(r'REPO = \\"[^"]*\\"', f'REPO = \\"{url}.git\\"', src))
        stamped += 1
    if not stamped:
        sys.exit("Could not find a REPO line in any master notebook.")
    builder = os.path.join(BASE, "scripts", "build_labs.py")
    subprocess.run([sys.executable, builder], check=True, cwd=BASE)

    links = "\n".join(
        f"- [{n}]({colab_link(org, repo, n, branch)})  "
        f"[![Open in Colab]({BADGE})]({colab_link(org, repo, n, branch)})"
        for n in NOTEBOOKS)
    block = f"<!-- COLAB -->\n## Open the labs in Colab\n\n{links}\n<!-- /COLAB -->"
    for name in ("README.md", "DEPLOY.md"):
        path = os.path.join(BASE, name)
        text = open(path, encoding="utf-8").read()
        if "<!-- COLAB -->" in text:
            text = re.sub(r"<!-- COLAB -->.*?<!-- /COLAB -->", block, text, flags=re.DOTALL)
        else:
            text = text.rstrip() + "\n\n" + block + "\n"
        open(path, "w", encoding="utf-8").write(text)

    print(f"Repository: {url}  (branch {branch})")
    print("Notebooks rebuilt with REPO set; Colab links written to README.md and DEPLOY.md.\n")
    for n in NOTEBOOKS:
        print("  " + colab_link(org, repo, n, branch))


if __name__ == "__main__":
    main()
