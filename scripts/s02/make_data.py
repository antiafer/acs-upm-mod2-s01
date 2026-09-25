"""
Genera el conjunto de datos docente de la Sesion 2 (Modulo 2, Diploma ACS-UPM).

Produce:
  anejo_geotecnico.pdf            anejo nativo con tabla de sondeos y SPT
  certificado_hormigon_escaneado.pdf  certificado de ensayo rasterizado, girado y con ruido
  piezometro_PZ07.csv             serie de un datalogger con centinelas, huecos y duplicado horario
  boletin_embalses.html           tabla web con cabecera de dos filas, notas y numeros espanoles
  s2_<fecha>_B0X.tif              bandas sinteticas tipo Sentinel-2 L2A (DN con desplazamiento)
  s2_<fecha>_SCL.tif              mapa de clasificacion de escena
  s2_<fecha>_MTD.json             metadatos con BOA_ADD_OFFSET y QUANTIFICATION_VALUE
  embalse.gpkg                    poligono de referencia del vaso

Los valores son sinteticos; la estructura y los defectos reproducen los originales.

Uso:
    python scripts/crear_datos_s2.py --comprobar
"""

import argparse
import json
import os
import subprocess

import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(BASE, "data")
SEMILLA = 20260925

# Area del embalse, ETRS89 / UTM 30N
EX0, EY1 = 420000.0, 4500000.0
RES = 20.0
NX = NY = 300

FECHAS = {"20230812": "sequia", "20250427": "lleno"}


