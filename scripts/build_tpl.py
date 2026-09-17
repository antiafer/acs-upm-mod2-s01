"""Session 1 deck, built with the components of the ACS-UPM template."""
from tpl import *
from tpl import _round, _fill, _noline, _line, _run
from tpl import session_strip, timeline_sessions
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

d = Deck()

MAP = [
    ["Structured", "Tabular", "pandas.DataFrame", ".csv .xlsx .parquet SQL", "Traffic counts, test registers", "Today", True],
    ["Structured", "Spatial: object", "geopandas.GeoDataFrame", ".shp .gpkg .geojson", "Parcels, alignments, structures", "Today", True],
    ["Structured", "Spatial: field", "xarray.DataArray, numpy", ".tif .asc .nc", "DEM, orthophoto, rainfall", "Today", True],
    ["Structured", "Hierarchical", "nested dict and list", ".json .xml .ifc", "API responses, BIM models", "Session 3", False],
    ["Structured", "Network", "networkx.Graph", ".graphml .osm .pbf", "Road, drainage, supply networks", "Session 11", False],
    ["Unstructured", "Document", "text, to be extracted", ".pdf .docx .html", "Geotechnical annex, tender", "Session 2", False],
    ["Unstructured", "Image", "array, to be interpreted", ".jpg .tif .jp2", "Site photos, satellite scenes", "Session 2", False],
]


def map_table(s, y, last_header, last_value):
    rows = [["", "Data model", "Structure in Python", "File formats", "In civil engineering", last_header]]
    for r in MAP:
        rows.append([r[0], r[1], r[2], r[3], r[4], last_value(r)])
    fills = lambda i, j: (LILAC if MAP[i][6] else (GREY1 if i % 2 else WHITE))
    return table(s, rows, 0.41, y, 12.5, [1.20, 1.75, 2.35, 2.20, 3.00, 2.00],
                 rowh=0.44, size=10.5, mono_cols=(2, 3), mono_size=9,
                 bold_col=1, row_fills=fills, hot_col=5)


# ===================================================================== 1
d.cover("Session 1", "From file to structure:", "data models in civil engineering",
        "Module 2. Data Fusion, Preparation and Visualization applied to Civil Engineering",
        "ACS-UPM Diploma on Engineering, Data Science and AI",
        "Antía Fernández", "2026", "Notebook: bit.ly/acs-mod2-s1")
d.notes(d.prs.slides[-1],
        "First session of Module 2. Module 1 covered pandas, numpy and matplotlib; that is assumed. "
        "Today's conceptual content is three words: model, structure, format. Everything else applies them.")

# ===================================================================== 2
s = d.slide("Structure of the module")
txt(s, "Twenty-four sessions, forty-eight contact hours, six blocks",
    0.41, 1.02, 12.0, 0.30, HNL, 14.5, GREY_TXT)
session_strip(s, 24, highlight={1, 2, 3, 19, 20}, y=1.38, h=0.30)
txt(s, "In purple, the five sessions taught by Antía Fernández. Today is the first.",
    0.41, 1.73, 9.0, 0.22, HNL, 10.5, GREY_TXT, italic=True)
timeline_sessions(s, [
    {"kicker": "Block 1 · S1-S3", "title": "Structured and\nunstructured data",
     "date": "18 Sep – 2 Oct", "meta": "3 sessions · 6 h", "sessions": [
        (1, "Data formats and models", "18 Sep", True),
        (2, "Unstructured data: PDF, HTML", "25 Sep", True),
        (3, "APIs and web scraping", "2 Oct", True)]},
    {"kicker": "Block 2 · S4-S12", "title": "Data quality\nand wrangling",
     "date": "21 Sep – 6 Nov", "meta": "9 sessions · 18 h", "sessions": [
        (4, "Descriptive statistics, DQ report", "21 Sep", False),
        (5, "Application to dataset", "28 Sep", False),
        (6, "Missing values and outliers", "5 Oct", False),
        (7, "Application to dataset", "9 Oct", False),
        (8, "Survey data: Likert scales", "16 Oct", False),
        (9, "Advanced pandas: merge and join", "23 Oct", False),
        (10, "Application to dataset", "26 Oct", False),
        (11, "Geospatial wrangling, choropleths", "30 Oct", False),
        (12, "Application to dataset", "6 Nov", False)]},
    {"kicker": "Block 3 · S13-S14", "title": "Data integration",
     "date": "10 – 13 Nov", "meta": "2 sessions · 4 h", "sessions": [
        (13, "Structure, granularity, relations", "10 Nov", False),
        (14, "Referential integrity", "13 Nov", False)]},
    {"kicker": "Block 4 · S15-S18", "title": "Feature\npreparation",
     "date": "16 – 27 Nov", "meta": "4 sessions · 8 h", "sessions": [
        (15, "Normalisation, scaling, encoding", "16 Nov", False),
        (16, "Feature selection", "20 Nov", False),
        (17, "PCA: scree plot, loadings, biplot", "23 Nov", False),
        (18, "Clustering as exploratory analysis", "27 Nov", False)]},
    {"kicker": "Block 5 · S19-S20", "title": "Data\nvisualization",
     "date": "4 – 11 Dec", "meta": "2 sessions · 4 h", "sessions": [
        (19, "Visualization design principles", "4 Dec", True),
        (20, "Interactive visualization, Plotly", "11 Dec", True)]},
    {"kicker": "Capstone · S21-S24", "title": "Mini-projects",
     "date": "Dec 2026 – Jan 2027", "meta": "4 sessions · 8 h", "sessions": [
        (21, "Group supervision", "", False),
        (22, "Independent work", "", False),
        (23, "Independent work", "", False),
        (24, "Oral presentations", "", False)]},
], marker=0)
d.notes(s, "One minute, no more. Point at the strip: the five purple sessions are the ones I teach; "
           "today is the first. Then point at block 2, which is nine of the twenty-four: most of "
           "this module is data quality and wrangling, and that proportion is itself the message. "
           "Two caveats from the spreadsheet: blocks 1 and 2 overlap, because block 1 runs on "
           "Fridays from 18 September while block 2 starts on 21 September, so the first fortnight "
           "has two sessions a week; and sessions 21 to 24 carry no date, so the December-January "
           "range is an assumption to be confirmed.")

# ===================================================================== 3
s = d.slide("Learning objectives")
card(s, 0.41, 1.45, 12.5, 4.95, LILAC)
txt(s, "By the end of the session, you will be able to:", 0.80, 1.68, 11.0, 0.32, HNL, 14.5, NAVY)
obj = ["distinguish between data model, data structure and file format, and place any dataset of a civil-engineering project at those three levels;",
       "determine the granularity of a table and verify it with a programmatic check, instead of assuming it;",
       "read a delimited file with Spanish conventions into Python with correct types, justifying each reading argument from prior inspection of the file;",
       "identify sentinel values and quantify the bias they introduce when they are not turned into explicit missing values;",
       "apply the distinction between object and field models to answer a query that combines a vector layer and a raster surface."]
for i, t in enumerate(obj):
    y = 2.18 + i * 0.83
    badge(s, i + 1, 0.80, y, PURPLE if i < 3 else TEAL)
    rich(s, [t], 1.42, y + 0.02, 11.2, 0.70, size=14.5)
txt(s, "Objective 1 is assessed in Exercise 0 and the exit ticket; 2 and 4 in Lab 1.1; 3 and 5 in Lab 1.2.",
    0.41, 6.55, 12.5, 0.28, HNL, 11, GREY_TXT, italic=True)
d.notes(s, "Read them out. Observable verbs only: distinguish, determine, read, identify, apply. "
           "Nothing that cannot be assessed.")

