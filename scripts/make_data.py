"""
Genera el conjunto de datos docente de la Sesion 1 (Modulo 2, Diploma ACS-UPM).

Los ficheros reproducen la estructura, la codificacion y los defectos de los
datos publicos reales (datos.madrid.es, CNIG) pero los valores son sinteticos.
Antes de impartir la sesion, sustituir por descargas reales y volver a calcular
los valores de los assert de los notebooks con:

    python scripts/make_data.py --comprobar

Uso:
    python scripts/make_data.py
"""

import argparse
import os
import numpy as np
import pandas as pd

RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
SEMILLA = 20260918

# Area de trabajo: ETRS89 / UTM 30N (EPSG:25830), entorno de Madrid
X0, X1 = 432000.0, 452000.0
Y0, Y1 = 4468000.0, 4488000.0


def crear_ubicaciones(rng, n=30):
    """Puntos de medida: CSV español con ; coma decimal y latin-1."""
    tipos = rng.choice(["URB", "M30"], size=n, p=[0.7, 0.3])
    df = pd.DataFrame(
        {
            "id": np.arange(1001, 1001 + n),
            "nombre": [f"PM-{i:04d}" for i in range(1, n + 1)],
            "distrito": rng.choice(
                ["Centro", "Chamartín", "Tetuán", "Arganzuela", "Alcalá"], size=n
            ),
            "tipo_elem": tipos,
            "x_utm": np.round(rng.uniform(X0 + 2000, X1 - 2000, n), 2),
            "y_utm": np.round(rng.uniform(Y0 + 2000, Y1 - 2000, n), 2),
        }
    )
    return df


def crear_aforos(rng, ubic, dias=30):
    """Aforos horarios. Estructura de datos.madrid.es: ; , latin-1, dd/mm/yyyy."""
    horas = pd.date_range("2025-09-01", periods=dias * 24, freq="h")
    filas = []
    for _, pm in ubic.iterrows():
        base = 900 if pm["tipo_elem"] == "M30" else 320
        for t in horas:
            # perfil diario con doble punta y caida de fin de semana
            h = t.hour
            perfil = (
                0.35
                + 0.65 * np.exp(-((h - 8.5) ** 2) / 8)
                + 0.80 * np.exp(-((h - 19.0) ** 2) / 10)
            )
            finde = 0.62 if t.dayofweek >= 5 else 1.0
            inten = base * perfil * finde * rng.normal(1.0, 0.10)
            ocup = np.clip(inten / (base * 2.4) * 100 * rng.normal(1.0, 0.18), 0, 100)
            vmed = np.clip(95 - 0.55 * ocup + rng.normal(0, 4), 5, 120)
            filas.append(
                (pm["id"], t, pm["tipo_elem"], max(inten, 0), ocup, vmed)
            )

    df = pd.DataFrame(
        filas, columns=["id", "fecha", "tipo_elem", "intensidad", "ocupacion", "vmed"]
    )

    # --- defectos deliberados, todos presentes en los ficheros reales ---
    n = len(df)
    # 1. valor centinela -1 en vmed cuando el detector no mide velocidad
    sin_vmed = rng.random(n) < 0.11
    df.loc[sin_vmed, "vmed"] = -1.0
    # 2. huecos reales: el detector 1007 cae tres dias enteros
    caida = (df["id"] == 1007) & (df["fecha"] >= "2025-09-12") & (
        df["fecha"] < "2025-09-15"
    )
    df = df.loc[~caida].copy()
    # 3. registros duplicados por reenvio del datalogger
    dup = df.sample(40, random_state=7)
    df = pd.concat([df, dup], ignore_index=True)
    df = df.sort_values(["fecha", "id"], kind="stable").reset_index(drop=True)

    df["intensidad"] = df["intensidad"].round(0).astype(int)
    df["ocupacion"] = df["ocupacion"].round(2)
    df["vmed"] = df["vmed"].round(1)
    return df