# ---------------------------------------------------------------- anejo PDF
def tabla_sondeos(rng):
    """Tabla resumen de ensayos SPT: 6 sondeos, 63 ensayos."""
    filas = []
    litologias = ["Relleno antrópico", "Arcilla arenosa", "Arena tosquiza", "Tosco"]
    for s in range(1, 7):
        n_ens = [12, 11, 10, 11, 9, 10][s - 1]
        prof = 1.50
        for _ in range(n_ens):
            lit = litologias[min(3, int(prof // 4))]
            base = {"Relleno antrópico": 7, "Arcilla arenosa": 15,
                    "Arena tosquiza": 28, "Tosco": 44}[lit]
            n_spt = int(np.clip(rng.normal(base + 1.4 * prof, 4), 2, 90))
            filas.append({
                "sondeo": f"S-{s}",
                "profundidad_m": round(prof, 2),
                "litologia": lit,
                "n_spt": n_spt,
                "humedad_pct": round(float(np.clip(rng.normal(18 - 0.3 * prof, 3), 4, 40)), 1),
                "densidad_g_cm3": round(float(np.clip(rng.normal(1.92 + 0.012 * prof, 0.07), 1.4, 2.4)), 2),
            })
            prof += rng.choice([1.5, 1.5, 3.0])
    return pd.DataFrame(filas)


def crear_anejo(df, ruta):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle, PageBreak)

    est = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=est["Heading1"], fontSize=13, spaceAfter=8)
    h2 = ParagraphStyle("h2", parent=est["Heading2"], fontSize=11, spaceAfter=6)
    cuerpo = ParagraphStyle("cuerpo", parent=est["BodyText"], fontSize=9, leading=12)

    doc = SimpleDocTemplate(ruta, pagesize=A4,
                            leftMargin=20 * mm, rightMargin=20 * mm,
                            topMargin=18 * mm, bottomMargin=18 * mm,
                            title="Anejo 3. Geología y geotecnia")
    el = []
    el.append(Paragraph("PROYECTO DE CONSTRUCCIÓN. VARIANTE DE LA M-407", h1))
    el.append(Paragraph("ANEJO Nº 3. GEOLOGÍA Y GEOTECNIA", h1))
    el.append(Spacer(1, 8))
    el.append(Paragraph("1. Objeto y alcance", h2))
    el.append(Paragraph(
        "El presente anejo recoge los resultados de la campaña geotécnica realizada entre "
        "marzo y mayo de 2025 para la definición del trazado de la variante. La campaña ha "
        "consistido en la ejecución de <b>6 sondeos a rotación con recuperación continua de "
        "testigo</b> y la realización de <b>63 ensayos de penetración estándar (SPT)</b>, "
        "complementados con ensayos de identificación en laboratorio.", cuerpo))
    el.append(Spacer(1, 6))
    el.append(Paragraph("2. Marco geológico", h2))
    el.append(Paragraph(
        "El ámbito se sitúa sobre los materiales terciarios de la Cuenca de Madrid. Bajo un "
        "nivel superficial de relleno antrópico de espesor variable, se reconoce una unidad de "
        "arcillas arenosas de consistencia firme, que pasa en profundidad a arenas tosquizas y "
        "finalmente al sustrato de tosco. El nivel freático se ha detectado entre 8,40 y 11,20 m "
        "de profundidad según el sondeo.", cuerpo))
    el.append(Spacer(1, 6))
    el.append(Paragraph("3. Unidades geotécnicas", h2))
    el.append(Paragraph(
        "Se distinguen cuatro unidades geotécnicas, cuyos parámetros característicos se resumen "
        "en el apartado 5. Los valores de golpeo N del ensayo SPT se presentan sin corregir.", cuerpo))
    el.append(PageBreak())

    el.append(Paragraph("4. Resultados de la campaña", h2))
    el.append(Paragraph(
        "En la tabla siguiente se recogen los 63 ensayos SPT realizados, con indicación del "
        "sondeo, la profundidad de ensayo, la unidad geotécnica atravesada, el golpeo N y los "
        "resultados de humedad natural y densidad aparente determinados sobre la muestra "
        "recuperada. Los valores de humedad se expresan en tanto por ciento sobre peso seco.", cuerpo))
    el.append(Spacer(1, 8))

    cab = ["Sondeo", "Prof. (m)", "Unidad geotécnica", "N (SPT)", "w (%)", "d (g/cm3)"]
    datos = [cab] + [
        [r.sondeo, f"{r.profundidad_m:.2f}".replace(".", ","), r.litologia,
         str(r.n_spt), f"{r.humedad_pct:.1f}".replace(".", ","),
         f"{r.densidad_g_cm3:.2f}".replace(".", ",")]
        for r in df.itertuples()
    ]
    t = Table(datos, colWidths=[20 * mm, 20 * mm, 45 * mm, 18 * mm, 18 * mm, 25 * mm],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.black),
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(.85, .85, .85)),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
    ]))
    el.append(t)
    el.append(Spacer(1, 8))
    el.append(Paragraph(
        "<i>Nota: los ensayos con rechazo (R) no se han incluido en la tabla.</i>", cuerpo))
    el.append(PageBreak())
    el.append(Paragraph("5. Parámetros de cálculo adoptados", h2))
    el.append(Paragraph(
        "A partir de los resultados anteriores se adoptan los parámetros que se recogen a "
        "continuación para el cálculo de cimentaciones y taludes.", cuerpo))
    doc.build(el)


def tabla_probetas(rng):
    """Serie de 12 probetas de un mismo lote de hormigon HA-30."""
    filas = []
    for i in range(1, 13):
        edad = 7 if i <= 4 else 28
        base = 24.0 if edad == 7 else 34.5
        res = float(np.clip(rng.normal(base, 1.9), 15, 48))
        carga = res * 17671.5 / 1000.0          # probeta cilindrica de 150 mm
        filas.append({
            "probeta": f"P-{i:02d}",
            "fabricacion": "12/03/2025",
            "rotura": "19/03/2025" if edad == 7 else "09/04/2025",
            "edad_dias": edad,
            "carga_kn": round(carga, 1),
            "resistencia_mpa": round(res, 1),
        })
    return pd.DataFrame(filas)