# ===================================================================== 4
s = d.slide("Session structure")
txt(s, "One hundred and ten minutes including the break, ten minutes of slack. Laptops open at minute seven.",
    0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
rowsx = [["0", "Opening and Exercise 0", "17", True, "How we work; the project folder, file by file"],
         ["1", "The map", "8", False, "Three levels, seven data models, and when each one is covered"],
         ["2", "Tabular data", "12", False, "From file to DataFrame: reading, storage, verification"],
         ["", "Lab 1.1", "26", True, "Reading files and columnar storage"],
         ["3", "Spatial data", "12", False, "Object and field: shapefile, raster, CRS, zonal statistics"],
         ["", "Lab 1.2", "22", True, "Object and field: answering the question"],
         ["4", "Close and exit ticket", "8", False, "Back to the map; three minutes of feedback"]]
for i, b in enumerate(rowsx):
    y = 1.55 + i * 0.70
    card(s, 0.41, y, 12.5, 0.62, LILAC if b[3] else GREY1, alpha=40 if b[3] else 100)
    if b[0]:
        txt(s, b[0], 0.62, y, 0.45, 0.62, NOHEMI, 22, PURPLE if b[3] else GREY_TXT,
            bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, b[1], 1.20, y + 0.04, 4.0, 0.30, HN, 15, NAVY, bold=True)
    txt(s, b[4], 1.20, y + 0.33, 8.6, 0.26, HNL, 11.5, GREY_TXT)
    txt(s, b[2] + " min", 10.3, y + 0.16, 1.0, 0.30, HN, 13, NAVY, align=PP_ALIGN.RIGHT)
    pill(s, "laptops" if b[3] else "notebook", 11.55, y + 0.16, w=1.05,
         color=PURPLE if b[3] else "9AA3B2", size=9)
banner(s, "Five-minute break after Lab 1.1.",
       "The handout also contains fourteen appendix slides that are not projected.",
       x=0.41, y=6.50, w=12.5, h=0.50, fill=NAVY2, size=12)
d.notes(s, "The schedule counts the opening and the close. Each theory block precedes the lab that "
           "practises it. If Lab 1.1 overruns, the slack is taken from there, never from Lab 1.2, "
           "which answers the question.")

# ===================================================================== 5
s = d.slide("How we work in the labs")
txt(s, "Four rules for all twenty-four sessions of the module", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
rules = [["Predict before you run", "Before running a prepared cell, tell your partner what you expect to see. Failed predictions are where learning happens; correct ones only confirm.", PURPLE],
         ["Pairs with roles", "Two people, one laptop. The driver does not decide alone; the navigator reads every line before it runs. Roles swap at the break.", TEAL_D],
         ["Errors stay on screen", "When a demonstration fails on the projector, we debug it there, in front of everyone. Reading an error message calmly is part of what this module teaches.", PURPLE],
         ["AI assistants: allowed, on one condition", "You must be able to explain every line you hand in. From time to time you will be asked to do so, out loud, without the laptop.", TEAL_D]]
for i, r in enumerate(rules):
    x = 0.41 + (i % 2) * 6.42
    y = 1.55 + (i // 2) * 2.45
    card(s, x, y, 6.08, 2.25, LILAC if i == 0 else GREY1, alpha=40 if i == 0 else 100)
    badge(s, i + 1, x + 0.28, y + 0.26, r[2])
    txt(s, r[0], x + 0.92, y + 0.30, 5.0, 0.40, HN, 16, NAVY, bold=True)
    rich(s, [r[1]], x + 0.28, y + 1.00, 5.55, 1.10, size=13.5)
txt(s, "Rule 1 is the hardest to keep and the one that pays most. Every lab has cells marked “predict before you run”.",
    0.41, 6.55, 12.5, 0.30, HNL, 12, GREY_TXT, italic=True)
d.notes(s, "Rule 1 is the predict-observe-explain cycle; well supported in programming education "
           "research and free. Rule 4 is the only AI policy enforceable in a classroom: say it on "
           "day one and apply it the first time someone hands in code they cannot explain.")

# ===================================================================== 6
s = d.section("Block 0", "At what elevation are the ten\nbusiest traffic counters in Madrid?",
              "Trivial to state; impossible to answer without solving three different problems.\nEach one is a block of this session.")
req = [["30 measurement points", "hourly counts, one month", "CSV", "tabular"],
       ["Their coordinates", "in ETRS89 / UTM 30N", "CSV", "object"],
       ["The terrain", "digital elevation model, 25 m", "GeoTIFF", "field"]]
for i, r in enumerate(req):
    x = 0.90 + i * 4.05
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(5.45), Inches(3.75), Inches(1.15))
    _round(sh, 8000); _fill(sh, "31344B"); _noline(sh)
    txt(s, r[0], x + 0.25, 5.57, 3.3, 0.28, HN, 14, WHITE, bold=True)
    txt(s, r[1], x + 0.25, 5.88, 3.3, 0.26, HNL, 12, "C9CEDA")
    pillrow(s, [r[2], r[3]], x + 0.25, 6.18, gap=0.08, color="4A5070", size=9, h=0.28)
d.notes(s, "Do not give the answer. It is answered at the end of Lab 1.2. The point of the question "
           "is not geographic: it forces a table, a vector layer and a surface to talk to each other, "
           "one from each of the three data models we cover today.")

# ===================================================================== 7
s = d.slide("Exercise 0: the project folder")
txt(s, "10 minutes · laptops open · this is how project information arrives", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
code(s, """proyecto_variante_M-407/
|-- aforos_202509.csv                 947 kB
|-- pm_ubicaciones.csv                1.5 kB
|-- imd_septiembre.xlsx               6.7 kB
|-- intensidades_2024.xls             0.8 kB
|-- municipios.geojson                6.8 kB
|-- municipios_shp/
|     '-- municipios.shp .shx .dbf .prj .cpg
|-- mdt25_madrid.tif                  2.0 MB
|-- PNOA_2020_0559.las               68 kB
|-- estructura_rev07.ifc              0.9 kB
'-- PZ07_20250915.dat                 7.6 kB""", 0.41, 1.50, 6.05, 3.35, 11.5)
steps = [["Run the peek() helper", "It shows the first bytes of every file, and a provisional text or binary verdict."],
         ["Classify all twelve", "Text or binary? Fill in the dictionary with your partner."],
         ["Predict, then check", "How many extensions lie? Identify them and say what they really are."],
         ["If you do not know, describe", "Write down what you can observe. That is also a professional answer."]]
for i, st in enumerate(steps):
    y = 1.55 + i * 0.95
    point(s, i + 1, st[0], st[1], 6.85, y, w=5.90, color=PURPLE if i % 2 == 0 else TEAL_D, size=13.5)
banner(s, "Done when", "the check prints “12 files classified” and you can explain why trying to decode as UTF-8 is not enough.",
       x=0.41, y=5.10, w=12.5, h=0.52, fill=NAVY2, size=12.5)
txt(s, "Debrief at minute ten. We come back to this folder at the close: by then you will know how to open seven of the twelve.",
    0.41, 5.80, 12.5, 0.30, HNL, 12, GREY_TXT, italic=True)
d.notes(s, "Debrief in this order. First, how many extensions lie: two, the .xls that is HTML (a typical "
           "public-portal export) and the .dat that is TOA5 logger text. Second, the IFC: nobody knows it, "
           "and that is where you model the professional answer out loud: I do not know it, but it is text, "
           "it says ISO-10303-21, and that string identifies the standard in thirty seconds. Third, the "
           "shapefile: the .prj is text and can be read. Verbal close: the extension is a label; the content "
           "identifies the format. Technical detail on peek: decoding as UTF-8 is not enough because null "
           "bytes are valid UTF-8, so it counts nulls and printable characters.")

# ===================================================================== 8
s = d.section("Block 1", "The map",
              "Three levels of abstraction, seven data models,\nand when each one is covered in this module.",
              ["model", "structure", "format"])
d.notes(s, "Eight minutes, three slides. This is the top of the pyramid: everything after it is a "
           "descent into two of the seven branches.")

# ===================================================================== 9
s = d.slide("Three levels: model, structure, format")
txt(s, "Three different questions about the same data", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
lv = [["Data model", "How do I conceive the phenomenon?", "Conceptual. Independent of software.",
       "A municipality has a boundary and attributes: it is an object. Elevation has a value at every point: it is a field.", PURPLE, LILAC],
      ["Data structure", "How does Python hold it in memory?", "Determines which operations are possible.",
       "DataFrame, GeoDataFrame, DataArray, Graph. A dozen libraries, a handful of structures.", TEAL_D, GREY1],
      ["File format", "How are the bytes written to disk?", "Exchange and storage. The most superficial level.",
       ".csv, .parquet, .shp, .gpkg, .tif, .json. The reading library absorbs it.", NAVY, GREY1]]
for i, n in enumerate(lv):
    y = 1.50 + i * 1.50
    card(s, 0.41, y, 12.5, 1.36, n[5], alpha=40 if i == 0 else 100)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.41), Inches(y), Inches(0.13), Inches(1.36))
    _fill(bar, n[4]); _noline(bar)
    txt(s, n[0], 0.78, y + 0.14, 3.2, 0.36, NOHEMI, 19, n[4], bold=True)
    txt(s, n[1], 0.78, y + 0.58, 3.4, 0.30, HNL, 13, GREY_TXT, italic=True)
    txt(s, n[2], 0.78, y + 0.92, 3.6, 0.30, HNL, 11.5, GREY_TXT)
    rich(s, [n[3]], 4.75, y + 0.30, 7.9, 0.90, size=14.5)
banner(s, "Formats change every few years; the models underneath almost never do.",
       "Learning a new format takes minutes once the structure is familiar; learning a new structure takes weeks.",
       x=0.41, y=6.10, w=12.5, h=0.56, fill=NAVY2, size=12.5)
txt(s, "Rey, Arribas-Bel and Wolf (2023), ch. 5. Lau, Gonzalez and Nolan (2023), note in ch. 8.2.",
    0.41, 6.78, 8.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "Three questions for any file, which summarise the three levels: which data model, which "
           "reader, and what is lost in conversion. The third is the one nobody asks. Rey and colleagues "
           "say explicitly that they discuss how Python represents data once read rather than file "
           "formats, because libraries reduce every format to a few canonical structures.")

# ===================================================================== 10
s = d.slide("The map: seven data models")
txt(s, "Everything you will meet in a project fits in one of these rows, and the session in which each is covered", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
map_table(s, 1.50, "Covered in", lambda r: r[5])
card(s, 0.41, 5.30, 6.08, 1.20, LILAC)
txt(s, "Today: three rows", 0.70, 5.42, 5.5, 0.28, HN, 13, PURPLE, bold=True)
rich(s, ["Tabular, spatial object and spatial field. Exactly the three that the question of the session needs, and the three that appear in every civil-engineering project."],
     0.70, 5.72, 5.5, 0.72, size=12)
card(s, 6.83, 5.30, 6.08, 1.20, GREY1, alpha=100)
txt(s, "Named today, developed later", 7.12, 5.42, 5.5, 0.28, HN, 13, TEAL_D, bold=True)
rich(s, ["Documents and images on Friday, with extraction and quality. Hierarchical data and JSON in session 3, with live APIs. Networks in session 11. BIM and point clouds in appendix A.1."],
     7.12, 5.72, 5.5, 0.72, size=12)
txt(s, "Object, field and network models after Rey, Arribas-Bel and Wolf (2023), ch. 3. Structured and unstructured split after Lau, Gonzalez and Nolan (2023), ch. 8.",
    0.41, 6.66, 11.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "This is the pyramid's second level and the slide to come back to. Walk the rows once, one "
           "example each. Then point at the three highlighted rows: that is today. Point at the last "
           "column for the rest: nobody should leave thinking JSON or PDFs were skipped; they are "
           "scheduled. We return to this table at the close with the three rows ticked.")

# ===================================================================== 11
s = d.slide("And one more axis: what the data means")
txt(s, "Five questions to ask any dataset before analysing it. Three are used today; the rest are scheduled",
    0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
q = [["Structure", "Is it rectangular? What shape is the file?", "Exercise 0", True],
     ["Granularity", "What does one row represent?", "Lab 1.1", True],
     ["Faithfulness", "Does the data resemble reality? Sentinels, duplicates, impossible values.", "Lab 1.1", True],
     ["Scope", "What population does it represent? What is left out?", "Session 4", False],
     ["Temporality", "Which moment does each date refer to: event, record, or storage?", "Session 6", False]]
for i, r in enumerate(q):
    y = 1.52 + i * 0.94
    card(s, 0.41, y, 12.5, 0.84, LILAC if r[3] else GREY1, alpha=40 if r[3] else 100)
    badge(s, i + 1, 0.70, y + 0.19, PURPLE if r[3] else "9AA3B2")
    txt(s, r[0], 1.32, y + 0.12, 2.4, 0.32, HN, 16, NAVY, bold=True)
    rich(s, [r[1]], 3.85, y + 0.16, 6.6, 0.55, size=12.5)
    pill(s, r[2], 10.85, y + 0.25, w=1.70, color=PURPLE if r[3] else "9AA3B2", size=10)
    if r[3]:
        txt(s, "today", 10.85, y + 0.02, 1.70, 0.22, HN, 9, PURPLE, bold=True, align=PP_ALIGN.CENTER)
txt(s, "Here “structure” means the shape of the dataset, not the in-memory structure of the previous slide. The framework keeps the term of its source.  ·  Data scope framework after Lau, Gonzalez and Nolan (2023), ch. 2, following Hellerstein.",
    0.41, 6.42, 12.5, 0.30, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "Orthogonal to the map: the map says what a dataset is; these five say what it means. Only "
           "three are exercised today, because they are the three the traffic file needs. Scope is "
           "session 4, temporality session 6. Say the schedule out loud: it is the same message as the map.")

# ===================================================================== 12
s = d.section("Block 2", "Tabular data: from file to DataFrame",
              "The first of today's three rows. Model, format, reading, storage, verification.\nThen Lab 1.1.",
              ["tidy", ".csv", ".parquet", "granularity", "sentinels"])
d.notes(s, "Twelve minutes, six slides. Same internal order as the spatial block later: model, then "
           "format, then the pitfalls the lab practises.")

# ===================================================================== 13
s = d.slide("The tabular model: tidy data")
banner(s, "A dataset is tidy when",
       "each variable forms a column, each observation forms a row, and each type of observational unit forms a table.",
       x=0.41, y=1.15, w=12.5, h=0.62, fill=NAVY2, size=14)
txt(s, "Messy (wide)", 0.41, 2.00, 5.5, 0.30, HN, 14, GREY_TXT, bold=True)
t1 = [["borehole", "1.50 m", "3.00 m", "4.50 m"], ["S-1", "12", "23", "31"], ["S-2", "8", "15", "22"]]
table(s, t1, 0.41, 2.38, 4.6, [1.3, 1.1, 1.1, 1.1], rowh=0.30, size=10.5,
      mono_cols=(0, 1, 2, 3), mono_size=10, head_fill="9AA3B2")
rich(s, ["Depth is a variable, but it lives in the headers. Blow count is a variable, but it occupies three columns."],
     0.41, 3.50, 4.8, 0.70, size=12, color=GREY_TXT)
ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(5.45), Inches(2.75), Inches(0.75), Inches(0.30))
_fill(ar, PURPLE); _noline(ar)
txt(s, "Tidy (long)", 6.55, 2.00, 5.5, 0.30, HN, 14, PURPLE, bold=True)
t2 = [["borehole", "depth_m", "n_spt"], ["S-1", "1.50", "12"], ["S-1", "3.00", "23"],
      ["S-1", "4.50", "31"], ["S-2", "1.50", "8"], ["...", "...", "..."]]
table(s, t2, 6.55, 2.38, 4.3, [1.4, 1.5, 1.4], rowh=0.30, size=10.5,
      mono_cols=(0, 1, 2), mono_size=10, head_fill=PURPLE)
rich(s, ["One row per test. Filtering, grouping and plotting all use the same three functions."],
     6.55, 4.35, 5.0, 0.70, size=12, color=GREY_TXT)
card(s, 0.41, 5.35, 12.5, 1.00, GREY1, alpha=100)
rich(s, [[("Wickham presents it as closely related to Codd's third normal form", True),
          (", with the constraints restated in statistical language. The five common ways a table is messy are in appendix A.2 and developed in session 4.", False)]],
     0.70, 5.55, 11.9, 0.65, size=13)
txt(s, "Wickham, H. (2014). Tidy Data. Journal of Statistical Software, 59(10).",
    0.41, 6.55, 8.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "One slide on the model before any format. The kinship with third normal form is what gives "
           "an obvious-looking idea academic standing; many students come from databases. Wickham says "
           "closely related, not equivalent: do not claim more than the source.")

# ===================================================================== 14
s = d.slide("Where does the schema live?")
txt(s, "Tabular formats: two independent axes that decide most of your reading errors", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
card(s, 0.41, 1.50, 5.95, 4.30, GREY1, alpha=100)
txt(s, "Text", 0.70, 1.65, 2.6, 0.38, HN, 17, GREY_TXT, bold=True)
txt(s, "Binary", 3.60, 1.65, 2.6, 0.38, HN, 17, PURPLE, bold=True)
pillrow(s, [".csv", ".json", ".geojson"], 0.70, 2.10, gap=0.08, color="9AA3B2", size=9, h=0.28)
pillrow(s, [".parquet", ".gpkg", ".tif"], 3.60, 2.10, gap=0.08, color=PURPLE, size=9, h=0.28)
rich(s, ["Opens in any editor", "Easy to version with git", "Encoding is the reader's problem",
         "Types are the reader's problem", "Large and slow past ~1 GB"],
     0.70, 2.60, 2.75, 3.0, size=12.5, space_after=8)
rich(s, ["Needs a library", "Types travel with the data", "Compressed; column access",
         "Usually 5-10x smaller", "Internal layout depends on the format"],
     3.60, 2.60, 2.60, 3.0, size=12.5, space_after=8)
sch = [["Implicit", "in your head or in a README", [".csv", ".txt"],
        "The read_csv arguments are the schema, written by hand every time.", "9AA3B2", GREY1],
       ["Embedded", "inside the file itself", [".parquet", ".gpkg", ".xlsx"],
        "Types and reference system survive the round trip.", PURPLE, LILAC],
       ["External", "in a published standard", [".ifc", ".gml"],
        "Software from different vendors agrees on the meaning.", "9AA3B2", GREY1]]
for i, r in enumerate(sch):
    y = 1.50 + i * 1.47
    card(s, 6.62, y, 6.30, 1.33, r[5], alpha=40 if i == 1 else 100)
    txt(s, r[0], 6.88, y + 0.12, 2.2, 0.34, NOHEMI, 17, r[4] if i == 1 else NAVY, bold=True)
    txt(s, r[1], 6.88, y + 0.50, 2.6, 0.28, HNL, 11.5, GREY_TXT, italic=True)
    pillrow(s, r[2], 6.88, y + 0.88, gap=0.07, color=r[4], size=9, h=0.28)
    rich(s, [r[3]], 9.65, y + 0.20, 3.05, 1.0, size=12)
banner(s, "A CSV is text with an implicit schema.",
       "That is where half of a career's data problems come from, and it is what the next slide is about.",
       x=0.41, y=5.95, w=12.5, h=0.52, fill=NAVY2, size=12.5)
d.notes(s, "The two axes are independent: there is text with an external schema (GML) and binary with "
           "an embedded schema (GeoPackage). What does not exist is binary with an implicit schema, "
           "because without a schema it cannot even be read.")

# ===================================================================== 15
s = d.slide("Reading a Spanish CSV")
txt(s, "Four conventions and one silent failure. Inspect the file first; configure the reader afterwards", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
code(s, """>>> with open("aforos_202509.csv", encoding="latin-1") as f:
...     for _ in range(3):
...         print(repr(f.readline()))

'id;fecha;tipo_elem;intensidad;ocupacion;vmed\\n'
'1001;01/09/2025 00:00:00;M30;328;15,19;80,50\\n'
'1006;01/09/2025 00:00:00;M30;1.418;22,07;-1,00\\n'
                    |       |     |      |
                    |       |     |      '- sentinel
                    |       |     '- thousands point
                    |       '- decimal comma
                    '- day before month""", 0.41, 1.50, 7.05, 3.30, 11)
rows = [["Symptom", "Argument"],
        ["One column; part of the data in the index", 'sep=";"'],
        ["15,19 read as text", 'decimal=","'],
        ["1.418 read as 1.418", 'thousands="."'],
        ["Chamartín shows as ChamartÃ­n", 'encoding="latin-1"'],
        ["01/09/2025 never becomes a date", "dayfirst=True"],
        ["Header starts with ï»¿", 'encoding="utf-8-sig"']]
table(s, rows, 7.75, 1.50, 5.17, [2.95, 2.22], rowh=0.47, size=11, mono_cols=(1,), mono_size=9.5)
card(s, 0.41, 5.00, 12.5, 1.35, LILAC)
txt(s, "The only one of the six that shows no visible symptom", 0.70, 5.13, 11.9, 0.30, HN, 14, PURPLE, bold=True)
rich(s, ["Without dayfirst, pandas cannot parse the date and leaves the column as text, raising nothing. The dangerous part comes next: min() and max() still work, compare strings, and return 01/09/2025 and 30/09/2025, which look exactly like the right answer. The failure surfaces much later, when sorting the series or grouping by month."],
     0.70, 5.48, 11.9, 0.80, size=13)
txt(s, "Inspection with repr() follows Lau, Gonzalez and Nolan (2023), ch. 8. Behaviour verified on the Lab 1.1 file with pandas 3.0.",
    0.41, 6.52, 11.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "The highest-yield slide of the day. The behaviour is verified on the lab file with the "
           "course's pandas version: the column stays text. Warn that older pandas versions behaved "
           "differently, silently converting month-first, and that this is why the rule is not to "
           "memorise what the library does but to always declare the convention. In exercise 2 they "
           "see it themselves: the dtype assert is the one that fails.")

# ===================================================================== 16
s = d.slide("Storing a table: by rows or by columns")
txt(s, "The same table written two different ways to disk", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
t = [["id", "date", "intensity", "occupancy"], ["1001", "2025-09-01", "328", "15.19"],
     ["1002", "2025-09-01", "121", "11.06"], ["1003", "2025-09-01", "318", "11.64"]]
table(s, t, 0.41, 1.50, 4.6, [0.9, 1.5, 1.2, 1.0], rowh=0.29, size=10,
      mono_cols=(0, 1, 2, 3), mono_size=9.5)
txt(s, "By rows (CSV): one record after another", 0.41, 2.85, 6.5, 0.28, HN, 12.5, GREY_TXT, bold=True)
cells = ["1001", "2025-09-01", "328", "15.19", "1002", "2025-09-01", "121", "…"]
cx = 0.41
for i, c in enumerate(cells):
    w = 0.35 if c == "…" else 0.095 * len(c) + 0.18
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(3.18), Inches(w), Inches(0.34))
    _fill(sh, [GREY1, "DCE0E6", GREY1, "DCE0E6"][i % 4]); _line(sh, WHITE, 1)
    txt(s, c, cx, 3.18, w, 0.34, MONO, 8.5, NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    cx += w
txt(s, "By columns (Parquet): one column after another", 0.41, 3.65, 6.5, 0.28, HN, 12.5, PURPLE, bold=True)
groups = [["1001", "1002", "1003"], ["2025-09-01", "x3"], ["328", "121", "318"], ["15.19", "11.06", "11.64"]]
gcol = ["EFE3FF", "DCC6FF", "EFE3FF", "DCC6FF"]
cx = 0.41
for gi, g in enumerate(groups):
    for c in g:
        w = 0.35 if c == "x3" else 0.095 * len(c) + 0.18
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(3.98), Inches(w), Inches(0.34))
        _fill(sh, gcol[gi]); _line(sh, WHITE, 1)
        txt(s, c, cx, 3.98, w, 0.34, MONO, 8.5, NAVY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cx += w
rich(s, ["Repeated values in a column compress almost entirely: the date, the id, the category.",
         "Two columns out of forty can be read without touching the rest of the file.",
         "Each column carries its type: a date is still a date when read back."],
     0.41, 4.55, 6.3, 1.3, size=12, space_after=6)
card(s, 7.10, 1.50, 5.82, 4.20, NAVY, alpha=100)
txt(s, "Vote", 7.40, 1.66, 4.6, 0.32, HN, 13, TEAL, bold=True)
rich(s, ["One month of hourly counts, 21,568 rows, almost one megabyte as CSV. How much smaller will the same data be as Parquet?"],
     7.40, 2.02, 5.2, 0.90, size=14, color=WHITE)
for i, o in enumerate(["2 times", "10 times", "50 times"]):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.40), Inches(3.10 + i * 0.70),
                            Inches(5.20), Inches(0.55))
    _round(sh, 14000); _fill(sh, "3B3F5C"); _noline(sh)
    txt(s, o, 7.40, 3.10 + i * 0.70, 5.20, 0.55, NOHEMI, 17, WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, "Show of hands. Measured in exercise 5 of Lab 1.1, on the projector.",
    7.40, 5.25, 5.2, 0.30, HNL, 11.5, "C9CEDA", italic=True)
txt(s, "Parquet is not always smaller: its schema and footer have a fixed cost. A 30-row table is three times larger as Parquet than as CSV. Columnar formats pay off at scale.",
    7.10, 5.85, 5.82, 0.55, HNL, 11, GREY_TXT, italic=True)
d.notes(s, "Vote before measuring. Measured answer on the course file: 7.4 times smaller (0.97 MB versus "
           "0.13 MB) and about 7 times faster to read in this environment; speed is machine-dependent. "
           "Most vote 10, some 2, almost nobody 50. The counterexample is real too: the 30-row locations "
           "table is 1.5 kB as CSV and 4.6 kB as Parquet. Both numbers come out in exercise 5.")

# ===================================================================== 17
s = d.slide("Verify what you read (1): granularity")
txt(s, "The same phenomenon admits several granularities. Choosing the wrong one invalidates the analysis",
    0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
niv = [["Fine", "one row = one hourly reading of one detector", ["1001", "01/09 08:00", "412"],
        "21,528 unique", "Hourly profile, peaks, incidents", True],
       ["Medium", "one row = one day of one detector", ["1001", "01/09", "6 840"],
        "900 rows", "Comparing days, weekends", False],
       ["Coarse", "one row = one detector", ["1001", "September", "205 200"],
        "30 rows", "Ranking detectors, AADT", False]]
for i, n in enumerate(niv):
    x = 0.41 + i * 4.22
    card(s, x, 1.50, 4.05, 3.35, LILAC if n[5] else GREY1, alpha=40 if n[5] else 100)
    txt(s, n[0], x + 0.28, 1.64, 3.4, 0.36, NOHEMI, 18, PURPLE if n[5] else GREY_TXT, bold=True)
    rich(s, [n[1]], x + 0.28, 2.06, 3.5, 0.55, size=12.5)
    table(s, [["id", "when", "veh"], n[2]], x + 0.28, 2.72, 3.5, [0.9, 1.4, 1.2], rowh=0.28,
          size=9.5, mono_cols=(0, 1, 2), mono_size=9, head_fill="9AA3B2")
    txt(s, n[3], x + 0.28, 3.42, 3.4, 0.32, HN, 14, NAVY, bold=True)
    txt(s, "Used for: " + n[4], x + 0.28, 3.85, 3.5, 0.70, HNL, 12, GREY_TXT)
banner(s, "How it is checked",
       "If one row were one hourly reading of one detector, the pair (id, fecha) would be unique. The file has 21,568 rows, of which 40 are duplicates from field-equipment retransmissions: 21,528 unique records remain. Declared and effective granularity differ, and that is discovered with one line of code, not by reading the documentation.",
       x=0.41, y=5.10, w=12.5, h=1.10, fill=NAVY2, size=12)
txt(s, "Lau, Gonzalez and Nolan (2023), ch. 9.", 0.41, 6.42, 8.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "This is exercise 3 of Lab 1.1, which comes right after this block. The 40 duplicates are "
           "real in the file they will use. Letting them find them is more effective than telling them.")

# ===================================================================== 18
s = d.slide("Verify what you read (2): sentinel values")
banner(s, "A sentinel is an impossible value used to encode a missing one.",
       "If it is not converted to NaN, it enters every average and contaminates it without producing any error.",
       x=0.41, y=1.15, w=12.5, h=0.58, fill=NAVY2, size=13.5)
txt(s, "How a gap is encoded, depending on the system", 0.41, 2.00, 6.0, 0.30, HN, 14, GREY_TXT, bold=True)
cent = [["-1", "Speed not measured (Madrid traffic counters)"],
        ["-9999", "Missing rainfall (meteorological networks)"],
        ["-99.99", "Missing monthly mean (Mauna Loa CO2)"],
        ["-32768", "No-data cell in a terrain model"],
        ['NaN, n/d, -, ""', "Spreadsheets filled in by hand"],
        ["0", "The worst of all: indistinguishable from a real zero"]]
for i, c in enumerate(cent):
    y = 2.45 + i * 0.52
    pill(s, c[0], 0.41, y, w=1.65, color=PURPLE if i == 5 else "3B3F5C", size=10, h=0.36)
    txt(s, c[1], 2.25, y + 0.06, 4.6, 0.30, HNL, 12.5, NAVY)
card(s, 7.10, 2.00, 5.82, 3.60, LILAC)
txt(s, "The effect on a mean", 7.40, 2.14, 5.2, 0.32, HN, 14, PURPLE, bold=True)
rich(s, ["Mean speed of the September counts, 21,528 records, 2,339 without a measurement:"],
     7.40, 2.52, 5.2, 0.55, size=12, color=GREY_TXT)
for i, (lab, val, col) in enumerate([("With sentinels", 58.4, "9AA3B2"), ("Converted to NaN", 65.7, PURPLE)]):
    y = 3.25 + i * 0.85
    txt(s, lab, 7.40, y, 2.2, 0.28, HNL, 12, NAVY)
    bw = 2.55 * val / 75.0
    bar = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.40), Inches(y + 0.28),
                             Inches(bw), Inches(0.34))
    _round(bar, 18000); _fill(bar, col); _noline(bar)
    txt(s, f"{val} km/h", 7.40 + bw + 0.12, y + 0.30, 1.6, 0.30, HN, 12, NAVY, bold=True)
rich(s, ["Seven kilometres per hour of bias, no exception, no warning, and a result of the right order of magnitude."],
     7.40, 4.98, 5.2, 0.55, size=12, color=GREY_TXT)
txt(s, "Null-encoding taxonomy adapted from MIT 6.S079, data cleaning lecture.",
    0.41, 6.42, 8.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "The figures are those of the real file; they are computed in exercise 4 of Lab 1.1. The "
           "message: the error does not show up as a failure, it shows up as a plausible number. That "
           "is why it has to be looked for.")

# ===================================================================== 19
s = d.section("Block 2 · Lab", "Lab 1.1 — Reading files and columnar storage",
              "26 minutes, in pairs. Exercise 0 is already done. Five more exercises,\nnumber 5 runs on the projector, plus three extensions.")
ej = [["1", "The naive read", "Diagnose why it fails without raising", "4 min"],
      ["2", "The correct read", "sep, decimal, thousands, encoding, dayfirst", "7 min"],
      ["3", "Granularity", "Check uniqueness of (id, fecha); find 40 duplicates", "4 min"],
      ["4", "Sentinel values", "Measure the bias they introduce on the mean", "4 min"],
      ["5", "CSV vs Parquet", "Resolve the vote; the 30-row counterexample", "3 min"],
      ["6", "The question of the session", "The ten busiest detectors, with their coordinates", "6 min"],
      ["A", "A public-body Excel", "Extension: three header rows and merged cells", "ext."],
      ["B", "Hourly profile", "Extension: weekday versus weekend", "ext."],
      ["C", "Provenance", "Extension: origin columns and extraction date", "ext."]]
for i, e in enumerate(ej):
    x = 0.90 + (i // 3) * 4.15
    y = 5.05 + (i % 3) * 0.48
    ext = e[3] == "ext."
    txt(s, e[0], x, y, 0.30, 0.32, NOHEMI, 15, "6B7089" if ext else TEAL, bold=True)
    txt(s, e[1], x + 0.35, y + 0.01, 2.6, 0.28, HN, 12, "9AA3B2" if ext else WHITE, bold=True)
    txt(s, e[2], x + 0.35, y + 0.24, 3.6, 0.24, HNL, 9.5, "9AA3B2")
txt(s, "Done when every check prints “passed” and you can explain which of the six reading arguments showed no visible symptom when missing.",
    0.90, 6.60, 11.8, 0.30, HNL, 11, "8E96AB", italic=True)
d.notes(s, "The six mandatory exercises add up to 26 minutes counted one by one. Circulate during "
           "exercise 2, where half the room gets stuck. Let exercise 1 run: discovering that part of "
           "the data ended up in the index is the teaching moment of the lab. If they run slow, "
           "exercise 5 can be done from the front in one minute, but 6 must be guaranteed because it "
           "feeds Lab 1.2.")

# ===================================================================== 20
s = d.slide("Checkpoint before the break")
txt(s, "Answer in the last cell of Lab 1.1", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
qs = [["The naive read returned a single column and also pushed part of each row into the index. Explain the exact mechanism that produces both.", True],
      ["The 2,339 sentinel values shift the mean speed by about 7 km/h. In which direction, and why does the error have that sign and not the opposite?", False],
      ["A colleague asks for the dataset and only has Excel. Which format do you send, what information is lost, and how do you document it?", True]]
for i, q in enumerate(qs):
    y = 1.60 + i * 1.45
    card(s, 0.41, y, 12.5, 1.25, LILAC if q[1] else GREY1, alpha=40 if q[1] else 100)
    badge(s, i + 1, 0.75, y + 0.40, PURPLE if q[1] else TEAL_D)
    rich(s, [q[0]], 1.45, y + 0.28, 11.1, 0.80, size=14.5, anchor=MSO_ANCHOR.MIDDLE)
txt(s, "Five-minute break. Lab 1.2 needs no new installs: open it and check that top10.parquet is in the folder.",
    0.41, 6.20, 12.5, 0.30, HNL, 12, GREY_TXT, italic=True)
d.notes(s, "Expected answers. (1) The default separator is the comma; the header has none, hence one "
           "column; data rows do have commas, from the decimals, hence extra fields that pandas places "
           "in the index. (2) Downwards, because -1 is smaller than any real speed. (3) xlsx or CSV with "
           "semicolons; types are lost and so is the guarantee that Excel will not reinterpret dates.")

# ===================================================================== 21
s = d.section("Block 3", "Spatial data: object and field",
              "The second and third rows of the map. Two models, two structures, two format families,\nthe reference system that binds them and the operation that joins them. Then Lab 1.2.",
              ["object", "field", ".shp", ".tif", "EPSG", "zonal statistics"])
d.notes(s, "Twelve minutes, six slides, same order as the tabular block: model first, then formats, "
           "then the pitfall the lab practises, then the operation that answers the question.")

# ===================================================================== 22
s = d.slide("Two spatial models: object and field")
txt(s, "The most useful distinction students take away from this session", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
card(s, 0.41, 1.50, 6.08, 4.50, GREY1, alpha=100)
txt(s, "Object model", 0.70, 1.64, 5.4, 0.38, NOHEMI, 19, TEAL_D, bold=True)
rich(s, ["The territory is occupied by discrete entities with a definite boundary and their own attributes."],
     0.70, 2.08, 5.5, 0.60, size=13)
for i, p in enumerate([[0.95, 2.95, 1.5, 1.05], [2.60, 2.90, 1.3, 1.20], [4.05, 3.05, 1.6, 0.90]]):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(p[0]), Inches(p[1]), Inches(p[2]), Inches(p[3]))
    _round(sh, 9000); _fill(sh, ["CBD4DC", "AEBAC6", "92A1B0"][i]); _line(sh, WHITE, 1.5)
txt(s, "each polygon carries its own row of attributes", 0.70, 4.25, 5.5, 0.26, HNL, 11, GREY_TXT,
    italic=True, align=PP_ALIGN.CENTER)
table(s, [["id", "name", "elev_m"], ["1", "Villanueva", "612"], ["2", "Los Sauces", "701"]],
      1.35, 4.58, 3.9, [0.8, 1.8, 1.3], rowh=0.26, size=9.5, mono_cols=(0, 1, 2), mono_size=9,
      head_fill="9AA3B2")
pill(s, "GeoDataFrame", 0.70, 5.55, w=1.60, color=TEAL_D, size=9)
pillrow(s, [".shp", ".gpkg", ".geojson"], 2.50, 5.55, gap=0.08, color="9AA3B2", size=9)
card(s, 6.83, 1.50, 6.08, 4.50, LILAC)
txt(s, "Field model", 7.12, 1.64, 5.4, 0.38, NOHEMI, 19, PURPLE, bold=True)
rich(s, ["A quantity takes a value at every point of the territory. It is measured on a regular grid of cells."],
     7.12, 2.08, 5.5, 0.60, size=13)
tone = ["F3E9FF", "E7D5FF", "DCC1FF", "D0ADFF", "C49AFF", "B886FF"]
for r in range(4):
    for c in range(8):
        v = min(5, round((r * 0.9 + c * 0.55 + ((r * 5 + c * 3) % 3) * 0.4) / 1.7))
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.55 + c * 0.36), Inches(2.90 + r * 0.36),
                                Inches(0.36), Inches(0.36))
        _fill(sh, tone[v]); _line(sh, WHITE, 1)
txt(s, "one cell, one value; position comes from the grid", 7.12, 4.42, 5.5, 0.26, HNL, 11, GREY_TXT,
    italic=True, align=PP_ALIGN.CENTER)
code(s, "array([[612., 615., 619., ...],\n       [608., 611., 616., ...]])", 7.55, 4.75, 4.35, 0.62, 9.5)
pill(s, "DataArray", 7.12, 5.55, w=1.35, color=PURPLE, size=9)
pillrow(s, [".tif", ".asc", ".nc"], 8.65, 5.55, gap=0.08, color="9AA3B2", size=9)
banner(s, "The same terrain admits both models.",
       "The choice depends on the question: “which municipality is this?” is an object question; “what is the elevation here?” is a field question.",
       x=0.41, y=6.18, w=12.5, h=0.52, fill=NAVY2, size=12.5)
d.notes(s, "Ask for examples from their degree: a pier is an object, concrete temperature is a field; "
           "a road section is an object, its slope is a field. The typical confusion is treating a field "
           "as objects because it arrived as a table of points. Simple Features geometry types are in "
           "appendix A.3.")

# ===================================================================== 23
s = d.slide("Object formats: anatomy of a shapefile")
txt(s, "A 1990s format that still carries official Spanish cartography", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
parts = [[".shp", "Geometry", "required", "3B3F5C"],
         [".shx", "Index into the .shp", "required", "3B3F5C"],
         [".dbf", "Attribute table, in 1983 dBase", "required", "3B3F5C"],
         [".prj", "Reference system, as WKT text", "optional", PURPLE],
         [".cpg", "Character encoding", "optional", PURPLE]]
for i, p in enumerate(parts):
    y = 1.55 + i * 0.80
    pill(s, p[0], 0.41, y + 0.06, w=0.95, color=p[3], size=12, h=0.44)
    txt(s, p[1], 1.60, y + 0.02, 4.2, 0.32, HN, 14, NAVY, bold=True)
    txt(s, p[2], 1.60, y + 0.34, 4.2, 0.26, HNL, 11, PURPLE if p[3] == PURPLE else GREY_TXT, italic=True)
card(s, 6.30, 1.55, 3.20, 4.05, GREY1, alpha=100)
txt(s, "Why we still read it", 6.58, 1.70, 2.7, 0.32, HN, 14, TEAL_D, bold=True)
rich(s, ["Default download at CNIG and most public administrations",
         "Every program opens it", "Simple enough to survive an e-mail"],
     6.58, 2.12, 2.70, 3.0, size=12, space_after=10)
card(s, 9.72, 1.55, 3.20, 4.05, LILAC)
txt(s, "Why we stop writing it", 10.00, 1.70, 2.7, 0.32, HN, 14, PURPLE, bold=True)
rich(s, ["Field names truncated to 10 characters", "One geometry type per layer",
         "2 GB limit per file; no real nulls", "Lose the .prj and nobody knows where the data is"],
     10.00, 2.12, 2.70, 3.0, size=12, space_after=9)
banner(s, "In exercise 1 of Lab 1.2",
       "you delete the .prj on purpose and watch gdf.crs become None, with no warning. Then you repair it with set_crs, which declares, and not with to_crs, which transforms. GeoJSON and GeoPackage are compared in appendix A.7.",
       x=0.41, y=5.80, w=12.5, h=0.62, fill=NAVY2, size=12)
txt(s, "Esri Shapefile Technical Description (1998).", 0.41, 6.58, 8.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "The 10-character truncation is the error they will see most often in their careers: a column "
           "called intensidad_media_diaria arrives as intensidad. Confusing set_crs and to_crs is the "
           "second; say the difference twice.")

# ===================================================================== 24
s = d.slide("Field formats: the raster grid")
txt(s, "A grid that knows where it is. Five properties define any raster", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
tone = ["E7EAEE", "D3D9E0", "BFC8D2", "AAB7C4", "96A6B6", "8295A8"]
GX, GY, CELL = 0.80, 2.05, 0.42
for r in range(6):
    for c in range(7):
        v = min(5, max(0, round((r * 0.7 + c * 0.6 + ((r * 7 + c * 3) % 4) * 0.5) / 2)))
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(GX + c * CELL), Inches(GY + r * CELL),
                                Inches(CELL), Inches(CELL))
        _fill(sh, WHITE if (r >= 4 and c < 2) else tone[v]); _line(sh, WHITE, 1)
dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(GX - 0.10), Inches(GY - 0.10), Inches(0.20), Inches(0.20))
_fill(dot, PURPLE); _noline(dot)
txt(s, "origin", GX - 0.62, GY - 0.44, 1.3, 0.26, HN, 11, PURPLE, bold=True, align=PP_ALIGN.CENTER)
txt(s, "no-data cells", GX, GY + 4 * CELL + 0.86, 1.7, 0.26, HNL, 10, GREY_TXT, align=PP_ALIGN.CENTER)
props = [["Reference system", "src.crs", "EPSG:25830. Defines what the origin coordinates mean."],
         ["Cell size", "src.res", "25 m × 25 m. Sets the resolution and the area each value represents."],
         ["Extent", "src.bounds", "The four coordinates of the rectangle the grid covers."],
         ["Number of bands", "src.count", "One in a terrain model; three in an orthophoto; thirteen in Sentinel-2."],
         ["No-data value", "src.nodata", "-32768. A sentinel, with the same risks as the -1 in the table."]]
for i, p in enumerate(props):
    y = 1.70 + i * 0.90
    txt(s, p[0], 4.70, y, 2.9, 0.30, HN, 14, NAVY, bold=True)
    txt(s, p[1], 4.70, y + 0.32, 2.9, 0.26, MONO, 10.5, PURPLE)
    rich(s, [p[2]], 7.85, y + 0.02, 5.05, 0.70, size=12.5)
banner(s, "A raster does not store the coordinates of each cell:",
       "it stores the origin and the cell size and derives them. That is why it is so much smaller than the same information as a table of points.",
       x=0.41, y=6.20, w=12.5, h=0.52, fill=NAVY2, size=12.5)
d.notes(s, "The last sentence explains why the field model exists as its own structure and is not "
           "represented as a table: position is implicit. It connects with extension B of Lab 1.2. "
           "Multiband scenes are Friday.")

# ===================================================================== 25
s = d.slide("The coordinate reference system")
txt(s, "What binds object and field. Three EPSG codes to recognise; the full treatment is session 11", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
crs = [["EPSG:4326", "WGS 84", "Latitude and longitude in degrees.",
        "What a GPS receiver gives and what most APIs return. GeoJSON requires it, in longitude-latitude order: a classic source of swapped coordinates.",
        "Nothing is measured here.", False],
       ["EPSG:25830", "ETRS89 / UTM 30N", "Metres.",
        "Official cartography for most of mainland Spain. The zone depends on longitude, not on the region: 25829, 25830 and 25831 for zones 29N, 30N and 31N.",
        "Measure here.", True],
       ["EPSG:3857", "Web Mercator", "Metres, but distorted.",
        "What browser base maps and OpenStreetMap tiles use.",
        "Display, do not measure.", False]]
for i, c in enumerate(crs):
    x = 0.41 + i * 4.22
    card(s, x, 1.50, 4.05, 4.25, LILAC if c[5] else GREY1, alpha=40 if c[5] else 100)
    txt(s, c[0], x + 0.28, 1.64, 3.4, 0.40, MONO, 18, PURPLE if c[5] else NAVY, bold=True)
    txt(s, c[1], x + 0.28, 2.12, 3.4, 0.30, HN, 14, GREY_TXT, bold=True)
    txt(s, c[2], x + 0.28, 2.48, 3.4, 0.30, HNL, 13, NAVY, italic=True)
    rich(s, [c[3]], x + 0.28, 2.92, 3.5, 1.60, size=12.5)
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x + 0.28), Inches(5.00),
                            Inches(3.50), Inches(0.55))
    _round(sh, 14000); _fill(sh, PURPLE if c[5] else NAVY2); _noline(sh)
    txt(s, c[4], x + 0.28, 5.00, 3.50, 0.55, HN, 13, WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
banner(s, "Working rule for today:",
       "check gdf.crs   →   to_crs(25830)   →   compute area or length.   Never in the opposite order.",
       x=0.41, y=6.05, w=12.5, h=0.56, fill=NAVY2, size=13)
d.notes(s, "No projections, no datums today. In exercise 2 of Lab 1.2 they compute a municipality's "
           "area in degrees, see the geopandas warning, reproject and compare with the declared value. "
           "That sequence teaches more than any theory.")

# ===================================================================== 26
s = d.slide("The CRS mismatch, before and after")
txt(s, "What you will see in exercise 3 of Lab 1.2, and the question to ask before running it",
    0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
s.shapes.add_picture("/home/claude/curso/figuras/crs_antes_despues.png",
                     Inches(0.41), Inches(1.55), Inches(12.5), Inches(4.44))
card(s, 0.41, 6.08, 6.08, 0.62, GREY1, alpha=100)
rich(s, ["Nobody complains. Metres and degrees on the same plane, and both libraries draw what they are told."],
     0.70, 6.18, 5.6, 0.45, size=12)
card(s, 6.83, 6.08, 6.08, 0.62, LILAC)
rich(s, [[("set_crs declares what the coordinates already were; to_crs transforms them. In that order, never the reverse.", True)]],
     7.12, 6.18, 5.6, 0.45, size=12)
d.notes(s, "Ask for the prediction before showing the left panel: will the points land on the "
           "municipalities? Almost everyone says yes. The left panel shows the problem raises no error; "
           "the right one, that the fix is two different operations.")

# ===================================================================== 27
s = d.slide("What joins them: zonal statistics")
txt(s, "The operation that connects the field model with the object model", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
txt(s, "Field", 0.90, 1.55, 2.6, 0.28, HN, 13, PURPLE, bold=True, align=PP_ALIGN.CENTER)
tone = ["F3E9FF", "E7D5FF", "DCC1FF", "D0ADFF", "C49AFF", "B886FF"]
for r in range(7):
    for c in range(7):
        v = min(5, round((r * 0.8 + c * 0.5 + ((r * 5 + c * 3) % 3) * 0.5) / 1.8))
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.62 + c * 0.32), Inches(1.95 + r * 0.32),
                                Inches(0.32), Inches(0.32))
        _fill(sh, tone[v]); _line(sh, WHITE, 1)
txt(s, "one cell, one value", 0.62, 4.28, 2.3, 0.26, HNL, 10.5, GREY_TXT, italic=True, align=PP_ALIGN.CENTER)
pl = s.shapes.add_shape(MSO_SHAPE.MATH_PLUS, Inches(3.35), Inches(2.85), Inches(0.30), Inches(0.30))
_fill(pl, "9AA3B2"); _noline(pl)
txt(s, "Object", 4.60, 1.55, 2.6, 0.28, HN, 13, TEAL_D, bold=True, align=PP_ALIGN.CENTER)
pent = s.shapes.add_shape(MSO_SHAPE.PENTAGON, Inches(4.25), Inches(2.15), Inches(1.5), Inches(1.15))
_fill(pent, WHITE); _line(pent, TEAL_D, 2.25)
rr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.40), Inches(3.45), Inches(1.2), Inches(0.9))
_round(rr, 9000); _fill(rr, WHITE); _line(rr, TEAL_D, 2.25)
txt(s, "polygons of interest", 4.15, 4.42, 2.1, 0.26, HNL, 10.5, GREY_TXT, italic=True, align=PP_ALIGN.CENTER)
ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(6.40), Inches(2.88), Inches(0.75), Inches(0.26))
_fill(ar, PURPLE); _noline(ar)
txt(s, "Table of objects with a summary of the field", 7.50, 1.55, 5.4, 0.28, HN, 13, NAVY, bold=True)
table(s, [["municipality", "mean_elev_m", "max_elev_m"], ["Villanueva", "612.4", "689.1"],
          ["Los Sauces", "701.8", "774.3"], ["Valdemuestra", "658.2", "712.9"]],
      7.50, 1.95, 5.4, [2.0, 1.8, 1.6], rowh=0.32, size=10, mono_cols=(0, 1, 2), mono_size=9.5)
