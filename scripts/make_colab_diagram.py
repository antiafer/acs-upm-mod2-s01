"""Draws the distribution diagram for the labs: repository or Drive, into Colab.

    python scripts/make_colab_diagram.py
Writes figuras/colab_setup.png and figuras/colab_setup.svg
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(BASE, "figuras")
os.makedirs(FIG, exist_ok=True)

PURPLE, TEAL, NAVY, GREY, LILAC, BG = "#964BFF", "#08A3A9", "#23263B", "#6B7683", "#EFE3FF", "#F4F4F6"
MONO = {"family": "DejaVu Sans Mono"}

fig, ax = plt.subplots(figsize=(15.5, 8.6))
ax.set_xlim(0, 155)
ax.set_ylim(0, 86)
ax.axis("off")


def box(x, y, w, h, fill=BG, edge=None, lw=1.2, r=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=fill, edgecolor=edge or fill, linewidth=lw, zorder=1))


def txt(x, y, s, size=10, color=NAVY, weight="normal", ha="left", va="top", font=None, style="normal"):
    kw = dict(fontsize=size, color=color, fontweight=weight, ha=ha, va=va, zorder=3, style=style)
    if font:
        kw.update(font)
    ax.text(x, y, s, **kw)


def arrow(x1, y1, x2, y2, color=PURPLE, lw=2.0, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16,
                                 color=color, linewidth=lw, zorder=2,
                                 shrinkA=0, shrinkB=0))


def chip(x, y, label, color=PURPLE, w=None, size=8.5):
    w = w or (len(label) * 1.05 + 3)
    box(x, y - 2.6, w, 3.6, fill=color, r=1.8)
    txt(x + w / 2, y - 0.8, label, size=size, color="white", weight="bold", ha="center", va="center")
    return w


txt(2, 84, "How the labs reach the students", size=19, weight="bold")
txt(2, 79.4, "One source folder, two delivery routes, the same notebook running unchanged in both",
    size=11.5, color=GREY)

# ---------------------------------------------------------------- source
box(2, 40, 34, 34.5, fill=BG)
txt(4.5, 71.5, "THE SOURCE FOLDER", size=10, color=TEAL, weight="bold")
txt(4.5, 67.8, "Keep this one folder. Everything else is a copy of it.", size=9, color=GREY)
tree = """acs-upm-mod2-s01/
├── notebooks/
│     ├── Lab_1_1_reading_files.ipynb
│     ├── Lab_1_2_object_and_field.ipynb
│     └── ..._SOLUTION.ipynb        ← do not share
├── data/                            ← 4.8 MB, 12 files
│     ├── aforos_202509.csv
│     ├── municipios_shp/
│     └── mdt25_madrid.tif
├── scripts/
└── README.md"""
txt(4.5, 64.0, tree, size=8.6, color=NAVY, font=MONO)

# ---------------------------------------------------------------- route A
box(42, 52.5, 111, 22, fill=LILAC)
chip(44.5, 73.2, "ROUTE A · RECOMMENDED", color=PURPLE, w=34)
txt(80, 71.5, "Public GitHub repository. One link, nothing to install, no permissions to manage.",
    size=9.5, color=NAVY, va="center")

steps_a = [
    ("1", "Push the folder\nto GitHub", "Public repo.\n4.8 MB of data fits\nwithout Git LFS."),
    ("2", "Build the link", "colab.research.google.com/\ngithub/ORG/REPO/blob/main/\nnotebooks/Lab_1_1....ipynb"),
    ("3", "Share the short link", "The cover slide already\nshows bit.ly/acs-mod2-s1.\nPoint it here."),
    ("4", "Student clicks it", "Colab opens the notebook\nstraight from GitHub.\nRead-only until they save."),
    ("5", "Cell 0 clones the data", "git clone into /content.\nDATA is found automatically.\nTakes about five seconds."),
]
for i, (n, title, body) in enumerate(steps_a):
    x = 44.5 + i * 21.6
    box(x, 53.5, 19.4, 15.5, fill="white")
    ax.add_patch(plt.Circle((x + 2.0, 66.6), 1.5, color=PURPLE, zorder=3))
    txt(x + 2.0, 66.6, n, size=9, color="white", weight="bold", ha="center", va="center")
    txt(x + 4.6, 68.0, title, size=9.5, weight="bold")
    txt(x + 1.2, 62.4, body, size=8.3, color=GREY)
    if i < 4:
        arrow(x + 19.8, 61.0, x + 21.3, 61.0, color=PURPLE, lw=1.6)

# ---------------------------------------------------------------- route B
box(42, 20.5, 111, 28, fill=BG)
chip(44.5, 47.2, "ROUTE B · GOOGLE DRIVE", color=TEAL, w=33)
txt(79, 45.5, "Use it if the repository cannot be public. Three extra steps, and two traps.",
    size=9.5, color=NAVY, va="center")

steps_b = [
    ("1", "Upload the whole\nfolder to Drive", "Drag acs-upm-mod2-s01/\ninto My Drive. Keep the\nsubfolders as they are."),
    ("2", "Share it", "Right click → Share →\nAnyone with the link →\nViewer. Copy the link."),
    ("3", "Student: add\nshortcut to Drive", "Open the link → folder\nname → Add shortcut to\nDrive → My Drive."),
    ("4", "Open the .ipynb", "Double click → Open with\n→ Google Colaboratory.\nThen: Save a copy in Drive."),
    ("5", "Cell 0 mounts Drive", "It asks for permission once,\nthen finds\nMyDrive/ACS-UPM/Mod2-S01."),
]
for i, (n, title, body) in enumerate(steps_b):
    x = 44.5 + i * 21.6
    box(x, 27.5, 19.4, 15.5, fill="white")
    ax.add_patch(plt.Circle((x + 2.0, 40.6), 1.5, color=TEAL, zorder=3))
    txt(x + 2.0, 40.6, n, size=9, color="white", weight="bold", ha="center", va="center")
    txt(x + 4.6, 42.0, title, size=9.5, weight="bold")
    txt(x + 1.2, 36.4, body, size=8.3, color=GREY)
    if i < 4:
        arrow(x + 19.8, 35.0, x + 21.3, 35.0, color=TEAL, lw=1.6)

txt(44.5, 25.5, "Trap 1: the shortcut is not optional. Without it the shared folder is not under "
                "MyDrive and no path reaches it.", size=8.6, color=NAVY)
txt(44.5, 23.2, "Trap 2: “Save a copy in Drive” moves the notebook to the student's own Drive, so "
                "relative paths break. Cell 0 is written to survive that.", size=8.6, color=NAVY)

# ---------------------------------------------------------------- arrows from source
arrow(36.5, 64.0, 42.0, 64.0, color=PURPLE, lw=2.2)
arrow(36.5, 52.0, 42.0, 36.0, color=TEAL, lw=2.2)

# ---------------------------------------------------------------- bottom band
box(2, 2.5, 151, 15, fill=NAVY)
txt(5, 15.2, "WHAT CELL 0 DOES, IN EITHER ROUTE", size=10, color="#42DEDC", weight="bold")
txt(5, 11.8, "It looks for a data/ folder next to the notebook or one level up (local clone). "
             "If it is not there and we are in Colab, it clones the repository into /content. "
             "If that fails too, it mounts Drive\nand looks under MyDrive/ACS-UPM/Mod2-S01. "
             "The two variables it sets are BASE and DATA, and everything else in the notebook "
             "uses them. Students change nothing.", size=9.2, color="#CFD8DC")
txt(5, 5.2, "Outputs go to WORK, which is /content in Colab. A session expires and /content is "
            "wiped: that is why Lab 1.2 rebuilds top10.parquet by itself instead of failing.",
    size=9.2, color="#CFD8DC")

plt.tight_layout()
for ext in ("png", "svg"):
    fig.savefig(os.path.join(FIG, f"colab_setup.{ext}"), dpi=170,
                facecolor="white", bbox_inches="tight")
plt.close(fig)
print("written:", os.path.join(FIG, "colab_setup.png"))