def formato_es(df, col_fecha=None):
    """Convierte a las convenciones españolas: dd/mm/yyyy, coma decimal, punto de millar."""
    out = df.copy()
    if col_fecha is not None:
        out[col_fecha] = out[col_fecha].dt.strftime("%d/%m/%Y %H:%M:%S")
    for c in out.columns:
        if pd.api.types.is_float_dtype(out[c]):
            out[c] = out[c].map(lambda v: f"{v:,.2f}".replace(",", "@")
                                .replace(".", ",").replace("@", "."))
        elif pd.api.types.is_integer_dtype(out[c]) and c not in ("id",):
            out[c] = out[c].map(lambda v: f"{v:,d}".replace(",", "."))
    return out


def crear_excel(rng, ubic, ruta):
    """Excel tipico de organismo: 3 filas de cabecera, celdas combinadas, hoja de notas."""
    import openpyxl
    from openpyxl.styles import Font

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Datos"
    ws["A1"] = "AYUNTAMIENTO DE MADRID - Dirección General de Gestión del Tráfico"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Puntos de medida. Resumen mensual. Septiembre 2025"
    ws["A4"] = "Identificación"
    ws["C4"] = "Tráfico medio"
    ws.merge_cells("A4:B4")
    ws.merge_cells("C4:E4")
    for j, h in enumerate(
        ["id", "nombre", "IMD (veh/día)", "Ocupación (%)", "V media (km/h)"], start=1
    ):
        ws.cell(row=5, column=j, value=h).font = Font(bold=True)

    for i, (_, pm) in enumerate(ubic.iterrows(), start=6):
        imd = int(rng.normal(21000 if pm["tipo_elem"] == "M30" else 7600, 1800))
        ws.cell(row=i, column=1, value=int(pm["id"]))
        ws.cell(row=i, column=2, value=pm["nombre"])
        ws.cell(row=i, column=3, value=imd)
        ws.cell(row=i, column=4, value=round(float(rng.uniform(4, 32)), 2))
        ws.cell(row=i, column=5, value=round(float(rng.uniform(28, 88)), 1))

    ws2 = wb.create_sheet("Notas")
    ws2["A1"] = "Los valores -1 indican ausencia de medida."
    ws2["A2"] = "IMD calculada sobre días con cobertura superior al 75%."
    wb.save(ruta)


def crear_geometrias(rng, ubic):
    """Municipios sinteticos (poligonos) en 4326 y en 25830, y un MDT en GeoTIFF."""
    import geopandas as gpd
    import rasterio
    from rasterio.transform import from_origin
    from shapely.geometry import Polygon

    # malla 3x3 de municipios rectangulares con borde irregular
    nombres = [
        "Villanueva del Ejemplo", "San Martín de Prueba", "Los Sauces",
        "Alcalá del Test", "Valdemuestra", "Pozuelo Sintético",
        "Torrejón de Datos", "Rivas Ficticia", "Getafe Simulado",
    ]
    polis, filas = [], []
    nx, ny = 3, 3
    dx, dy = (X1 - X0) / nx, (Y1 - Y0) / ny
    k = 0
    for j in range(ny):
        for i in range(nx):
            x0, y0 = X0 + i * dx, Y0 + j * dy
            # borde con ruido para que no sea una cuadricula perfecta
            pts = []
            for t in np.linspace(0, 1, 12, endpoint=False):
                ang = 2 * np.pi * t
                r = 0.42 + 0.06 * rng.normal()
                pts.append(
                    (x0 + dx / 2 + r * dx * np.cos(ang), y0 + dy / 2 + r * dy * np.sin(ang))
                )
            polis.append(Polygon(pts))
            filas.append({"nombre": nombres[k], "codigo": f"280{k+10:02d}"})
            k += 1

    gdf = gpd.GeoDataFrame(filas, geometry=polis, crs="EPSG:25830")
    gdf["superficie_km2"] = (gdf.area / 1e6).round(3)

    os.makedirs(os.path.join(RUTA, "municipios_shp"), exist_ok=True)
    # Shapefile: nombres de campo se truncan a 10 caracteres
    gdf.rename(columns={"superficie_km2": "superficie_km2"}).to_file(
        os.path.join(RUTA, "municipios_shp", "municipios.shp")
    )
    # GeoJSON: la especificacion RFC 7946 exige WGS84
    gdf.to_crs(4326).to_file(os.path.join(RUTA, "municipios.geojson"), driver="GeoJSON")

    # --- MDT sintetico: meseta con un valle fluvial y una sierra al norte ---
    res = 25.0
    ancho = int((X1 - X0) / res)
    alto = int((Y1 - Y0) / res)
    xs = np.linspace(X0, X1, ancho)
    ys = np.linspace(Y1, Y0, alto)  # norte arriba
    XX, YY = np.meshgrid(xs, ys)

    cota = (
        600
        + 0.0085 * (YY - Y0)                                    # sube hacia el norte
        + 85 * np.exp(-(((XX - 447000) / 3000) ** 2))           # sierra
        - 70 * np.exp(-(((YY - 4476000 - 0.12 * (XX - X0)) / 900) ** 2))  # valle
    )
    suave = rng.normal(0, 1.0, cota.shape)
    ker = np.ones((5, 5)) / 25.0
    from scipy.signal import convolve2d  # noqa: E402
    cota = cota + convolve2d(suave, ker, mode="same") * 6.0

    cota = cota.astype("float32")
    # zona sin dato en una esquina (hueco de vuelo)
    cota[:40, :40] = -32768.0

    perfil = {
        "driver": "GTiff", "height": alto, "width": ancho, "count": 1,
        "dtype": "float32", "crs": "EPSG:25830",
        "transform": from_origin(X0, Y1, res, res),
        "nodata": -32768.0, "compress": "deflate",
    }
    with rasterio.open(os.path.join(RUTA, "mdt25_madrid.tif"), "w", **perfil) as dst:
        dst.write(cota, 1)

    return gdf