code(s, "from rasterio.mask import mask\nclip, _ = mask(src, [geom], crop=True)\nvalues = clip[0]\nvalues[values != src.nodata].mean()", 7.50, 3.40, 5.4, 1.05, 9.5)
card(s, 0.41, 4.85, 6.85, 1.60, GREY1, alpha=100)
txt(s, "The same operation, throughout a career", 0.70, 4.97, 6.3, 0.28, HN, 13, TEAL_D, bold=True)
rich(s, ["Mean elevation of each municipality", "Accumulated rainfall over each catchment",
         "Maximum slope along each alignment section", "Mean vegetation index in each parcel",
         "Mean flood depth per block"],
     0.70, 5.28, 6.3, 1.05, size=11, space_after=2)
rich(s, ["In Lab 1.2 you apply it twice: sampling the terrain model at ten points, and averaging it inside nine polygons."],
     7.50, 4.90, 5.4, 0.90, size=12.5)
txt(s, "Rey, Arribas-Bel and Wolf (2023), ch. 5, section on hybrids between structures.",
    0.41, 6.60, 9.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "This operation has a name and they should learn it, because it is what an engineering office "
           "will ask for without knowing what it is called. The fast production version is the rasterstats "
           "library; the teaching version is on the slide.")

# ===================================================================== 28
s = d.section("Block 3 · Lab", "Lab 1.2 — Object and field:\nfrom the point to the zonal statistic",
              "22 minutes, in pairs. Roles swap: whoever typed in Lab 1.1 now navigates.")