def crear_certificado(df, ruta_pdf):
    """Certificado de ensayo a compresion, tipografia grande y reglado ligero."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                    Table, TableStyle)

    est = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=est["Heading1"], fontSize=14, spaceAfter=6)
    cuerpo = ParagraphStyle("c", parent=est["BodyText"], fontSize=10.5, leading=14)

    doc = SimpleDocTemplate(ruta_pdf, pagesize=A4, leftMargin=22 * mm,
                            rightMargin=22 * mm, topMargin=20 * mm, bottomMargin=20 * mm)
    el = [
        Paragraph("LABORATORIO DE ENSAYOS DE MATERIALES", h1),
        Paragraph("CERTIFICADO DE ENSAYO A COMPRESION SIMPLE", h1),
        Spacer(1, 6),
        Paragraph("Expediente: 2025/GE/0417 &nbsp;&nbsp; Obra: Variante de la M-407", cuerpo),
        Paragraph("Tipificacion del hormigon: HA-30/B/20/IIa &nbsp;&nbsp; Lote: L-12", cuerpo),
        Paragraph("Probetas cilindricas de 150 x 300 mm. Norma UNE-EN 12390-3.", cuerpo),
        Paragraph("Se ensayan <b>12 probetas</b> procedentes del mismo amasado.", cuerpo),
        Spacer(1, 10),
    ]
    cab = ["Probeta", "Fabricacion", "Rotura", "Edad (dias)", "Carga (kN)", "Resistencia (MPa)"]
    datos = [cab] + [
        [r.probeta, r.fabricacion, r.rotura, str(r.edad_dias),
         f"{r.carga_kn:.1f}".replace(".", ","),
         f"{r.resistencia_mpa:.1f}".replace(".", ",")]
        for r in df.itertuples()
    ]
    t = Table(datos, colWidths=[24 * mm, 27 * mm, 27 * mm, 24 * mm, 26 * mm, 32 * mm])
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.black),
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10.5),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    el.append(t)
    el.append(Spacer(1, 10))
    el.append(Paragraph(
        "Resistencia caracteristica estimada a 28 dias: 32,1 MPa. "
        "El lote CUMPLE las especificaciones del pliego.", cuerpo))
    doc.build(el)


def crear_escaneado(rng, ruta_pdf, ruta_salida):
    """Rasteriza, gira ligeramente, anade ruido y guarda como PDF de imagen."""
    from PIL import Image
    tmp = os.path.join(RUTA, "_tmp_cert")
    subprocess.run(["pdftoppm", "-r", "300", "-f", "1", "-l", "1", "-png", ruta_pdf, tmp],
                   check=True)
    img = Image.open(tmp + "-1.png").convert("L")
    img = img.rotate(-0.6, resample=Image.BICUBIC, fillcolor=255, expand=False)
    a = np.asarray(img).astype(np.int16)
    a = a + rng.normal(0, 6, a.shape).astype(np.int16)
    a[rng.random(a.shape) < 0.0004] = 70
    a = np.clip(a, 0, 255).astype(np.uint8)
    Image.fromarray(a).convert("RGB").save(ruta_salida, "PDF", resolution=300.0)
    os.remove(tmp + "-1.png")


# ---------------------------------------------------------------- piezometro
def crear_piezometro(rng, ruta):
    """Serie horaria de un datalogger: cabecera TOA5, centinelas, hueco y cambio de hora."""
    idx = pd.date_range("2025-09-15", "2025-11-15 23:00", freq="h")
    t = np.arange(len(idx))
    nivel = (12.80
             + 0.9 * np.sin(2 * np.pi * t / (24 * 30))
             - 0.0009 * t
             + rng.normal(0, 0.012, len(idx)).cumsum() * 0.25)
    temp = 14.5 + 1.2 * np.sin(2 * np.pi * (t - 200) / (24 * 30)) + rng.normal(0, 0.15, len(idx))
    bat = np.clip(12.9 - 0.0008 * t + rng.normal(0, 0.03, len(idx)), 11.4, 13.2)

    df = pd.DataFrame({"TIMESTAMP": idx, "RECORD": np.arange(4400, 4400 + len(idx)),
                       "Nivel_m": nivel.round(3), "Temp_C": temp.round(1),
                       "Batt_V": bat.round(2)})

    # 1. centinela -99.99 cuando la bateria baja de 11.9 V
    flojo = df["Batt_V"] < 11.9
    df.loc[flojo, "Nivel_m"] = -99.99
    # 2. hueco real: el equipo se desconecta cuatro dias
    hueco = (df["TIMESTAMP"] >= "2025-10-06") & (df["TIMESTAMP"] < "2025-10-10")
    df = df.loc[~hueco].copy()
    # 3. cambio de hora: la madrugada del 26 de octubre repite las 02:00 y 02:30
    repetida = df[(df["TIMESTAMP"] >= "2025-10-26 02:00") & (df["TIMESTAMP"] < "2025-10-26 03:00")]
    df = pd.concat([df, repetida], ignore_index=True).sort_values("TIMESTAMP", kind="stable")

    cabecera = (
        '"TOA5","CR1000_PZ07","CR1000","E4521","CR1000.Std.32.05","CPU:pz07.CR1","1842","Horario"\n'
        '"TIMESTAMP","RECORD","Nivel_m","Temp_C","Batt_V"\n'
        '"TS","RN","m","Deg C","Volts"\n'
        '"","","Smp","Smp","Min"\n'
    )
    cuerpo = df.copy()
    cuerpo["TIMESTAMP"] = cuerpo["TIMESTAMP"].dt.strftime("%Y-%m-%d %H:%M:%S")
    with open(ruta, "w", encoding="latin-1") as f:
        f.write(cabecera)
        cuerpo.to_csv(f, index=False, header=False, lineterminator="\n")
    return df


# ---------------------------------------------------------------- boletin HTML
def crear_boletin(rng, ruta, sup_sequia, sup_lleno):
    embalses = [
        ("El Atazar", 425.3, 68.2), ("Valmayor", 124.4, 71.0),
        ("Pinilla", 38.1, 54.6), ("Riosequillo", 50.0, 62.3),
        ("Navacerrada", 11.0, 77.4), ("Santillana", 91.2, 69.8),
        ("El Vellón", 41.0, 58.9), ("Puentes Viejas", 53.0, 61.2),
    ]
    # el embalse del ejercicio, con la superficie que se medira en la imagen
    embalses.insert(0, ("Presa de la Hoz", 96.4, 63.5))
    total_cap = sum(e[1] for e in embalses)

    def num(v, dec=1):
        s = f"{v:,.{dec}f}"
        return s.replace(",", "@").replace(".", ",").replace("@", ".")

    filas = ""
    for i, (n, cap, pct) in enumerate(embalses):
        nota = "<sup>[1]</sup>" if i == 0 else ""
        sup = f"{num(sup_lleno if i == 0 else rng.uniform(50, 900), 1)}"
        filas += (f'    <tr><td>{n}{nota}</td><td>{num(cap)}</td>'
                  f'<td>{num(pct)}</td><td>{sup}</td></tr>\n')
    filas += (f'    <tr class="total"><td>Total cuenca</td><td>{num(total_cap)}</td>'
              f'<td>&nbsp;</td><td>&nbsp;</td></tr>\n')

    html = f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Boletín hidrológico semanal. Cuenca del Tajo</title></head>
<body>
<h1>Boletín hidrológico semanal</h1>
<p>Datos correspondientes a la semana del 21 al 27 de abril de 2025.
Sistema de explotación: cuenca alta del Tajo.</p>

<table class="datos">
  <thead>
    <tr><th rowspan="2">Embalse</th><th colspan="2">Reserva</th>
        <th rowspan="2">Superficie de lámina (ha)</th></tr>
    <tr><th>Capacidad (hm3)</th><th>Llenado (%)</th></tr>
  </thead>
  <tbody>
{filas}  </tbody>
</table>

<p class="notas">[1] Superficie de lámina estimada por teledetección a partir de imagen
Sentinel-2 de 27 de abril de 2025.</p>

<h2>Precipitación acumulada</h2>
<table class="secundaria">
  <tr><th>Estación</th><th>mm</th></tr>
  <tr><td>Buitrago</td><td>12,4</td></tr>
  <tr><td>Rascafría</td><td>18,9</td></tr>
</table>
</body></html>
"""
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(html)
    return total_cap