def crear_ficheros_de_proyecto(rng, ubic):
    """Ficheros adicionales de la carpeta de proyecto para el Ejercicio 0.

    Dos de ellos mienten en la extension, como ocurre en la practica:
      intensidades_2024.xls   -> es HTML (exportacion tipica de un portal web)
      PZ07_20250915.dat       -> es texto TOA5 de un datalogger
    Y dos son formatos de dominio que el alumno no conoce:
      estructura_rev07.ifc    -> texto STEP (ISO 10303-21), se identifica leyendo la cabecera
      PNOA_2020_0559.las      -> binario, cabecera 'LASF'
    """
    # 1. "Excel" que en realidad es HTML: muy frecuente en descargas de portales publicos
    filas = ""
    for _, pm in ubic.head(12).iterrows():
        imd = int(rng.normal(21000 if pm["tipo_elem"] == "M30" else 7600, 1800))
        filas += (f"<tr><td>{pm['id']}</td><td>{pm['nombre']}</td>"
                  f"<td>{imd:,}</td></tr>\n".replace(",", "."))
    html = ("<html><head><meta charset='utf-8'></head><body>\n"
            "<table border='1'>\n<tr><th>Id</th><th>Punto de medida</th>"
            "<th>IMD 2024 (veh/dia)</th></tr>\n" + filas + "</table></body></html>\n")
    with open(os.path.join(RUTA, "intensidades_2024.xls"), "w", encoding="utf-8") as f:
        f.write(html)

    # 2. Datalogger TOA5 con extension .dat (Campbell Scientific exporta asi)
    idx = pd.date_range("2025-09-15", periods=24 * 7, freq="h")
    t = np.arange(len(idx))
    nivel = 12.80 + 0.4 * np.sin(2 * np.pi * t / 96) + rng.normal(0, 0.01, len(idx))
    cab = ('"TOA5","CR1000_PZ07","CR1000","E4521","CR1000.Std.32.05","CPU:pz07.CR1","1842","Horario"\n'
           '"TIMESTAMP","RECORD","Nivel_m","Temp_C","Batt_V"\n"TS","RN","m","Deg C","Volts"\n'
           '"","","Smp","Smp","Min"\n')
    with open(os.path.join(RUTA, "PZ07_20250915.dat"), "w", encoding="latin-1") as f:
        f.write(cab)
        for i, (ts, n) in enumerate(zip(idx, nivel)):
            f.write(f'"{ts:%Y-%m-%d %H:%M:%S}",{4400 + i},{n:.3f},{14.5 + rng.normal(0, .2):.1f},12.7\n')

    # 3. IFC minimo valido: fichero STEP de texto
    ifc = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('estructura_rev07.ifc','2025-09-18T10:12:00',('Oficina tecnica'),('ACS-UPM'),'IfcOpenShell','Revit 2025','');