ej = [["1", "Break the shapefile", "Delete the .prj, see crs=None, repair with set_crs", "4 min"],
      ["2", "Areas in degrees and metres", "Compare with the declared area; relative error", "5 min"],
      ["3", "Geographic table and mismatch", "Points without CRS over degrees; predict; then repair", "5 min"],
      ["4", "Open the surface", "Guided: crs, res, bounds, nodata and the effect of not masking", "2 min"],
      ["5", "The question of the session", "src.sample at the ten points; check plausible range", "5 min"],
      ["6", "Zonal statistics", "Mean elevation per municipality with rasterio.mask", "if time"],
      ["A", "Multi-layer GeoPackage", "Extension: two layers, one file; compare sizes", "ext."],
      ["B", "From surface to table", "Extension: a raster window as a DataFrame", "ext."]]
for i, e in enumerate(ej):
    x = 0.90 + (i // 4) * 6.10
    y = 4.95 + (i % 4) * 0.48
    dim = e[3] in ("ext.", "if time")
    txt(s, e[0], x, y, 0.30, 0.32, NOHEMI, 15, "6B7089" if dim else TEAL, bold=True)
    txt(s, e[1], x + 0.35, y + 0.01, 3.0, 0.28, HN, 12, "9AA3B2" if dim else WHITE, bold=True)
    txt(s, e[2], x + 0.35, y + 0.24, 5.4, 0.24, HNL, 9.5, "9AA3B2")
txt(s, "Done when exercise 5 prints the mean elevation and you can explain why sampling the raster with the wrong CRS would not have raised an error: it would have returned elevations from somewhere else.",
    0.90, 6.90, 11.8, 0.30, HNL, 11, "8E96AB", italic=True)
d.notes(s, "Exercise 4 is guided, code given, to save time. Exercise 5 closes the session and must be "
           "guaranteed. Exercise 6 is the zonal statistic: if there is no time, show the solution from "
           "the front in two minutes, because the operation matters even if they do not code it today.")

# ===================================================================== 29
s = d.slide("The answer")
txt(s, "What it took to answer a one-line question", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
steps = [["Read", "A CSV with four Spanish conventions and one failure that raises nothing", "read_csv, six arguments"],
         ["Verify", "Declared versus effective granularity; 40 duplicates; 2,339 sentinels", "duplicated, replace"],
         ["Aggregate", "Mean intensity per measurement point; the ten largest", "groupby, sort_values, merge"],
         ["Locate", "Coordinates turned into geometries, with the reference system declared", "set_crs, to_crs"],
         ["Sample", "The field model queried at ten positions, no-data handled", "src.sample"]]
for i, p in enumerate(steps):
    x = 0.41 + i * 2.53
    card(s, x, 1.50, 2.36, 3.15, LILAC if i == 4 else GREY1, alpha=40 if i == 4 else 100)
    badge(s, i + 1, x + 0.95, 1.70, PURPLE if i == 4 else TEAL_D)
    txt(s, p[0], x + 0.18, 2.32, 2.0, 0.32, HN, 15, NAVY, bold=True, align=PP_ALIGN.CENTER)
    rich(s, [p[1]], x + 0.18, 2.72, 2.0, 1.30, size=11.5, align=PP_ALIGN.CENTER)
    txt(s, p[2], x + 0.18, 4.22, 2.0, 0.30, MONO, 8.5, GREY_TXT, align=PP_ALIGN.CENTER)
    if i < 4:
        ar = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + 2.40), Inches(2.95), Inches(0.14), Inches(0.20))
        _fill(ar, "9AA3B2"); _noline(ar)
