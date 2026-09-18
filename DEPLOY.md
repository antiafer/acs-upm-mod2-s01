# Publishing the labs so students open them in Colab

![How the labs reach the students](figuras/colab_setup.png)

## Route A — GitHub (recommended)

The whole folder is 4.8 MB, so the data fit in an ordinary public repository with no Git LFS.

1. Create a public repository, for example `acs-upm-mod2-s01`, and push this folder to it.
   **Do not push the `_SOLUTION.ipynb` files**: either keep them in a private branch or add them to
   `.gitignore` and hand them out separately.
2. Build the Colab link by putting `colab.research.google.com/github/` in front of the repository
   path:

   ```
   https://colab.research.google.com/github/ORG/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_1_reading_files.ipynb
   ```
3. Shorten it and put it on the cover slide, which already shows `bit.ly/acs-mod2-s1`.
4. Run `python scripts/prepare_repo.py <your repository URL>`, which stamps `REPO` into the
   master notebooks and rebuilds both versions of each lab.

The student clicks the link, Colab opens the notebook read-only, and the first cell clones the data
into `/content`. When they edit anything Colab offers **Save a copy in Drive**, which puts their
copy in their own Drive. The notebook still works, because cell 0 does not rely on relative paths.

## Route B — Google Drive

Use it when the repository cannot be public.

1. Drag the whole folder into My Drive, keeping the subfolders. Suggested location:
   `My Drive / ACS-UPM / Mod2-S01`.
2. Right click the folder → **Share** → *Anyone with the link* → **Viewer**. Copy the link.
3. Tell students to open the link and then **Add shortcut to Drive → My Drive**. This step is not
   optional: without it the folder is not under `MyDrive` and no path reaches it.
4. They open the `.ipynb` → **Open with → Google Colaboratory** → **Save a copy in Drive**.
5. Cell 0 mounts Drive, asks for permission once, and finds `MyDrive/ACS-UPM/Mod2-S01`.

If you place the folder somewhere else in Drive, change `DRIVE` at the top of cell 0 (and in
the master notebooks in `master/`) to match.

## What cell 0 does

The same cell works in the three situations, so students never edit a path:

| Situation | What it finds |
|---|---|
| Local clone, Jupyter launched in `notebooks/` or in the repository root | `data/` next to the notebook or one level up |
| Colab, Route A | clones `REPO` into `/content/acs-mod2` and uses its `data/` |
| Colab, Route B | mounts Drive and uses `MyDrive/<DRIVE>/data` |

It sets two variables, `BASE` and `DATA`, plus `WORK` for outputs (`/content` in Colab).

## Two things that will otherwise bite

**A Colab session expires and `/content` is wiped.** Lab 1.2 needs `top10.parquet`, produced by
exercise 6 of Lab 1.1. If a student comes back the next day, or opens Lab 1.2 first, the file is
gone. Cell 0 of Lab 1.2 rebuilds it from the source CSVs instead of failing, so the lab always
starts.

**`geopandas` and `rasterio` are not preinstalled in Colab.** Lab 1.2 installs them in its first
cell; it takes about a minute. Tell students to run that cell at the start of the break, not when
the lab begins.

## Checklist for the Thursday before class

- [ ] Open the Colab link in a private browser window, logged out, and check it opens.
- [ ] Run both student notebooks from top to bottom in Colab, not just locally.
- [ ] Check the install cell of Lab 1.2 still succeeds; Colab images change.
- [ ] Confirm the short link on the cover slide resolves.
- [ ] Confirm the `_SOLUTION` notebooks are **not** reachable from the shared link.

<!-- COLAB -->
## Open the labs in Colab

- [Lab_1_1_reading_files.ipynb](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_1_reading_files.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_1_reading_files.ipynb)
- [Lab_1_2_object_and_field.ipynb](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_2_object_and_field.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_2_object_and_field.ipynb)
<!-- /COLAB -->
