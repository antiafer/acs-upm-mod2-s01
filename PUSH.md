# Pushing this folder to GitHub

Four commands. Run them from this folder.

```bash
# 1. stamp your repository URL everywhere and rebuild the notebooks
python scripts/prepare_repo.py https://github.com/ORG/acs-upm-mod2-s01

# 2. create the repository on github.com, public, empty, no README

# 3. push
git init -b main
git add .
git commit -m "Session 1: slides, labs and data"
git remote add origin https://github.com/ORG/acs-upm-mod2-s01.git
git push -u origin main
```

`master/` and `solutions/` are in `.gitignore`, so neither the source notebooks nor the instructor
versions reach the public repository. Before every push, check that what you are about to publish
contains no answers: `git status --short` and, if in doubt, `git diff --cached`.

After the push, the links printed by `prepare_repo.py` are the ones to hand to students. Check one
of them in a private browser window, logged out, before class.

## If you prefer the GitHub web interface

Create the repository, then **Add file → Upload files**, and drag the whole folder in. Two caveats:
the browser uploader does not read `.gitignore`, so delete `master/` and `solutions/` from your
copy first, and
it will not upload empty folders.

## Size

4.8 MB in total, largest file 2.0 MB. Well inside GitHub's limits; no Git LFS needed.