banner(s, "Of the five steps, three are verification and format, and only two are analysis.",
       "That proportion is not a flaw of this exercise: it is the normal proportion of work with real data. Sessions 4 to 9 of the module are devoted entirely to the first three steps.",
       x=0.41, y=4.95, w=12.5, h=0.85, fill=NAVY2, size=13)
txt(s, "The actual figure for the mean elevation is the one you obtained in exercise 5. It is deliberately not on these slides.",
    0.41, 6.05, 12.5, 0.30, HNL, 12, GREY_TXT, italic=True)
d.notes(s, "Do not give the number. Ask two pairs for theirs and check they agree. If they do not, one "
           "of them almost certainly did not mask the no-data or did not check the CRS, and diagnosing "
           "that live is worth more than the slide.")

# ===================================================================== 30
s = d.slide("Back to the map")
txt(s, "Three rows covered; four scheduled", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
map_table(s, 1.50, "Status", lambda r: "covered today" if r[6] else r[5])
banner(s, "The project folder, revisited",
       "Of the twelve files of Exercise 0 you can now open seven: the two CSVs, the Excel, the GeoJSON, the shapefile, the GeoTIFF and the logger file. The HTML table and the IFC are Friday and session 3. The point cloud is appendix A.1. The extension told you nothing; the first bytes and the model told you everything.",
       x=0.41, y=5.30, w=12.5, h=1.05, fill=NAVY2, size=12)
d.notes(s, "Closing the pyramid: same table as slide 10, with today's rows ticked. Then go back to the "
           "folder of Exercise 0 and count together: seven of twelve. It is the same slide the students "
           "saw at minute seven, and now they can read it.")

# ===================================================================== 31
s = d.slide("Synthesis")
txt(s, "Six statements that summarise the session", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
items = [["Model, structure and format are three different levels.", "Learning a new format takes minutes; learning a new structure, weeks."],
         ["A CSV does not carry its schema.", "The read_csv arguments are that schema, written by hand and with no guarantee of being right."],
         ["Granularity is checked, not assumed.", "One line of code separates declared from effective granularity."],
         ["An unconverted sentinel produces wrong means without raising any exception.", "The result has the right order of magnitude, which is why nobody reviews it."],
         ["Object and field are different models with different structures.", "The choice depends on the question, not on the data."],
         ["Zonal statistics join the two models.", "It is the spatial operation you will be asked for most often, without anyone naming it."]]
for i, it in enumerate(items):
    y = 1.50 + i * 0.85
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.41), Inches(y + 0.10), Inches(0.26), Inches(0.26))
    _fill(dot, PURPLE if i % 2 == 0 else TEAL_D); _noline(dot)
    txt(s, it[0], 0.90, y, 11.9, 0.32, HN, 15, NAVY, bold=True)
    txt(s, it[1], 0.90, y + 0.34, 11.9, 0.36, HNL, 12.5, GREY_TXT)
