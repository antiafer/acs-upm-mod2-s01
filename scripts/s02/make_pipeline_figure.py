"""The chain from a satellite scene to a number of hectares, in four panels, on the Lab 2.2 data.

    python scripts/make_pipeline_figure.py
Writes figuras/pipeline_pixels_to_hectares.png
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from skimage.filters import threshold_otsu

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
FIG = os.path.join(BASE, "figuras")
DATE = "20250427"
PURPLE, NAVY, GREY = "#964BFF", "#23263B", "#6B7683"


def band(b):
    with open(os.path.join(DATA, f"s2_{DATE}_MTD.json"), encoding="utf-8") as f:
        m = json.load(f)
    with rasterio.open(os.path.join(DATA, f"s2_{DATE}_{b}.tif")) as src:
        dn = src.read(1).astype("float32")
    return (dn + m["BOA_ADD_OFFSET"][b]) / m["QUANTIFICATION_VALUE"]


def stretch(a):
    lo, hi = np.percentile(a, (2, 98))
    return np.clip((a - lo) / (hi - lo), 0, 1)


def main():
    r, g, b, n = band("B04"), band("B03"), band("B02"), band("B08")
    with rasterio.open(os.path.join(DATA, f"s2_{DATE}_SCL.tif")) as src:
        scl = src.read(1)
    ndwi = (g - n) / (g + n + 1e-9)
    thr = float(threshold_otsu(ndwi))
    mask = (ndwi > thr) & ~np.isin(scl, [3, 8, 9])
    ha = mask.sum() * 400 / 10000

    fig, axes = plt.subplots(1, 4, figsize=(15, 4.3))
    axes[0].imshow(np.dstack([stretch(r), stretch(g), stretch(b)]))
    axes[0].set_title("1. The scene\nfour bands, digital numbers", fontsize=11, color=NAVY, loc="left")
    im = axes[1].imshow(ndwi, cmap="BrBG", vmin=-1, vmax=1)
    axes[1].set_title("2. Reflectance, then NDWI\none value per pixel, -1 to 1", fontsize=11, color=NAVY, loc="left")
    axes[2].imshow(mask, cmap="Blues", interpolation="nearest")
    axes[2].set_title(f"3. Threshold and cloud mask\nwater where NDWI > {thr:.2f}", fontsize=11, color=NAVY, loc="left")
    for a in axes[:3]:
        a.set_axis_off()
    axes[3].set_axis_off()
    axes[3].set_title("4. Count and convert", fontsize=11, color=NAVY, loc="left")
    axes[3].text(0.08, 0.78, f"{int(mask.sum()):,} water pixels", fontsize=15, color=NAVY,
                 transform=axes[3].transAxes)
    axes[3].text(0.08, 0.62, "x 400 m2 per pixel (20 m by 20 m)", fontsize=12, color=GREY,
                 transform=axes[3].transAxes)
    axes[3].text(0.08, 0.46, "/ 10 000 m2 per hectare", fontsize=12, color=GREY,
                 transform=axes[3].transAxes)
    axes[3].plot([0.08, 0.98], [0.40, 0.40], color=GREY, lw=1, transform=axes[3].transAxes)
    axes[3].text(0.08, 0.17, f"{ha:.1f} ha", fontsize=34, color=PURPLE, fontweight="bold",
                 transform=axes[3].transAxes)
    plt.tight_layout(w_pad=4.0)
    from matplotlib.patches import FancyArrowPatch
    for i in range(3):
        a0 = axes[i].get_position()
        a1 = axes[i + 1].get_position()
        y = a0.y0 + a0.height / 2
        fig.patches.append(FancyArrowPatch((a0.x1 + 0.006, y), (a1.x0 - 0.006, y),
                                           transform=fig.transFigure, arrowstyle="-|>",
                                           mutation_scale=22, color=PURPLE, lw=2.2))
    fig.savefig(os.path.join(FIG, "pipeline_pixels_to_hectares.png"), dpi=165,
                facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"written; water pixels {int(mask.sum())}, threshold {thr:.3f}, {ha:.1f} ha")


if __name__ == "__main__":
    main()