FILE_SCHEMA(('IFC4'));
ENDSEC;
DATA;
#1=IFCPROJECT('2O2Fr$t4X7Zf8NOew3FLKI',$,'Variante M-407. Paso superior PK 3+420',$,$,$,$,(#20),#7);
#7=IFCUNITASSIGNMENT((#8,#9));
#8=IFCSIUNIT(*,.LENGTHUNIT.,.MILLI.,.METRE.);
#9=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#20=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#21,$);
#21=IFCAXIS2PLACEMENT3D(#22,$,$);
#22=IFCCARTESIANPOINT((0.,0.,0.));
#30=IFCBEAM('1kTvXnbbzCWw8lcMdlWtcm',$,'Viga prefabricada V-01',$,'Viga artesa 1.40',$,$,$,.BEAM.);
#31=IFCBEAM('1kTvXnbbzCWw8lcMdlWtcn',$,'Viga prefabricada V-02',$,'Viga artesa 1.40',$,$,$,.BEAM.);
#40=IFCCOLUMN('3ZYW59sxj8lei475l7EhLU',$,'Pila P-1',$,'Pila circular D=1.20',$,$,$,.COLUMN.);
ENDSEC;
END-ISO-10303-21;
"""
    with open(os.path.join(RUTA, "estructura_rev07.ifc"), "w", encoding="utf-8") as f:
        f.write(ifc)

    # 4. Nube de puntos LAS pequena y valida
    import laspy
    n = 2000
    hdr = laspy.LasHeader(point_format=3, version="1.2")
    hdr.offsets = np.array([X0, Y0, 0.0])
    hdr.scales = np.array([0.01, 0.01, 0.01])
    las = laspy.LasData(hdr)
    las.x = rng.uniform(X0 + 5000, X0 + 5200, n)
    las.y = rng.uniform(Y0 + 5000, Y0 + 5200, n)
    las.z = 640 + rng.normal(0, 1.5, n)
    las.classification = rng.choice([2, 2, 2, 5, 6], n).astype(np.uint8)
    las.intensity = rng.integers(20, 200, n).astype(np.uint16)
    las.write(os.path.join(RUTA, "PNOA_2020_0559.las"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comprobar", action="store_true",
                    help="imprime los valores esperados de los assert")
    args = ap.parse_args()

    os.makedirs(RUTA, exist_ok=True)
    rng = np.random.default_rng(SEMILLA)

    ubic = crear_ubicaciones(rng)
    aforos = crear_aforos(rng, ubic)

    # CSV en formato español, codificado en latin-1
    formato_es(ubic).to_csv(
        os.path.join(RUTA, "pm_ubicaciones.csv"), sep=";", index=False,
        encoding="latin-1")
    formato_es(aforos, col_fecha="fecha").to_csv(
        os.path.join(RUTA, "aforos_202509.csv"), sep=";", index=False,
        encoding="latin-1")

    crear_excel(rng, ubic, os.path.join(RUTA, "imd_septiembre.xlsx"))
    crear_geometrias(rng, ubic)
    crear_ficheros_de_proyecto(rng, ubic)

    print(f"Datos escritos en {RUTA}")
    if args.comprobar:
        import geopandas as gpd
        import rasterio
        print("\n--- valores para los assert de los notebooks ---")
        print("aforos: filas =", len(aforos))
        print("aforos: puntos de medida =", aforos['id'].nunique())
        print("aforos: duplicados =", int(aforos.duplicated().sum()))
        print("aforos: vmed == -1 =", int((aforos['vmed'] == -1).sum()))
        print("aforos: intensidad max =", int(aforos['intensidad'].max()))
        g = gpd.read_file(os.path.join(RUTA, "municipios.geojson"))
        print("municipios:", len(g), "crs geojson =", g.crs)
        with rasterio.open(os.path.join(RUTA, "mdt25_madrid.tif")) as src:
            print("mdt: shape =", src.shape, "res =", src.res, "crs =", src.crs)
            print("mdt: nodata =", src.nodata)


if __name__ == "__main__":
    main()