d.notes(s, "Read them slowly. These are the six statements they should be able to repeat in session 4 "
           "without notes.")

# ===================================================================== 32
s = d.section("Three minutes before you leave", "Exit ticket",
              "Anonymous, three short answers. Read before session 2 and discussed at its start.")
qs = [["1", "One thing you learned today.", ""],
      ["2", "One thing that is still unclear.", ""],
      ["3", "A colleague sends you three gigabytes of hourly sensor readings as CSV, the model of an overpass as IFC, and the municipal cartography as a shapefile.",
       "For each file: which data model, what would you open it with, and what would be your first check."]]
for i, q in enumerate(qs):
    y = 4.72 + i * 0.62
    h = 1.15 if i == 2 else 0.55
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.90), Inches(y), Inches(11.9), Inches(h))
    _round(sh, 8000); _fill(sh, "31344B"); _noline(sh)
    txt(s, q[0], 1.10, y, 0.5, h, NOHEMI, 20, TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, q[1], 1.70, y + (0.10 if i == 2 else 0), 10.9, 0.50, HNL, 14, WHITE,
        anchor=MSO_ANCHOR.TOP if i == 2 else MSO_ANCHOR.MIDDLE)
    if q[2]:
        txt(s, q[2], 1.70, y + 0.62, 10.9, 0.40, HNL, 12.5, "C9CEDA")
d.notes(s, "Three real minutes, with the clock on. Question 3 is the only one with a right answer and "
           "tells you whether the session landed: tabular, hierarchical object with semantics, spatial "
           "object; pandas in chunks, ifcopenshell, geopandas; and as first checks granularity, the count "
           "of elements per class, and the .prj. Read all the answers to 1 and 2 before Friday.")

# ===================================================================== 33
s = d.slide("Homework: the format card")
txt(s, "A format card on your own data. Due before session 4 (9 October), and reused there in the data-quality report",
    0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
card(s, 0.41, 1.50, 7.60, 4.60, LILAC)
rich(s, ["Choose a dataset you will actually use: from your final-year project, a current course or your company. In a format you have never opened. Hand in half a page with:"],
     0.70, 1.68, 7.0, 0.62, size=13.5)
fields = ["What it is, who publishes it and under which licence",
          "Data model and the structure you read it into",
          "Granularity: what one row or one cell represents",
          "Scope: what population it represents and what is left out",
          "Temporality: which moment each date refers to",
          "Units or reference system, and where you found them",
          "The line of code that opens it",
          "One faithfulness problem you found"]
for i, f in enumerate(fields):
    y = 2.45 + i * 0.44
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.75), Inches(y + 0.08), Inches(0.14), Inches(0.14))
    _fill(dot, PURPLE); _noline(dot)
    txt(s, f, 1.05, y, 6.6, 0.32, HNL, 13, NAVY)
card(s, 8.32, 1.50, 4.60, 2.20, GREY1, alpha=100)
txt(s, "Choose one with defects", 8.62, 1.66, 4.0, 0.32, HN, 15, TEAL_D, bold=True)
rich(s, ["A toy dataset produces a toy card. Session 4 needs a dataset with real problems in it, because the quality report is built on top of this one."],
     8.62, 2.06, 4.0, 1.40, size=12.5)
card(s, 8.32, 3.90, 4.60, 2.20, LILAC)
txt(s, "Session 2, Friday 25", 8.62, 4.06, 4.0, 0.32, HN, 15, PURPLE, bold=True)
rich(s, ["Extraction and quality: from the document to the validated datum. Tables out of a geotechnical annex in PDF, a web table, and a Sentinel-2 scene."],
     8.62, 4.46, 4.0, 1.40, size=12.5)
d.notes(s, "The dataset has to be theirs: a toy dataset produces a toy card. Insist on choosing something "
           "with defects, because session 4 needs them.")

# ===================================================================== 34
s = d.slide("References")
txt(s, "The first three are the recommended readings for the topic", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
refs = [["Lau, S., Gonzalez, J. and Nolan, D. (2023).", "Learning Data Science: Data Wrangling, Exploration, Visualization, and Modeling with Python. O'Reilly. Chapters 2, 8 and 9. Open version: learningds.org", True],
        ["Rey, S., Arribas-Bel, D. and Wolf, L. J. (2023).", "Geographic Data Science with Python. CRC Press. Chapters 3 and 5. Open version: geographicdata.science", True],
        ["Wickham, H. (2014).", "Tidy Data. Journal of Statistical Software, 59(10).", True],
        ["Rubin, D. B. (1976).", "Inference and missing data. Biometrika, 63(3), 581-592.", False],
        ["Rule, A. et al. (2019).", "Ten simple rules for writing and sharing computational analyses in Jupyter Notebooks. PLOS Computational Biology, 15(7), e1007007.", False],
        ["ISO 19125-1.", "Geographic information: Simple feature access. Part 1: Common architecture. Open Geospatial Consortium.", False],
        ["Codd, E. F. (1970).", "A relational model of data for large shared data banks. Communications of the ACM, 13(6), 377-387.", False]]
for i, r in enumerate(refs):
    y = 1.50 + i * 0.68
    if r[2]:
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.41), Inches(y), Inches(0.08), Inches(0.56))
        _fill(bar, PURPLE); _noline(bar)
    txt(s, r[0], 0.70, y, 3.5, 0.56, HN, 12, NAVY if r[2] else GREY_TXT, bold=True)
    rich(s, [r[1]], 4.35, y, 8.55, 0.60, size=11.5, color=NAVY if r[2] else GREY_TXT, spacing=1.08)
txt(s, "Technical specifications consulted: IETF RFC 7946 (GeoJSON); OGC GeoPackage Encoding Standard; Esri Shapefile Technical Description (1998).",
    0.41, 6.32, 12.5, 0.26, HNL, 9.5, GREY_TXT, italic=True)
txt(s, "Courses consulted in the design of the session: CMU 15-388; UC Berkeley Data 100; MIT 6.S079; UIUC CEE 492.",
    0.41, 6.60, 12.5, 0.26, HNL, 9.5, GREY_TXT, italic=True)
d.notes(s, "The first three are open and linked from the repository.")

# ===================================================================== A.0
s = d.section("Appendix", "Reference material",
              "Fourteen slides that are not projected and stay in the handout.\nThey develop what the session only names, and serve as a reserve if time allows.")
d.notes(s, "Order: other structures; Wickham's five problems (session 4); Simple Features; text-file "
           "families; temporality (session 6); missingness mechanisms (session 7); vector formats "
           "compared; format criteria; cheat sheet; data sources; decision table; study questions; "
           "prerequisites.")