# ---------------------------------------------------------------- Sentinel-2
def crear_escena(rng, fecha, estado):
    """Bandas sinteticas tipo L2A: DN enteros con desplazamiento de -1000."""
    import rasterio
    from rasterio.transform import from_origin

    yy, xx = np.mgrid[0:NY, 0:NX]
    cx, cy = NX * 0.45, NY * 0.5

    # vaso del embalse: cuerpo principal mas dos colas
    def elipse(x0, y0, a, b, ang=0.0):
        dx, dy = xx - x0, yy - y0
        u = dx * np.cos(ang) + dy * np.sin(ang)
        v = -dx * np.sin(ang) + dy * np.cos(ang)
        return (u / a) ** 2 + (v / b) ** 2
    vaso = np.minimum.reduce([
        elipse(cx, cy, 62, 28),
        elipse(cx + 55, cy - 32, 40, 12, 0.6),
        elipse(cx - 48, cy + 26, 34, 10, -0.5),
    ])
    umbral = 1.0 if estado == "lleno" else 0.42   # en sequia el agua se retira
    agua = vaso < umbral

    # reflectancias de superficie plausibles
    veg = np.clip(0.55 + 0.25 * np.sin(xx / 37.0) * np.cos(yy / 29.0), 0.15, 0.95)
    b02 = np.where(agua, 0.042, 0.055 + 0.015 * (1 - veg))
    b03 = np.where(agua, 0.055, 0.075 + 0.030 * (1 - veg))
    b04 = np.where(agua, 0.038, 0.095 + 0.090 * (1 - veg))
    b08 = np.where(agua, 0.018, 0.150 + 0.330 * veg)
    # orla de suelo desecado alrededor del agua en la fecha de sequia
    if estado == "sequia":
        orla = (vaso >= umbral) & (vaso < umbral + 0.55)
        b04 = np.where(orla, 0.185, b04)
        b08 = np.where(orla, 0.210, b08)

    bandas = {"B02": b02, "B03": b03, "B04": b04, "B08": b08}
    for k in bandas:
        bandas[k] = np.clip(bandas[k] + rng.normal(0, 0.004, (NY, NX)), 0.001, 1.2)

    # clasificacion de escena (SCL) y un banco de nubes en la fecha de lleno
    scl = np.where(agua, 6, 4).astype("uint8")
    if estado == "lleno":
        nube = elipse(NX * 0.83, NY * 0.18, 34, 26) < 1.0
        sombra = elipse(NX * 0.83 + 16, NY * 0.18 + 20, 30, 18) < 1.0
        scl = np.where(nube, 9, scl).astype("uint8")
        scl = np.where(sombra & ~nube, 3, scl).astype("uint8")
        for k in bandas:
            bandas[k] = np.where(nube, np.clip(bandas[k] + 0.55, 0, 1.4), bandas[k])

    perfil = {
        "driver": "GTiff", "height": NY, "width": NX, "count": 1, "dtype": "int16",
        "crs": "EPSG:25830", "transform": from_origin(EX0, EY1, RES, RES),
        "nodata": -32768, "compress": "deflate",
    }
    for k, v in bandas.items():
        # DN con la convencion de la linea base 04.00: DN = ref*10000 + 1000
        dn = np.round(v * 10000.0 + 1000.0).astype("int16")
        with rasterio.open(os.path.join(RUTA, f"s2_{fecha}_{k}.tif"), "w", **perfil) as dst:
            dst.write(dn, 1)

    p8 = dict(perfil, dtype="uint8", nodata=0)
    with rasterio.open(os.path.join(RUTA, f"s2_{fecha}_SCL.tif"), "w", **p8) as dst:
        dst.write(scl, 1)

    meta = {
        "PRODUCT_ID": f"S2B_MSIL2A_{fecha}T105619_N0511_R094_T30TVK",
        "PROCESSING_BASELINE": "05.11",
        "SENSING_DATE": f"{fecha[:4]}-{fecha[4:6]}-{fecha[6:]}",
        "QUANTIFICATION_VALUE": 10000,
        "BOA_ADD_OFFSET": {b: -1000 for b in ["B02", "B03", "B04", "B08"]},
        "SCL_CLASSES": {"3": "sombra de nube", "4": "vegetacion", "6": "agua",
                        "8": "nube probable", "9": "nube alta probabilidad"},
        "NOTA": "Producto sintetico con fines docentes. No corresponde a una adquisicion real.",
    }
    with open(os.path.join(RUTA, f"s2_{fecha}_MTD.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    return float(agua.sum() * RES * RES / 10000.0)   # superficie en hectareas


def crear_poligono_embalse():
    import geopandas as gpd
    from shapely.geometry import box
    g = gpd.GeoDataFrame(
        {"nombre": ["Presa de la Hoz"], "capacidad_hm3": [96.4]},
        geometry=[box(EX0 + 25 * RES, EY1 - 265 * RES, EX0 + 275 * RES, EY1 - 35 * RES)],
        crs="EPSG:25830",
    )
    g.to_file(os.path.join(RUTA, "embalse.gpkg"), layer="vaso", driver="GPKG")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--comprobar", action="store_true")
    args = ap.parse_args()

    os.makedirs(RUTA, exist_ok=True)
    rng = np.random.default_rng(SEMILLA)

    df = tabla_sondeos(rng)
    ruta_pdf = os.path.join(RUTA, "anejo_geotecnico.pdf")
    crear_anejo(df, ruta_pdf)

    probetas = tabla_probetas(rng)
    sol_dir = os.path.join(BASE, "solutions")
    os.makedirs(sol_dir, exist_ok=True)
    probetas.rename(columns={"probeta": "specimen", "fabricacion": "cast_date", "rotura": "test_date",
                             "edad_dias": "age_days", "carga_kn": "load_kN",
                             "resistencia_mpa": "strength_MPa"}).to_csv(
        os.path.join(sol_dir, "certificate_ground_truth.csv"), sep=";", index=False, decimal=",")
    ruta_cert = os.path.join(RUTA, "_certificado_nativo.pdf")
    crear_certificado(probetas, ruta_cert)
    crear_escaneado(rng, ruta_cert, os.path.join(RUTA, "certificado_hormigon_escaneado.pdf"))
    os.remove(ruta_cert)

    pz = crear_piezometro(rng, os.path.join(RUTA, "piezometro_PZ07.csv"))

    sup = {}
    for fecha, estado in FECHAS.items():
        sup[estado] = crear_escena(rng, fecha, estado)
    crear_poligono_embalse()
    total = crear_boletin(rng, os.path.join(RUTA, "boletin_embalses.html"),
                          sup["sequia"], sup["lleno"])

    print(f"Datos escritos en {RUTA}")
    if args.comprobar:
        print("\n--- valores para los assert ---")
        print("anejo: ensayos SPT      =", len(df))
        print("anejo: sondeos          =", df['sondeo'].nunique())
        print("anejo: N min / max      =", df['n_spt'].min(), "/", df['n_spt'].max())
        print("anejo: prof max         =", df['profundidad_m'].max())
        print("certificado: probetas   =", len(probetas))
        print("certificado: R min/max  =", probetas['resistencia_mpa'].min(), "/",
              probetas['resistencia_mpa'].max())
        print("piezometro: filas       =", len(pz))
        print("piezometro: centinelas  =", int((pz['Nivel_m'] == -99.99).sum()))
        print("piezometro: duplicados  =", int(pz['TIMESTAMP'].duplicated().sum()))
        print("boletin: total cuenca   =", round(total, 1), "hm3")
        print("boletin: embalses       = 9 (+1 fila de total)")
        print("imagen: sup sequia      =", round(sup['sequia'], 1), "ha")
        print("imagen: sup lleno       =", round(sup['lleno'], 1), "ha")
        print("imagen: razon           =", round(sup['lleno'] / sup['sequia'], 2))


if __name__ == "__main__":
    main()
