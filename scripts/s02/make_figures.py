"""
Genera las figuras de la presentacion de la Sesion 2 a partir de los datos reales
del curso. Escribe PNG en figuras/.

    python scripts/figuras_s2.py
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from skimage.filters import threshold_otsu

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "data")
FIG = os.path.join(BASE, "figuras")
os.makedirs(FIG, exist_ok=True)

NARANJA = "#964BFF"
ACERO = "#6B7683"
OSCURO = "#23263B"
plt.rcParams.update({
    "font.size": 9, "axes.edgecolor": "#B0BEC5", "axes.labelcolor": OSCURO,
    "xtick.color": ACERO, "ytick.color": ACERO, "axes.titlesize": 10,
    "figure.facecolor": "white", "savefig.facecolor": "white",
})


def piezometro():
    """Tres tratamientos del hueco, sobre la serie real del datalogger."""
    pz = pd.read_csv(os.path.join(DATOS, "piezometro_PZ07.csv"), skiprows=4,
                     encoding="latin-1",
                     names=["TIMESTAMP", "RECORD", "Nivel_m", "Temp_C", "Batt_V"],
                     parse_dates=["TIMESTAMP"])
    pz = pz.drop_duplicates(subset="TIMESTAMP").set_index("TIMESTAMP").sort_index()
    completo = pz.reindex(pd.date_range(pz.index.min(), pz.index.max(), freq="h"))

    bruto = completo["Nivel_m"]
    borrado = bruto[bruto != -99.99]
    nan = bruto.replace(-99.99, np.nan)
    interp = nan.interpolate(limit_direction="both")

    fig, axes = plt.subplots(1, 4, figsize=(13.2, 2.9), sharey=False)
    paneles = [
        (bruto, "1. As it comes from the logger", ACERO),
        (borrado, "2. Records dropped", ACERO),
        (nan, "3. Sentinel to NaN", ACERO),
        (interp, "4. Gap interpolated", NARANJA),
    ]
    for ax, (serie, titulo, color) in zip(axes, paneles):
        ax.plot(serie.index, serie.values, lw=.8, color=color)
        ax.set_title(titulo, color=OSCURO)
        ax.grid(alpha=.25)
        ax.tick_params(axis="x", rotation=30, labelsize=7)
        if titulo.startswith("1"):
            ax.set_ylabel("level (m)")
        else:
            ax.set_ylim(11.6, 14.2)
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "piezometro_tratamientos.png"), dpi=185)
    plt.close(fig)

    # detalle del hueco
    fig, ax = plt.subplots(figsize=(6.4, 2.6))
    ven = slice("2025-10-03", "2025-10-13")
    ax.plot(nan[ven].index, nan[ven].values, "o-", ms=2.2, lw=.9, color=ACERO, label="data")
    ax.plot(interp[ven].index, interp[ven].values, lw=1.6, color=NARANJA, alpha=.75,
            label="interpolation")
    ax.set_ylabel("level (m)"); ax.grid(alpha=.25); ax.legend(fontsize=8)
    ax.tick_params(axis="x", rotation=30, labelsize=7)
    ax.set_title("Four days without records: the logger went offline", color=OSCURO)
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "piezometro_hueco.png"), dpi=185)
    plt.close(fig)
    return int((bruto == -99.99).sum()), int(bruto.isna().sum())


def _leer(fecha, banda):
    with open(os.path.join(DATOS, f"s2_{fecha}_MTD.json"), encoding="utf-8") as f:
        m = json.load(f)
    with rasterio.open(os.path.join(DATOS, f"s2_{fecha}_{banda}.tif")) as s:
        dn = s.read(1).astype("float32")
    return (dn + m["BOA_ADD_OFFSET"][banda]) / m["QUANTIFICATION_VALUE"]


def _estirar(a, p=(2, 98)):
    lo, hi = np.nanpercentile(a, p)
    return np.clip((a - lo) / (hi - lo), 0, 1)


def escena():
    f = "20250427"
    b = {k: _leer(f, k) for k in ["B02", "B03", "B04", "B08"]}
    rgb = np.dstack([_estirar(b["B04"]), _estirar(b["B03"]), _estirar(b["B02"])])
    fc = np.dstack([_estirar(b["B08"]), _estirar(b["B04"]), _estirar(b["B03"])])
    ndwi = (b["B03"] - b["B08"]) / (b["B03"] + b["B08"] + 1e-9)

    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.4))
    axes[0].imshow(rgb); axes[0].set_title("True colour  B04 B03 B02")
    axes[1].imshow(fc); axes[1].set_title("False-colour infrared  B08 B04 B03")
    im = axes[2].imshow(ndwi, cmap="BrBG", vmin=-1, vmax=1)
    axes[2].set_title("NDWI (McFeeters, 1996)")
    plt.colorbar(im, ax=axes[2], shrink=.72)
    for a in axes:
        a.set_axis_off()
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "escena_composiciones.png"), dpi=135)
    plt.close(fig)

    # histograma con los tres umbrales
    u = float(threshold_otsu(ndwi))
    fig, ax = plt.subplots(figsize=(6.6, 2.8))
    ax.hist(ndwi.ravel(), bins=130, color=ACERO)
    for v, c, et in [(0.0, "#90A4AE", "zero"), (0.3, "#B0BEC5", "literature: 0.30"),
                     (u, NARANJA, f"Otsu: {u:.3f}")]:
        ax.axvline(v, color=c, lw=2, label=et)
    ax.set_xlabel("NDWI"); ax.set_ylabel("pixels"); ax.legend(fontsize=8)
    ax.grid(alpha=.25)
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "ndwi_histograma.png"), dpi=185)
    plt.close(fig)
    return u


def mascaras():
    res = {}
    for etiqueta, f in [("August 2023 (drought)", "20230812"),
                        ("April 2025 (full)", "20250427")]:
        g, n = _leer(f, "B03"), _leer(f, "B08")
        ind = (g - n) / (g + n + 1e-9)
        with rasterio.open(os.path.join(DATOS, f"s2_{f}_SCL.tif")) as s:
            scl = s.read(1)
        m = (ind > threshold_otsu(ind)) & ~np.isin(scl, [3, 8, 9])
        res[etiqueta] = (m, m.sum() * 400 / 10000)

    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.6))
    for ax, (et, (m, ha)) in zip(axes, res.items()):
        ax.imshow(m, cmap="Blues", interpolation="nearest")
        ax.set_title(f"{et}\n{ha:.0f} ha of water surface", color=OSCURO)
        ax.set_axis_off()
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "mascaras_agua.png"), dpi=175)
    plt.close(fig)
    return {k: round(v[1], 1) for k, v in res.items()}


def desplazamiento():
    """Efecto de ignorar BOA_ADD_OFFSET sobre la reflectancia y sobre el area detectada."""
    f = "20250427"
    with open(os.path.join(DATOS, f"s2_{f}_MTD.json"), encoding="utf-8") as fh:
        m = json.load(fh)
    with rasterio.open(os.path.join(DATOS, f"s2_{f}_B08.tif")) as s:
        dn8 = s.read(1).astype("float32")
    with rasterio.open(os.path.join(DATOS, f"s2_{f}_B03.tif")) as s:
        dn3 = s.read(1).astype("float32")
    with rasterio.open(os.path.join(DATOS, f"s2_{f}_SCL.tif")) as s:
        scl = s.read(1)
    q = m["QUANTIFICATION_VALUE"]
    bien8, bien3 = (dn8 - 1000) / q, (dn3 - 1000) / q
    mal8, mal3 = dn8 / q, dn3 / q
    agua = scl == 6
    valido = ~np.isin(scl, [3, 8, 9])
    nd_b = (bien3 - bien8) / (bien3 + bien8 + 1e-9)
    nd_m = (mal3 - mal8) / (mal3 + mal8 + 1e-9)
    area_b = ((nd_b > 0.3) & valido).sum() * 400 / 10000
    area_m = ((nd_m > 0.3) & valido).sum() * 400 / 10000

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.0))
    axes[0].bar(["correct", "offset ignored"],
                [bien8[agua].mean(), mal8[agua].mean()], color=[NARANJA, ACERO], width=.55)
    axes[0].set_ylabel("NIR reflectance over water")
    axes[0].set_title("Water appears to shine in the infrared")
    for i, v in enumerate([bien8[agua].mean(), mal8[agua].mean()]):
        axes[0].text(i, v, f"{v:.3f}", ha="center", va="bottom", fontsize=9)
    axes[1].bar(["correct", "offset ignored"], [area_b, area_m],
                color=[NARANJA, ACERO], width=.55)
    axes[1].set_ylabel("detected surface (ha)")
    axes[1].set_title("Water detected with fixed threshold NDWI > 0.3")
    for i, v in enumerate([area_b, area_m]):
        axes[1].text(i, v, f"{v:.0f}", ha="center", va="bottom", fontsize=9)
    for a in axes:
        a.grid(alpha=.25, axis="y")
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "desplazamiento_radiometrico.png"), dpi=185)
    plt.close(fig)
    return round(float(bien8[agua].mean()), 4), round(float(mal8[agua].mean()), 4), area_b, area_m


def spt():
    """Golpeo frente a profundidad, salida real del Lab 2.1."""
    import pdfplumber
    with pdfplumber.open(os.path.join(DATOS, "anejo_geotecnico.pdf")) as pdf:
        t1 = pdf.pages[1].extract_tables()[0]
        t2 = pdf.pages[2].extract_tables()[0]
    df = pd.DataFrame(t1[1:] + t2[1:], columns=t1[0])
    df.columns = ["sondeo", "prof", "unidad", "n", "w", "d"]
    df["prof"] = df["prof"].str.replace(",", ".").astype(float)
    df["n"] = df["n"].astype(int)

    fig, ax = plt.subplots(figsize=(4.4, 5.0))
    for s_, g in df.groupby("sondeo"):
        ax.plot(g["n"], g["prof"], "o-", ms=3.2, lw=1, label=s_)
    ax.invert_yaxis()
    ax.set_xlabel("N (SPT), blows"); ax.set_ylabel("depth (m)")
    ax.grid(alpha=.25); ax.legend(fontsize=7, ncol=2)
    ax.set_title("63 tests extracted from two pages", color=OSCURO)
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "spt_perfil.png"), dpi=185)
    plt.close(fig)
    return len(df)


if __name__ == "__main__":
    c, h = piezometro()
    print("piezómetro: centinelas", c, "| horas ausentes", h)
    print("umbral de Otsu:", round(escena(), 3))
    print("superficies:", mascaras())
    print("desplazamiento (nir bien, nir mal, area bien, area mal):", desplazamiento())
    print("ensayos en la figura de SPT:", spt())
    print("figuras en", FIG)