# ===================================================================== A.1
s = d.slide("A.1. Other structures in your career")
txt(s, "Outside today's scope; named so that you recognise them", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
otros = [["Point cloud", "Millions of coordinates with intensity and class. One 2 × 2 km PNOA-LiDAR tile holds tens of millions of points. The .las of Exercise 0 is a small one.", [".las", ".laz", ".e57"], "laspy, PDAL"],
         ["BIM model", "Objects with class, properties and relations, after ISO 16739. A database in the shape of a file. The .ifc of Exercise 0 is a minimal one.", [".ifc"], "ifcopenshell"],
         ["Instrumentation time series", "A table with a time index and its own problems: time zone, gaps, mixed frequencies. The .dat of Exercise 0 is one.", [".txt", ".dat", "SQL"], "pandas, xarray"],
         ["Network", "Nodes and edges with geometry. Roads, drainage, water supply, routes. Session 11.", ["OSM", ".graphml"], "networkx, osmnx"]]
for i, o in enumerate(otros):
    x = 0.41 + (i % 2) * 6.42
    y = 1.50 + (i // 2) * 2.45
    card(s, x, y, 6.08, 2.25, GREY1, alpha=100)
    badge(s, i + 1, x + 0.28, y + 0.24, PURPLE if i % 2 == 0 else TEAL_D)
    txt(s, o[0], x + 0.90, y + 0.28, 3.6, 0.36, HN, 15, NAVY, bold=True)
    txt(s, o[3], x + 4.55, y + 0.30, 1.30, 0.30, MONO, 9.5, PURPLE, align=PP_ALIGN.RIGHT)
    rich(s, [o[1]], x + 0.28, y + 0.92, 5.55, 0.90, size=12.5)
    pillrow(s, o[2], x + 0.28, y + 1.82, gap=0.08, color="9AA3B2", size=9, h=0.28)
txt(s, "All four install with pip in Colab. IFC is the one that connects most with the rest of the degree: it lets you query a structural model without opening the program that created it.",
    0.41, 6.50, 12.5, 0.30, HNL, 12, GREY_TXT, italic=True)

# ===================================================================== A.2
s = d.slide("A.2. Five ways a table is messy")
txt(s, "Wickham lists them for data in general. All five appear in civil-engineering spreadsheets. Developed in session 4",
    0.41, 1.02, 11.8, 0.30, HNL, 14.5, GREY_TXT)
rows = [["Problem", "How it looks in a project file", "Fix in pandas"],
        ["Column headers are values, not variable names", "One column per year in a traffic yearbook; one column per depth in an SPT table", "melt"],
        ["Several variables in one column", "\"S-1 / 1.50-1.95 m\" as a sample identifier", "str.split, str.extract"],
        ["Variables in both rows and columns", "A 'measurement type' row alternating level and flow", "pivot"],
        ["Several observational units in one table", "Borehole header (coordinates, elevation, date) mixed with its samples", "Split into two keyed tables"],
        ["One unit spread across several tables", "One sheet per borehole; one file per month of monitoring", "concat with a source column"]]
table(s, rows, 0.41, 1.50, 12.5, [4.2, 5.7, 2.6], rowh=0.72, size=12, mono_cols=(2,), mono_size=10, bold_col=0)
txt(s, "The fourth and fifth are the most frequent in civil engineering, because the natural unit of field work is the borehole or the month, not the observation.",
    0.41, 5.95, 12.5, 0.30, HNL, 12.5, GREY_TXT, italic=True)
txt(s, "Wickham (2014), section 3. Examples adapted to the domain.", 0.41, 6.42, 8.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)

# ===================================================================== A.3
s = d.slide("A.3. Simple Features geometries")
txt(s, "Standardised geometries: the common vocabulary of every GIS, fixed in an ISO standard",
    0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
geoms = [["Point", "Location without dimension", "Borehole, lamp post, traffic counter"],
         ["LineString", "Sequence of points", "Alignment, sewer, road section"],
         ["Polygon", "Closed surface", "Parcel, municipality, catchment"]]
for i, g in enumerate(geoms):
    x = 0.41 + i * 4.22
    card(s, x, 1.50, 4.05, 3.05, GREY1, alpha=100)
    cx, cy = x + 2.02, 2.35
    if i == 0:
        for p in [(-0.5, 0), (0.3, 0.3), (0.55, -0.35)]:
            sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + p[0] - 0.09), Inches(cy + p[1] - 0.09),
                                    Inches(0.18), Inches(0.18))
            _fill(sh, PURPLE); _noline(sh)
    elif i == 1:
        pts = [(-0.9, 0.35), (-0.3, -0.25), (0.25, 0.2), (0.9, -0.3)]
        for k in range(3):
            a, b = pts[k], pts[k + 1]
            ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                    Inches(cx + min(a[0], b[0])), Inches(cy + (a[1] + b[1]) / 2),
                                    Inches(abs(b[0] - a[0])), Pt(2.2))
            _fill(ln, PURPLE); _noline(ln)
            ln.rotation = -18 if (b[1] - a[1]) * (b[0] - a[0]) < 0 else 18
        for p in pts:
            sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + p[0] - 0.06), Inches(cy + p[1] - 0.06),
                                    Inches(0.12), Inches(0.12))
            _fill(sh, NAVY); _noline(sh)
    else:
        sh = s.shapes.add_shape(MSO_SHAPE.PENTAGON, Inches(cx - 0.85), Inches(cy - 0.55),
                                Inches(1.7), Inches(1.1))
        _fill(sh, LILAC, alpha=90); _line(sh, PURPLE, 2)
    txt(s, g[0], x + 0.28, 3.10, 3.4, 0.36, MONO, 16, NAVY, bold=True)
    txt(s, g[1], x + 0.28, 3.50, 3.4, 0.28, HNL, 12.5, GREY_TXT)
    txt(s, g[2], x + 0.28, 3.84, 3.5, 0.40, HNL, 12.5, NAVY)
card(s, 0.41, 4.80, 12.5, 1.35, LILAC)
txt(s, "Multi variants and practical consequences", 0.70, 4.94, 11.9, 0.30, HN, 14, PURPLE, bold=True)
rich(s, ["Each type has a Multi variant: MultiPolygon for a municipality with detached enclaves, MultiLineString for an interrupted section. A shapefile declares one geometry type per layer. In GeoPackage each table declares its own, which may be generic, and a GeoDataFrame allows mixtures; in both cases homogeneous layers are more interoperable."],
     0.70, 5.28, 11.9, 0.80, size=13)
txt(s, "ISO 19125-1, Geographic information: Simple feature access. Open Geospatial Consortium.",
    0.41, 6.42, 9.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)

# ===================================================================== A.4
s = d.slide("A.4. Four families of text file")
txt(s, "Classified by how values are separated, not by extension", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
fam = [["Delimited", "One character separates fields: comma, semicolon, tab, space.", "aforos.csv, a logger export", "pd.read_csv(sep=...)", True],
       ["Fixed width", "No separator: each field always occupies the same columns. Needs the codebook.", "DGT microdata, old yearbooks", "pd.read_fwf(colspecs=...)", False],
       ["Hierarchical", "Tree of keys and values, with nesting and optional fields.", "API response, INSPIRE cadastre, IFC", "json.load, pd.json_normalize", False],
       ["Loosely structured", "Patterns but no table: equipment logs, vendor headers, reports.", "TOA5 header, pumping-station log", "regular expressions", False]]
for i, f in enumerate(fam):
    y = 1.50 + i * 1.22
    card(s, 0.41, y, 12.5, 1.10, LILAC if f[4] else GREY1, alpha=40 if f[4] else 100)
    txt(s, f[0], 0.70, y + 0.12, 2.5, 0.34, NOHEMI, 16, PURPLE if f[4] else NAVY, bold=True)
    txt(s, f[3], 0.70, y + 0.54, 2.8, 0.30, MONO, 9.5, GREY_TXT)
    rich(s, [f[1]], 3.80, y + 0.14, 4.8, 0.85, size=12.5)
    rich(s, ["In civil engineering: " + f[2]], 8.90, y + 0.14, 3.8, 0.85, size=12.5, color=GREY_TXT)
banner(s, "The extension is a convention, not a guarantee.", "A file called .csv can contain any of the four.",
       x=0.41, y=6.42, w=12.5, h=0.44, fill=NAVY2, size=12.5)

# ===================================================================== A.5
s = d.slide("A.5. Temporality")
txt(s, "A date column can refer to three different moments, and rarely says which. Developed in session 6",
    0.41, 1.02, 11.8, 0.30, HNL, 14.5, GREY_TXT)
mom = [["When it happened", "The vehicle crossed the loop", "18/09/2026 08:42:11"],
       ["When it was recorded", "The equipment wrote it to memory", "18/09/2026 08:45:00"],
       ["When it was stored", "It reached the central database", "18/09/2026 09:12:37"]]
ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.40), Inches(2.18), Inches(10.4), Pt(2))
_fill(ln, "C9CFD8"); _noline(ln)
for i, m in enumerate(mom):
    x = 1.40 + i * 3.55
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x - 0.11), Inches(2.08), Inches(0.22), Inches(0.22))
    _fill(dot, PURPLE if i == 0 else "9AA3B2"); _line(dot, WHITE, 1.5)
    txt(s, m[2], x - 1.3, 1.62, 2.6, 0.30, MONO, 11, NAVY, bold=True, align=PP_ALIGN.CENTER)
    txt(s, m[0], x - 1.3, 2.45, 2.6, 0.32, HN, 15, NAVY, bold=True, align=PP_ALIGN.CENTER)
    txt(s, m[1], x - 1.3, 2.80, 2.6, 0.50, HNL, 12, GREY_TXT, align=PP_ALIGN.CENTER)
casos = [["Undeclared time zone", "A file in local time does not say which. Mixed with one in UTC, the offset is one or two hours depending on the month."],
         ["The October clock change", "The last Sunday of October has hour 02:00 twice. An hourly series for that day has 25 records and a duplicate key."],
         ["Record dates used as event dates", "A monitoring report dated Monday may contain readings from the previous Friday."],
         ["Declared versus actual frequency", "A logger set to 15 minutes that drops to hourly, unannounced, when the battery is low."]]
