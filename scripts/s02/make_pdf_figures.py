"""Figures that make slides 9, 10 and 11 concrete, from the real annex PDF.

    python scripts/make_pdf_figures.py
Writes:
  figuras/pdf_what_you_see.png      the table as a reader sees it (page 2, first rows)
  figuras/pdf_what_file_stores.png  the same region with every word the file stores boxed
  figuras/pdf_split_table.png       end of page 2 and start of page 3, header repeated
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pdfplumber
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(BASE, "data", "anejo_geotecnico.pdf")
FIG = os.path.join(BASE, "figuras")
RES = 170
PURPLE = (150, 75, 255)
TEAL = (8, 163, 169)


def crop_box(page, top_pt, bottom_pt, left_pt=86, right_pt=510):
    return (left_pt, top_pt, right_pt, bottom_pt)


def to_px(v):
    return int(round(v * RES / 72.0))


def main():
    os.makedirs(FIG, exist_ok=True)
    with pdfplumber.open(PDF) as pdf:
        p2, p3 = pdf.pages[1], pdf.pages[2]
        tb = p2.find_tables()[0]
        top = tb.bbox[1] - 4
        box = crop_box(p2, top, top + 78)

        # 1. what a reader sees
        seen = p2.crop(box).to_image(resolution=RES).original.convert("RGB")
        seen.save(os.path.join(FIG, "pdf_what_you_see.png"))

        # 2. what the file stores: every word as a separate positioned string
        stored = p2.crop(box).to_image(resolution=RES)
        words = [w for w in p2.extract_words() if box[1] <= w["top"] <= box[3] - 6]
        stored.draw_rects([(w["x0"], w["top"], w["x1"], w["bottom"]) for w in words],
                          stroke=PURPLE, stroke_width=2, fill=(150, 75, 255, 40))
        img = stored.annotated.convert("RGB")
        img.save(os.path.join(FIG, "pdf_what_file_stores.png"))

        # 3. the split: last rows of page 2 and first rows of page 3
        tb3 = p3.find_tables()[0]
        end2 = p2.crop(crop_box(p2, tb.bbox[3] - 50, tb.bbox[3] + 4)).to_image(resolution=RES).original.convert("RGB")
        start3 = p3.crop(crop_box(p3, tb3.bbox[1] - 4, tb3.bbox[1] + 50)).to_image(resolution=RES).original.convert("RGB")

    fig, axes = plt.subplots(2, 1, figsize=(7.6, 3.7), gridspec_kw={"hspace": 0.38})
    for ax, im, title, col in [(axes[0], end2, "End of page 2: the table seems to finish here (42 rows)", "#6B7683"),
                               (axes[1], start3, "Top of page 3: it continues, and the header is printed again", "#964BFF")]:
        ax.imshow(im)
        ax.set_axis_off()
        ax.set_title(title, fontsize=10.5, color=col, loc="left", fontweight="bold")
    axes[1].add_patch(plt.Rectangle((2, 2), start3.width - 5, 18.5 * RES / 72.0, fill=False,
                                    edgecolor="#964BFF", linewidth=2.5))
    fig.savefig(os.path.join(FIG, "pdf_split_table.png"), dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    with pdfplumber.open(PDF) as pdf:
        pdf.pages[1].to_image(resolution=60).original.convert("RGB").save(os.path.join(FIG, "thumb_annex.png"))
    cert = os.path.join(BASE, "data", "certificado_hormigon_escaneado.pdf")
    with pdfplumber.open(cert) as pdf:
        pdf.pages[0].to_image(resolution=60).original.convert("RGB").save(os.path.join(FIG, "thumb_certificate.png"))
    print("written: pdf_what_you_see.png, pdf_what_file_stores.png, pdf_split_table.png, thumbnails")


if __name__ == "__main__":
    main()
