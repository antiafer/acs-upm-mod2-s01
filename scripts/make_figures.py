"""Figuras de la Sesion 1 generadas de los datos del curso. Escribe PNG en figuras/."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = os.path.join(BASE, "data")
FIG = os.path.join(BASE, "figuras")
os.makedirs(FIG, exist_ok=True)
NARANJA, ACERO, OSCURO = "#E8590C", "#546E7A", "#1F2A30"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": "#B0BEC5", "axes.titlesize": 10,
                     "xtick.color": ACERO, "ytick.color": ACERO})


def top10():
    kw = dict(sep=";", decimal=",", thousands=".", encoding="latin-1")
    af = pd.read_csv(os.path.join(DATOS, "aforos_202509.csv"), parse_dates=["fecha"],
                     dayfirst=True, **kw).drop_duplicates()
    ub = pd.read_csv(os.path.join(DATOS, "pm_ubicaciones.csv"), **kw)
    m = af.groupby("id", as_index=False)["intensidad"].mean()
    return m.sort_values("intensidad", ascending=False).head(10).merge(ub, on="id")


def desajuste_crs():
    geo = gpd.read_file(os.path.join(DATOS, "municipios.geojson"))
    t = top10()
    sin = gpd.GeoDataFrame(t, geometry=gpd.points_from_xy(t.x_utm, t.y_utm))
    bien = sin.set_crs("EPSG:25830").to_crs(geo.crs)

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    geo.plot(ax=axes[0], facecolor="#CFD8DC", edgecolor="white")
    sin.plot(ax=axes[0], color=NARANJA, markersize=22)
    axes[0].set_title("Antes: municipios en grados, puntos en metros", color=OSCURO)
    axes[0].annotate("municipios\n(lon −3,7, lat 40,4)", xy=(-3.7, 40.4), xytext=(90000, 1.1e6),
                     fontsize=8, color=ACERO, arrowprops=dict(arrowstyle="->", color=ACERO, lw=.8))
    axes[0].annotate("puntos de aforo\n(x 440 000, y 4 480 000)", xy=(441000, 4478000),
                     xytext=(150000, 3.4e6), fontsize=8, color=NARANJA,
                     arrowprops=dict(arrowstyle="->", color=NARANJA, lw=.8))
    axes[0].set_aspect("auto")
    axes[0].ticklabel_format(style="plain")
    axes[0].set_xlim(-60000, 520000); axes[0].set_ylim(-250000, 4.75e6)
    axes[0].tick_params(labelsize=7)

    geo.plot(ax=axes[1], facecolor="#CFD8DC", edgecolor="white")
    bien.plot(ax=axes[1], color=NARANJA, markersize=26, edgecolor="white", linewidth=.5)
    axes[1].set_title("Después: set_crs(25830) y luego to_crs(4326)", color=OSCURO)
    axes[1].tick_params(labelsize=7)
    for a in axes:
        a.grid(alpha=.25)
    plt.tight_layout()
    fig.savefig(os.path.join(FIG, "crs_antes_despues.png"), dpi=175)
    plt.close(fig)


if __name__ == "__main__":
    desajuste_crs()
    print("figuras en", FIG)