for i, c in enumerate(casos):
    x = 0.41 + (i % 2) * 6.42
    y = 3.75 + (i // 2) * 1.35
    card(s, x, y, 6.08, 1.20, GREY1, alpha=100)
    txt(s, c[0], x + 0.28, y + 0.12, 5.5, 0.30, HN, 13.5, TEAL_D, bold=True)
    rich(s, [c[1]], x + 0.28, y + 0.46, 5.5, 0.65, size=12)
txt(s, "Lau, Gonzalez and Nolan (2023), ch. 5 and ch. 9.", 0.41, 6.55, 8.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)

# ===================================================================== A.6
s = d.slide("A.6. Why a value is missing")
txt(s, "Three mechanisms with different consequences. Developed in session 7", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
mec = [["MCAR", "Missing completely at random", "Depends neither on the observed nor on the unobserved.",
        "A communications outage that erases one hour for every detector, regardless of traffic.",
        "Complete-case analysis is unbiased but loses precision.", False],
       ["MAR", "Missing at random, conditionally", "Depends on the observed; conditional on it, no longer on the missing value.",
        "Older detectors fail more often, and we know which ones are old.",
        "Tractable by modelling the observed variables. The assumption cannot be verified from the data.", False],
       ["MNAR", "Missing not at random", "Still depends on the unobserved value after conditioning on everything available.",
        "An extensometer stops recording just when the movement exceeds its range.",
        "Deleting or averaging biases towards the dangerous side. Requires modelling the mechanism.", True]]
for i, m in enumerate(mec):
    x = 0.41 + i * 4.22
    card(s, x, 1.50, 4.05, 4.70, LILAC if m[5] else GREY1, alpha=40 if m[5] else 100)
    txt(s, m[0], x + 0.28, 1.64, 3.4, 0.42, MONO, 20, PURPLE if m[5] else NAVY, bold=True)
    txt(s, m[1], x + 0.28, 2.14, 3.5, 0.44, HN, 13, GREY_TXT, bold=True)
    rich(s, [m[2]], x + 0.28, 2.66, 3.5, 0.70, size=12)
    txt(s, "In civil engineering", x + 0.28, 3.50, 3.4, 0.26, HN, 11, PURPLE if m[5] else TEAL_D, bold=True)
    rich(s, [m[3]], x + 0.28, 3.80, 3.5, 1.00, size=12)
    txt(s, "Consequence", x + 0.28, 4.90, 3.4, 0.26, HN, 11, PURPLE if m[5] else TEAL_D, bold=True)
    rich(s, [m[4]], x + 0.28, 5.20, 3.5, 0.90, size=12)
txt(s, "The third case is the usual one in instrumentation: the instrument stops measuring precisely when the phenomenon becomes interesting.  ·  Rubin (1976), as presented in MIT 6.S079.",
    0.41, 6.42, 12.5, 0.26, HNL, 11.5, GREY_TXT, italic=True)

# ===================================================================== A.7
s = d.slide("A.7. Object formats compared")
txt(s, "Read shapefile because administrations send it; write GeoPackage because it is 2026",
    0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
rows = [["", "Shapefile", "GeoJSON", "GeoPackage"],
        ["Files per layer", "3 minimum, usually 5", "1", "1 (SQLite database)"],
        ["Reference system", "in a separate .prj, easily lost", "WGS 84 lon-lat (RFC 7946)", "inside the file; several allowed"],
        ["Field names", "10 characters", "free", "free"],
        ["Several layers in one file", "no", "no: one FeatureCollection", "yes: several vector layers and tiles"],
        ["Typical origin", "IGN, MITMA, administrations", "web services, APIs", "QGIS, your own work"]]
table(s, rows, 0.41, 1.50, 12.5, [3.0, 3.1, 3.1, 3.3], rowh=0.62, size=12, bold_col=0, hot_col=3)
card(s, 0.41, 5.10, 12.5, 1.00, GREY1, alpha=100)
txt(s, "Also in circulation", 0.70, 5.22, 11.9, 0.28, HN, 13, TEAL_D, bold=True)
rich(s, ["KML and KMZ for Google Earth. GML for INSPIRE services, the format in which the Spanish cadastre publishes parcels and buildings. DXF when a design drawing is read as geometry without attributes."],
     0.70, 5.52, 11.9, 0.52, size=12.5)
txt(s, "IETF RFC 7946; OGC GeoPackage Encoding Standard.", 0.41, 6.32, 9.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)

# ===================================================================== A.8
s = d.slide("A.8. Choosing a format")
txt(s, "Four questions, in this order", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
crit = [["Who will open it?", "If the recipient works in Excel, the format is .xlsx or CSV, even at the cost of losing types. The recipient criterion dominates every other."],
        ["How many times will it be read?", "A file read once can be CSV. One re-read in every working session should be Parquet or GeoPackage."],
        ["Is there a spatial component?", "If so, the next question is object or field, and that already fixes the format family."],
        ["Must it survive archiving?", "For delivery and long-term archive: open, documented format, with metadata in a readable file alongside."]]
for i, c in enumerate(crit):
    y = 1.50 + i * 1.18
    card(s, 0.41, y, 12.5, 1.06, LILAC if i == 0 else GREY1, alpha=40 if i == 0 else 100)
    badge(s, i + 1, 0.70, y + 0.30, PURPLE if i == 0 else TEAL_D)
    txt(s, c[0], 1.42, y + 0.15, 4.2, 0.36, HN, 15, NAVY, bold=True)
    rich(s, [c[1]], 5.75, y + 0.16, 6.9, 0.80, size=12.5)
banner(s, "Working rule:",
       "distinguish three formats that need not coincide. Working (Parquet, GeoPackage), exchange (whatever the recipient asks for), and archive copy (open, documented, provenance alongside).",
       x=0.41, y=6.30, w=12.5, h=0.52, fill=NAVY2, size=12.5)

# ===================================================================== A.9
s = d.slide("A.9. How each format opens in Python")
txt(s, "Cheat sheet. Everything runs in Google Colab; asterisk means pip install", 0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
rows = [["Format", "Library", "Read", "Write"],
        [".csv .txt", "pandas", 'pd.read_csv(f, sep=";", decimal=",", encoding="latin-1")', "df.to_csv(f, index=False)"],
        [".txt fixed width", "pandas", "pd.read_fwf(f, colspecs=[...])", "—"],
        [".xlsx", "pandas + openpyxl", "pd.read_excel(f, sheet_name=None, header=4)", "df.to_excel(f, index=False)"],
        [".json", "json, pandas", "pd.json_normalize(json.load(open(f)))", 'df.to_json(f, orient="records")'],
        [".parquet", "pandas + pyarrow", "pd.read_parquet(f, columns=[...])", "df.to_parquet(f)"],
        [".sqlite", "sqlite3, pandas", 'pd.read_sql("SELECT ...", con)', "df.to_sql(table, con)"],
        [".shp .geojson .gpkg", "geopandas", "gpd.read_file(f, layer=...)", 'gdf.to_file(f, driver="GPKG")'],
        [".tif .asc", "rasterio*", "rasterio.open(f); src.read(1); src.sample(xy)", 'rasterio.open(f, "w", **profile)'],
        [".nc .h5", "xarray*", "xr.open_dataset(f)", "ds.to_netcdf(f)"],
        [".las .laz", "laspy[lazrs]*", "laspy.read(f)", "las.write(f)"],
        [".ifc", "ifcopenshell*", 'ifcopenshell.open(f).by_type("IfcBeam")', "model.write(f)"],
        [".dxf", "ezdxf*", "ezdxf.readfile(f).modelspace()", "doc.saveas(f)"]]
table(s, rows, 0.41, 1.50, 12.5, [2.1, 2.1, 5.1, 3.2], rowh=0.40, size=10.5,
      mono_cols=(2, 3), mono_size=9, bold_col=0)

# ===================================================================== A.10
s = d.slide("A.10. Where to get real data")
txt(s, "Sources you will use in the module and in the final project", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
src = [["CNIG / IGN", "Administrative boundaries, BTN, terrain models MDT02, MDT05, MDT25, PNOA orthophotos and LiDAR", [".shp", ".tif", ".laz"]],
       ["datos.madrid.es", "Traffic counters, air quality, EMT buses, mobility", [".csv", ".json", ".shp"]],
       ["Catastro (INSPIRE)", "Parcels, buildings and addresses by municipality", [".gml"]],
       ["MITMA", "State road network, average daily traffic, ports and railways", [".shp", ".xlsx"]],
       ["DGT", "Accident microdata and vehicle fleet", [".csv", ".xlsx"]],
       ["AEMET OpenData", "Observations, climatologies and forecasts, with API key", [".json"]],
       ["INE", "Population, housing and economic indicators", [".csv", ".xlsx", ".px"]],
       ["Copernicus", "ERA5 climate reanalysis, Sentinel imagery, land cover", [".nc", ".tif"]],
       ["OpenStreetMap", "Roads, buildings and points of interest, via osmnx", [".pbf", ".geojson"]]]
for i, it in enumerate(src):
    x = 0.41 + (i % 3) * 4.22
    y = 1.50 + (i // 3) * 1.60
    card(s, x, y, 4.05, 1.45, LILAC if i % 4 == 0 else GREY1, alpha=40 if i % 4 == 0 else 100)
    txt(s, it[0], x + 0.25, y + 0.12, 3.6, 0.32, HN, 14, NAVY, bold=True)
    rich(s, [it[1]], x + 0.25, y + 0.48, 3.6, 0.60, size=11, color=GREY_TXT, spacing=1.05)
    pillrow(s, it[2], x + 0.25, y + 1.08, gap=0.07, color="9AA3B2", size=8.5, h=0.26)
txt(s, "Portals reorganise their downloads frequently. The course repository keeps a frozen copy of everything used in class, with download date and licence in SOURCES.md.",
    0.41, 6.42, 12.5, 0.30, HNL, 11.5, GREY_TXT, italic=True)

# ===================================================================== A.11
s = d.slide("A.11. Format decision table")
txt(s, "Summary of the criteria in A.8", 0.41, 1.02, 11.0, 0.30, HNL, 14.5, GREY_TXT)
rows = [["Situation", "Format", "Reason"],
        ["Small table for someone who works in Excel", ".xlsx or CSV with ; and ,", "They will open it; losing types is accepted"],
        ["Table re-read many times or above 100 MB", ".parquet", "Types kept, smaller, column reads"],
        ["Table queried and updated by several people", "PostgreSQL / PostGIS", "Concurrent writes, transactions, one source of truth"],
        ["Nested API response, configuration, metadata", ".json", "Natural format for hierarchies"],
        ["Vector layer for your own analysis", ".gpkg", "Multi-layer, CRS embedded, no practical limits"],
        ["Vector layer to deliver to an administration", ".shp, keeping the .gpkg", "It is what they ask for; keep the good copy"],
        ["Vector layer for a web viewer or a repository", ".geojson", "Text, git-friendly, WGS 84 lon-lat by specification"],
        ["Elevation, imagery, any continuous quantity", "GeoTIFF", "Georeference and no-data inside the file"],
        ["Grid with a time axis", "NetCDF", "xarray opens it as labelled dimensions"],
        ["Structure or building model for exchange", ".ifc", "Vendor-neutral objects with meaning"]]
table(s, rows, 0.41, 1.50, 12.5, [5.0, 3.3, 4.2], rowh=0.45, size=11, mono_cols=(1,), mono_size=10,
      bold_col=0, hot_col=1)

# ===================================================================== A.12
s = d.slide("A.12. Questions to work on your own")
txt(s, "Five transfer questions. Handed out with the material and discussed at the start of session 2",
    0.41, 1.02, 11.8, 0.30, HNL, 14.5, GREY_TXT)
qs = ["A monitoring file has one column per sensor and one row per instant. Is it tidy in Wickham's sense? If not, which of the five problems does it show and how is it fixed?",
      "A colleague computes the mean annual rainfall of a station and gets −412 mm. What has almost certainly happened, and which check would have caught it earlier?",
      "You have a road alignment as a shapefile and a digital elevation model. Describe, without code, how you would obtain the longitudinal terrain profile along the alignment. Which data models are involved?",
      "Justify why a GeoJSON of the Madrid region with the geometry of all its municipalities is several times larger than the same data as GeoPackage.",
      "A slope extensometer stops recording during the heaviest rainfall episode of the winter. Classify the missingness mechanism and explain its consequence for the maximum displacement computed over the period."]
for i, q in enumerate(qs):
    y = 1.50 + i * 1.02
    card(s, 0.41, y, 12.5, 0.92, LILAC if i % 2 == 0 else GREY1, alpha=40 if i % 2 == 0 else 100)
    badge(s, i + 1, 0.70, y + 0.22, PURPLE if i % 2 == 0 else TEAL_D)
    rich(s, [q], 1.42, y + 0.14, 11.2, 0.70, size=12.5)

# ===================================================================== A.13
s = d.slide("A.13. Prerequisites and pre-reading")
txt(s, "What is assumed, what had to be read, and what is needed in the room", 0.41, 1.02, 11.5, 0.30, HNL, 14.5, GREY_TXT)
cols = [["Assumed from Module 1", ["Python syntax and basic data structures", "pandas: read_csv, indexing, groupby, merge", "numpy: arrays and vectorised operations", "matplotlib: figure, axes, line plot"], False],
        ["Pre-reading (required)", ["Lau, Gonzalez and Nolan (2023), sections 8.2 and 8.3", "Open access at learningds.org", "Ten minutes of reading", "Three-question quiz, due Thursday"], True],
        ["In the room", ["Laptop with a browser and a Google account", "Google Colab, no local install", "Course repository open in a tab", "Data preloaded: nothing downloaded in class"], False]]
for i, c in enumerate(cols):
    x = 0.41 + i * 4.22
    card(s, x, 1.50, 4.05, 4.40, LILAC if c[2] else GREY1, alpha=40 if c[2] else 100)
    badge(s, i + 1, x + 0.28, 1.70, PURPLE if c[2] else TEAL_D)
    txt(s, c[0], x + 0.28, 2.32, 3.5, 0.40, HN, 15, NAVY, bold=True)
    rich(s, c[1], x + 0.28, 2.85, 3.5, 2.8, size=12.5, space_after=9)
txt(s, "Whoever could not do the pre-reading can follow the session, but should do it before Lab 1.1.",
    0.41, 6.20, 12.5, 0.30, HNL, 12, GREY_TXT, italic=True)

d.save("/home/claude/Session1_Data_models_TEMPLATE.pptx")
print("slides:", len(d.prs.slides))
