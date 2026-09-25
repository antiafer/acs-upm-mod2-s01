"""Session 2 deck — Unstructured data: extraction from documents, web pages and images.
Built on the ACS-UPM template through tpl.py."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from tpl import *
from tpl import _round, _fill, _noline, _line, _run
from tpl import session_strip, timeline
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

MID = "CFD8DC"
BASE = os.path.dirname(HERE)
FIG = os.path.join(BASE, "figuras")

import tpl
tpl.FOOTER_CENTRE = "Module 2. S02: Unstructured data"

d = Deck()
ACC = [PURPLE, TEAL_D]
acc = lambda i: ACC[i % 2]


def sub(s, text):
    txt(s, text, 0.41, 1.02, 12.0, 0.30, HNL, 14.5, GREY_TXT)


def cite(s, text, y=6.78):
    txt(s, text, 0.41, y, 12.0, 0.22, HNL, 9.5, GREY_TXT, italic=True)


# ===================================================================== 1
d.cover("Session 2", "Unstructured data:", "documents, web and images",
        "Module 2. Data Fusion, Preparation and Visualization applied to Civil Engineering",
        "ACS–UPM Diploma on Engineering, Data Science and AI",
        "Antía Fernández", "2026", "Notebook: bit.ly/acs-mod2-s2")
d.notes(d.prs.slides[-1],
        "State the goal at the start: by the end of the session the class will have measured the same "
        "drought from an official bulletin and from satellite imagery, and compared the two. Everything "
        "else is the road to that comparison.")

# ===================================================================== 1b
s = d.slide("Structure of the course")
session_strip(s, 20, highlight={1, 2, 3, 19, 20}, y=1.30, h=0.34)
timeline(s, [
    {"tag": "Data basics", "kicker": "Session 1", "title": "Landscape of\ndata formats",
     "date": "Sept 18, 2026", "meta": "2 h",
     "body": "Data models, structures and file formats: CSV, JSON, Parquet, GeoJSON, shapefiles."},
    {"kicker": "Session 2", "title": "Unstructured civil\nengineering data",
     "date": "Sept 25, 2026", "meta": "2 h",
     "body": "Extraction from documents, web pages and imagery: PDF reports, HTML tables, satellite images."},
    {"kicker": "Session 3", "title": "Data acquisition:\nAPIs and web scraping",
     "date": "Oct 2, 2026", "meta": "2 h",
     "body": "Acquisition through REST APIs and web extraction, and the rules that govern it."},
    {"tag": "Data visualization", "kicker": "Session 19", "title": "Visualization\ndesign principles",
     "date": "Dec 4, 2026", "meta": "2 h",
     "body": "Principles of visual encoding, chart selection and the reporting of uncertainty."},
    {"kicker": "Session 20", "title": "Interactive\nvisualizations",
     "date": "Dec 11, 2026", "meta": "2 h",
     "body": "Interactive visualisation with Plotly: exploration, filtering and publication."},
], marker=1, x0=0.53, pitch=2.55, colw=2.25)
d.notes(s, "The five sessions of this module taught by Antía Fernández; today is the second. Thirty "
           "seconds: the point is that last week the data could be read, and this week they have to be "
           "extracted.")

# ===================================================================== 2
s = d.slide("Three questions from last Friday")
sub(s, "Two minutes, answered aloud. Then the point most often raised in the exit tickets")
qs = [("Which read_csv argument corrects  Ã¡  where  á  was expected?", 'encoding="latin-1"'),
      ("Three gigabytes of hourly sensor data, re-read daily for analysis: CSV or Parquet, and one reason.", "Parquet: types preserved, seven times smaller, column reads"),
      ("Two map layers do not overlap. What is the first thing to check?", "the reference system of both layers")]
for i, (q, a) in enumerate(qs):
    y = 1.55 + i * 1.32
    card(s, 0.41, y, 12.5, 1.15, LILAC if i % 2 == 0 else GREY1, alpha=40 if i % 2 == 0 else 100)
    badge(s, i + 1, 0.72, y + 0.35, acc(i))
    rich(s, [q], 1.42, y + 0.18, 7.6, 0.85, size=14.5, anchor=MSO_ANCHOR.MIDDLE)
    card(s, 9.30, y + 0.28, 3.35, 0.60, WHITE, alpha=100)
    txt(s, a, 9.45, y + 0.28, 3.05, 0.60, MONO, 10, NAVY, bold=True, anchor=MSO_ANCHOR.MIDDLE)
banner(s, "From the exit tickets:", "the point most often raised, addressed now.",
       x=0.41, y=5.60, w=12.5, h=0.52, fill=NAVY2, size=13.5)
txt(s, "The answers are revealed only after someone offers them. Cover the right-hand column when projecting.",
    0.41, 6.30, 12.0, 0.28, HNL, 11.5, GREY_TXT, italic=True)
d.notes(s, "Retrieval practice, two minutes. Ask, wait, let someone answer, then uncover. Then read the "
           "one confusion that came up most in the exit tickets and answer it in one minute. If nobody "
           "handed in tickets, skip that line.")

# ===================================================================== 3
s = d.slide("Learning objectives")
sub(s, "By the end of the session, students should be able to:")
obj = [("Distinguish", "a native PDF from a scanned one, and select the extraction route accordingly."),
       ("Extract", "a table that spans several pages and reconstruct it without duplicating its header."),
       ("Validate", "an extracted table against statements made in the document itself and against physical ranges."),
       ("Verify", "a table extracted by an AI assistant by means of a five-line log, and state when that log is required."),
       ("Convert", "Sentinel-2 digital numbers into reflectance using the product metadata, and quantify the error of omitting the conversion."),
       ("Compare", "a quantity derived from an image with the same quantity published in a document.")]
for i, (v, r) in enumerate(obj):
    y = 1.55 + i * 0.86
    card(s, 0.41, y, 12.5, 0.76, LILAC if i < 4 else GREY1, alpha=40 if i < 4 else 100)
    badge(s, f"{i + 1:02d}", 0.70, y + 0.16, acc(0) if i < 4 else acc(1))
    txt(s, v, 1.36, y + 0.20, 1.45, 0.36, HN, 15, NAVY, bold=True)
    rich(s, [r], 2.90, y + 0.22, 9.7, 0.45, size=13.5)
txt(s, "Objectives 1 to 4 are assessed in Lab 2.1; objectives 5 and 6 in Lab 2.2.", 0.41, 6.80, 11, 0.26, HNL, 10, GREY_TXT, italic=True)
d.notes(s, "Observable verbs only. Objective 4 is the new one relative to the syllabus wording, and the "
           "one students will use most in their careers.")

# ===================================================================== 4
s = d.slide("Session roadmap")
sub(s, "Each expository block precedes the laboratory that practises it. 110 minutes including the break; 10 in reserve")
rows = [("0", "Opening: three questions, the aim, three files, the map", "10", False),
        ("1", "Route 1, rules: what a PDF contains", "12", False),
        ("LAB", "Lab 2.1: the annex by rules, the certificate by assistant", "25", True),
        ("", "Break", "5", False),
        ("2", "Routes 2 and 3, OCR and assistants: how each one fails", "10", False),
        ("3", "The reservoir: a web table claims, an image checks", "12", False),
        ("LAB", "Lab 2.2: the web table, then the reservoir on two dates", "28", True),
        ("4", "Close: two routes to one number; exit ticket", "8", False)]
for i, (n, t, mins, hot) in enumerate(rows):
    y = 1.50 + i * 0.64
    card(s, 0.41, y, 12.5, 0.56, LILAC if hot else GREY1, alpha=40 if hot else 100)
    if n == "LAB":
        pill(s, "LAB", 0.62, y + 0.12, w=0.72, color=PURPLE, size=9)
    elif n:
        badge(s, n, 0.68, y + 0.08, acc(i), d=0.40)
    txt(s, t, 1.55, y + 0.12, 8.5, 0.34, HN if n else HNL, 14, NAVY, bold=bool(n))
    txt(s, mins + " min", 10.30, y + 0.14, 1.1, 0.30, HN, 13, NAVY, align=PP_ALIGN.RIGHT)
    pill(s, "laptops" if hot else "notebook", 11.55, y + 0.13, w=1.10, color=PURPLE if hot else "9AA3B2", size=9)
txt(s, "Run the installation cell of Lab 2.2 during the break: rasterio and scikit-image take about a minute in Colab.",
    0.41, 6.72, 12.5, 0.28, HNL, 11.5, GREY_TXT, italic=True)
d.notes(s, "The schedule counts the opening and the close. If Lab 2.1 overruns, the slack is taken from "
           "there; Lab 2.2 answers the goal and must be protected.")

# ===================================================================== 5
s = d.section("BLOCK 0", "How much water is in the reservoir?",
              "A basin authority publishes the answer in a web bulletin. By the end of the session\nwe will have checked that figure independently, from a satellite image.")
d.notes(s, "Say it and move on. The point of announcing the destination is that every block can be "
           "placed on the road to it.")

# ===================================================================== 5a
s = d.slide("Last week's folder: three files left")
sub(s, "Each of the three files that could not be opened last week is one block of today's session")
code(s, """proyecto_variante_M-407/
|-- aforos_202509.csv            read in session 1
|-- pm_ubicaciones.csv           read in session 1
|-- municipios_shp/              read in session 1
|-- mdt25_madrid.tif             read in session 1
|-- ...
|
|-- anejo_geotecnico.pdf         block 1: a report
|-- boletin_embalses.html        block 3: a web page
'-- S2B_MSIL2A_20250427.SAFE/    block 3: a satellite image""",
     0.41, 1.50, 7.40, 3.10, 11)
three = [("A report", "anejo_geotecnico.pdf", "A geotechnical annex with a table of 63 SPT tests. Block 1.", PURPLE),
         ("A web page", "boletin_embalses.html", "A reservoir bulletin that states a water surface. Block 3.", TEAL_D),
         ("A satellite image", "Sentinel-2, two dates", "The same reservoir, measured from space. Block 3.", PURPLE)]
for i, (t, f, b, col) in enumerate(three):
    y = 1.50 + i * 1.05
    card(s, 8.10, y, 4.82, 0.95, LILAC if i != 1 else GREY1, alpha=40 if i != 1 else 100)
    badge(s, i + 1, 8.32, y + 0.25, col)
    txt(s, t, 8.92, y + 0.08, 3.8, 0.30, HN, 13.5, NAVY, bold=True)
    txt(s, f, 8.92, y + 0.36, 3.8, 0.26, MONO, 9.5, col)
    rich(s, [b], 8.92, y + 0.60, 3.9, 0.35, size=10.5, color=GREY_TXT)
banner(s, "Reading is over.", "From here on, data have to be extracted, and an extraction can be wrong without anything failing.",
       x=0.41, y=4.85, w=12.5, h=0.52, fill=NAVY2, size=13.5)
txt(s, "Block 2 covers the case in which a document has no text at all, only an image of it.",
    0.41, 5.55, 12.5, 0.30, HNL, 12, GREY_TXT, italic=True)
d.notes(s, "The hook. Return to the session 1 folder: three files could not be opened, and each one is a "
           "block today. The report is block 1; the web page and the image are both about the reservoir "
           "and form block 3. Block 2, between them, deals with documents that have no text layer at all.")

# ===================================================================== 5b
s = d.slide("Degrees of structure in engineering data")
sub(s, "Last week the schema was known before reading; today it has to be recovered")
cols = [("Structured", "the schema is known before reading",
         ["sensor tables", "Parquet files", "relational databases", "the traffic counts of session 1"],
         "Reading is a configuration problem: separator, types, encoding.", False),
        ("Semi-structured", "structure is present, but flexible",
         ["JSON responses from APIs", "HTML tables", "GTFS transit feeds", "today's reservoir bulletin"],
         "The structure must be located and flattened; it is there, but not in the shape needed.", False),
        ("Unstructured", "the structure is apparent only to a human reader",
         ["reports and annexes in PDF", "scanned certificates", "drawings and photographs", "today's geotechnical annex"],
         "The table has to be reconstructed, and the reconstruction verified against the source.", True)]
for i, (t, defn, ex, body, hot) in enumerate(cols):
    x = 0.41 + i * 4.22
    card(s, x, 1.50, 4.05, 3.95, LILAC if hot else GREY1, alpha=40 if hot else 100)
    badge(s, i + 1, x + 0.25, 1.68, PURPLE if hot else TEAL_D)
    txt(s, t, x + 0.85, 1.72, 3.0, 0.40, HN, 16, NAVY, bold=True)
    txt(s, defn, x + 0.25, 2.22, 3.55, 0.30, HNL, 11.5, GREY_TXT, italic=True)
    rich(s, ex, x + 0.25, 2.62, 3.55, 1.65, size=12, space_after=4)
    rich(s, [body], x + 0.25, 4.45, 3.55, 0.95, size=11.5, color=GREY_TXT)
ar1 = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(0.41), Inches(5.62), Inches(12.5), Inches(0.30))
_fill(ar1, "DCE0E6"); _noline(ar1)
txt(s, "extraction effort and risk", 0.41, 5.62, 12.5, 0.30, HN, 11, NAVY, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
card(s, 0.41, 6.05, 12.5, 0.85, NAVY, alpha=100)
txt(s, "A satellite image sits in both places at once.", 0.70, 6.14, 5.0, 0.28, HN, 12.5, TEAL, bold=True)
txt(s, "As an array it is perfectly structured: the field model of session 1. As information it is not: the quantity of interest, here the surface of water, is not stored anywhere and has to be derived and then checked against an independent source.",
    0.70, 6.40, 11.9, 0.48, HNL, 11, "CFD8DC", spacing=1.08)
d.notes(s, "The bridge from session 1. Structured data are read; unstructured data are extracted, and "
           "extraction is falible. A project produces geotechnical reports, as-built drawings, inspection "
           "photographs and minutes, against a comparatively small stream of clean tables: most project "
           "information sits on the right of this spectrum. The remark on images matters: students tend "
           "to think a raster is structured because it opens as an array, and then forget that the number "
           "they want is a derived quantity that needs validating like any extracted one.")

# ===================================================================== 6
s = d.slide("How to extract information: four routes")
sub(s, "Every source considered today is handled by one of these four routes")
routes = [("Rules", "pdfplumber, read_html, rasterio", "fails visibly",
           "A wrong shape, missing rows, a header among the data. The error can be seen.", "Recurring, auditable and batch work", True),
          ("OCR", "Tesseract on a scanned page", "fails silently",
           "Replaces characters with similar ones and gives no sign of it. An age of 7 becomes a letter; 25,1 becomes 20.)", "Scanned documents, with every digit that matters checked", False),
          ("AI assistants", "any language model", "fails convincingly",
           "Fills gaps with plausible values that were never on the page. The table appears complete and consistent.", "One-off documents with complicated layouts, never without the log", False),
          ("Ask for the source", "the spreadsheet the PDF was made from", "cannot fail",
           "The table is never transcribed. Most published PDFs originate in a spreadsheet that someone still has.", "Before any of the above", False)]
for i, (name, tool, how, body, when, hot) in enumerate(routes):
    x = 0.41 + i * 3.16
    card(s, x, 1.50, 3.00, 4.55, LILAC if hot else GREY1, alpha=40 if hot else 100)
    badge(s, i + 1, x + 0.25, 1.70, acc(i))
    txt(s, name, x + 0.85, 1.72, 2.1, 0.45, HN, 15, NAVY, bold=True)
    txt(s, tool, x + 0.25, 2.30, 2.55, 0.30, MONO, 9, GREY_TXT)
    pill(s, how, x + 0.25, 2.72, w=2.10, color=acc(i), size=9.5)
    rich(s, [body], x + 0.25, 3.25, 2.55, 1.55, size=11.5)
    txt(s, "Use it for", x + 0.25, 4.95, 2.5, 0.26, HN, 10, acc(i), bold=True)
    rich(s, [when], x + 0.25, 5.22, 2.55, 0.75, size=11, color=GREY_TXT)
banner(s, "Extraction reconstructs a table that the file never stored.",
       "Validation is therefore part of the procedure, not an optional addition.",
       x=0.41, y=6.20, w=12.5, h=0.52, fill=NAVY2, size=13.5)
d.notes(s, "The pyramid's top. Rules, OCR and assistants each fail in their own characteristic way, and "
           "the protocol is the same for the three: recount, range-check, spot-check, log. Route four is "
           "the one professionals forget: ask whether the source file exists before extracting anything. "
           "We return to this slide at the close.")

# ===================================================================== 7
s = d.section("BLOCK 1, THE REPORT", "Rules: what a PDF actually contains",
              "Pieces of text placed at coordinates; no rows, no columns, no table.\nThe tool rebuilds the table from the layout, and it may rebuild it wrongly.",
              ["pdffonts", "pdfplumber", "extract_tables", "validate"])
d.notes(s, "Twelve minutes, five slides.")

# ===================================================================== 8
s = d.slide("What a PDF file actually contains")
sub(s, "The same table twice: as a reader sees it, and as the file stores it")
txt(s, "What a reader sees", 0.41, 1.45, 6.0, 0.30, HN, 14, NAVY, bold=True)
s.shapes.add_picture(os.path.join(FIG, "pdf_what_you_see.png"), Inches(0.41), Inches(1.82), Inches(6.08), Inches(1.12))
txt(s, "A table with a header, rows and columns.", 0.41, 3.00, 6.0, 0.28, HNL, 11.5, GREY_TXT, italic=True)
txt(s, "What the file stores", 6.83, 1.45, 6.0, 0.30, HN, 14, PURPLE, bold=True)
s.shapes.add_picture(os.path.join(FIG, "pdf_what_file_stores.png"), Inches(6.83), Inches(1.82), Inches(6.09), Inches(1.12))
txt(s, "Separate pieces of text, each with a position. Nothing else.", 6.83, 3.00, 6.0, 0.28, HNL, 11.5, PURPLE, italic=True)
card(s, 0.41, 3.45, 4.60, 2.60, GREY1, alpha=100)
txt(s, "Six of the purple boxes, as stored", 0.66, 3.55, 4.2, 0.28, HN, 12, NAVY, bold=True)
table(s, [["text", "x", "y"], ["Prof.", "153", "128"], ["(m)", "174", "128"], ["S-1", "97", "143"],
          ["1,50", "168", "143"], ["Relleno", "236", "143"], ["antrópico", "266", "143"]],
      0.66, 3.90, 4.10, [1.80, 1.15, 1.15], rowh=0.29, size=10, mono_cols=(0, 1, 2), mono_size=10)
pts = [("Nothing says that 1,50 is a depth", "Only that it is drawn at x = 168. It belongs to the column Prof. (m) because it happens to sit underneath it."),
       ("Even one label is two pieces", "The header Prof. (m) is stored as two separate strings, and so is Relleno antrópico."),
       ("The tool rebuilds the table", "It regroups pieces into cells, cells into rows and rows into a table, using the positions and the drawn lines. It can regroup them wrongly.")]
for i, (t, b) in enumerate(pts):
    y = 3.45 + i * 0.88
    card(s, 5.25, y, 7.67, 0.78, LILAC if i == 2 else GREY1, alpha=40 if i == 2 else 100)
    badge(s, i + 1, 5.48, y + 0.17, acc(i))
    txt(s, t, 6.08, y + 0.07, 6.7, 0.30, HN, 13, NAVY, bold=True)
    rich(s, [b], 6.08, y + 0.37, 6.7, 0.40, size=11)
banner(s, "A PDF records where to draw each piece of text, not what the table means.",
       "Extracting a table means rebuilding it.",
       x=0.41, y=6.25, w=12.5, h=0.50, fill=NAVY2, size=13)
d.notes(s, "This is the central idea of the first half. A PDF is a set of drawing instructions: draw the "
           "text 1,50 at this position, draw S-1 at that one, draw a line from here to there. It does not "
           "record that 1,50 is the depth of the first test of borehole S-1. The table the reader sees is "
           "an effect of alignment, and the extraction tool has to infer it from the positions.\n\n"
           "Point at the purple boxes: each one is a separate piece of text. The coordinates in the small "
           "table are real, taken with pdfplumber from the lab annex; students can reproduce them with "
           "page.extract_words(). Stress the second point: even a two-word header is two pieces, which is "
           "why a tool can split a label across two columns.\n\n"
           "Technical note if asked: the file actually stores glyphs, the drawn shapes of characters, "
           "together with a font; pdfplumber groups them back into words. The word glyph is not needed "
           "in class.")

# ===================================================================== 8b
s = d.slide("First question: is there any text at all?")
sub(s, "Both files carry a .pdf extension. One contains text; the other is a photograph of a page")
cases = [("anejo_geotecnico.pdf", "thumb_annex.png", """$ pdffonts anejo_geotecnico.pdf
name              type
----------------- ------
Helvetica         Type 1
Helvetica-Bold    Type 1
Helvetica-Oblique Type 1""", "Fonts are listed: the file contains text, and the pieces of the previous slide exist.",
          "NATIVE: route 1, rules", PURPLE, LILAC),
         ("certificado_hormigon_escaneado.pdf", "thumb_certificate.png", """$ pdffonts certificado_escaneado.pdf
name              type
----------------- ------

        (no fonts at all)""", "No font is listed: the page is a single image. There are no pieces of text to regroup.",
          "SCANNED: route 2 or 3", TEAL_D, GREY1)]
for i, (name, thumb, out, reading, verdict, col, fill) in enumerate(cases):
    x = 0.41 + i * 6.42
    card(s, x, 1.50, 6.08, 4.55, fill, alpha=40 if i == 0 else 100)
    txt(s, name, x + 0.25, 1.62, 5.6, 0.30, MONO, 11, NAVY, bold=True)
    s.shapes.add_picture(os.path.join(FIG, thumb), Inches(x + 0.25), Inches(2.05), Inches(1.62), Inches(2.29))
    code(s, out, x + 2.05, 2.05, 3.80, 1.55, 8.5)
    rich(s, [reading], x + 2.05, 3.72, 3.80, 0.75, size=11.5)
    pill(s, verdict, x + 0.25, 4.62, w=2.60, color=col, size=10, h=0.38)
    txt(s, "a page rendered as it looks" if i == 0 else "the same kind of page, but scanned",
        x + 0.25, 5.12, 5.6, 0.28, HNL, 10.5, GREY_TXT, italic=True)
banner(s, "The same test in Python:",
       "page.extract_text() returns 1062 characters for the annex and an empty string for the certificate.",
       x=0.41, y=6.25, w=12.5, h=0.50, fill=NAVY2, size=12.5)
d.notes(s, "The bridge between the previous slide and the choice of route. Rule-based extraction regroups "
           "pieces of text; if a page holds no text at all, only a picture of it, there is nothing to "
           "regroup, and the work passes to OCR or to an assistant. The two thumbnails look alike to a "
           "reader; the command tells them apart immediately. The outputs are genuine, from the two "
           "documents of Lab 2.1, and students run the same check in the first cell of the lab.")

# ===================================================================== 9
s = d.slide("The table that spans pages")
sub(s, "The failure that nobody sees: the usual case in an annex, and the hardest error to detect")
s.shapes.add_picture(os.path.join(FIG, "pdf_split_table.png"), Inches(0.41), Inches(1.50), Inches(6.60), Inches(3.03))
steps = [("Extract page 2 only", "42 rows", "It appears complete: correct columns, correct types, a plausible plot. Nothing looks wrong.", TEAL_D),
         ("Add page 3", "42 + 22 = 64", "The header is printed again at the top of page 3 and enters the table as if it were a test.", TEAL_D),
         ("Remove the repeated header", "63 rows", "Which is exactly what section 1 of the annex declares: sixty-three SPT tests.", PURPLE)]
for i, (t, n, b, col) in enumerate(steps):
    y = 1.50 + i * 1.05
    card(s, 7.30, y, 5.62, 0.95, LILAC if i == 2 else GREY1, alpha=40 if i == 2 else 100)
    badge(s, i + 1, 7.52, y + 0.25, col)
    txt(s, t, 8.12, y + 0.08, 3.1, 0.30, HN, 13, NAVY, bold=True)
    txt(s, n, 11.10, y + 0.08, 1.65, 0.30, MONO, 12.5, col, bold=True, align=PP_ALIGN.RIGHT)
    rich(s, [b], 8.12, y + 0.40, 4.65, 0.52, size=11)
card(s, 0.41, 4.75, 12.5, 1.25, NAVY, alpha=100)
txt(s, "Why it is so hard to detect", 0.70, 4.86, 11.9, 0.30, HN, 13.5, TEAL, bold=True)
txt(s, "Nothing in step 1 appears wrong. The only thing that reveals the error is comparing the row count with a statement in the document itself. "
       "Had the annex not stated how many tests there were, there would be no way of knowing short of counting by hand.",
    0.70, 5.20, 11.9, 0.75, HNL, 12, "CFD8DC", spacing=1.12)
banner(s, "Rule:", "before extracting a table, find the sentence in the text that states how many rows it should have.",
       x=0.41, y=6.20, w=12.5, h=0.50, fill=NAVY2, size=13)
d.notes(s, "The figure is the real annex. Top: the end of page 2, where the table appears to finish after "
           "42 tests. Bottom: the top of page 3, where it continues and the header is printed again, framed "
           "in purple. Concatenating the two pages gives 64 rows, one of which is the repeated header; "
           "removing it leaves 63, the number the annex states. This is exercise 3 of Lab 2.1: let students "
           "discover that 42 is not 63 before saying it. Extension A extracts the 63 from the text with a "
           "regular expression, which is what one does with a hundred annexes.")

# ===================================================================== 10
s = d.slide("Validation with checks")
sub(s, "Concrete checks for an extracted table, written as assertions; the last one applies wherever a total is printed")
rows = [["Check", "How it is written", "What it catches"],
        ["Row count against the text", "len(spt) == 63", "Split table, dropped rows, omitted pages"],
        ["Number of declared units", "spt.borehole.nunique() == 6", "An entire borehole page that was not extracted"],
        ["Internal monotonicity", "groupby.depth_m.is_monotonic_increasing", "Shifted columns, disordered rows"],
        ["Physical range", "n_spt.between(0, 100)", "A lost decimal comma, a wrong column"],
        ["Coherence between columns", "density between 1.0 and 2.5 g/cm3", "Mixed units, a forgotten scale factor"],
        ["Published control figure", "sum == printed total", "Any of the above, at one stroke"]]
table(s, rows, 0.41, 1.50, 12.5, [3.4, 4.9, 4.2], rowh=0.54, size=12, mono_cols=(1,), mono_size=10, bold_col=0)
card(s, 0.41, 5.45, 12.5, 1.10, LILAC)
s.shapes.add_picture(os.path.join(FIG, "spt_perfil.png"), Inches(0.55), Inches(5.52), Inches(1.20), Inches(0.96))
txt(s, "And a seventh, the cheapest of all: plot it", 1.95, 5.55, 10.5, 0.30, HN, 13.5, PURPLE, bold=True)
rich(s, ["A wrongly extracted value almost always appears as a point outside the cloud. Three lines of matplotlib catch what no assertion anticipated, because one need not know in advance what to look for."],
     1.95, 5.88, 10.7, 0.62, size=12)
cite(s, "The thumbnail is the real output of exercise 5 of Lab 2.1.")
d.notes(s, "These six are the asserts of exercise 5. The seventh, plotting, is the one that will save them "
           "most often and the one least taught.")

# ===================================================================== 11
s = d.section("LAB 2.1", "The annex and the certificate",
              "Twenty-five minutes, in pairs. Seven exercises and three extensions.")
lab1 = [("Locate", "which pages hold the SPT table"), ("Extract", "raw lists from both pages"),
        ("Reconstruct", "one table, no repeated header; 63?"), ("Type", "decimal comma to numbers, units in the names"),
        ("Validate", "five assertions and a plot"), ("Assistant", "certificate, CSV, verification, log"),
        ("Provenance", "four columns; saved to Parquet")]
for i, (t, b) in enumerate(lab1):
    x = 0.90 + (i % 4) * 3.10
    y = 4.85 + (i // 4) * 1.0
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.37), Inches(0.37))
    _fill(sh, "9B7BFF" if i == 5 else TEAL); _noline(sh)
    txt(s, str(i + 1), x, y, 0.37, 0.37, HN, 11, WHITE if i == 5 else NAVY, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, t, x + 0.50, y - 0.02, 2.5, 0.30, HN, 13, WHITE, bold=True)
    txt(s, b, x + 0.50, y + 0.28, 2.55, 0.45, HNL, 9.5, "9AA3B2")
txt(s, "Finished when every check prints passed, the log has five non-empty lines and LOG_COMPLETE is True. "
       "Extensions: the control figure by regular expression; OCR with confidence; a datalogger series.",
    0.90, 6.75, 11.8, 0.45, HNL, 10.5, "8E96AB", italic=True)
d.notes(s, "Circulate during exercise 3 (the split table) and exercise 6 (the assistant). For exercise 6 "
           "students may use any assistant, phone included; the solution notebook pastes the ground "
           "truth so it runs end to end, and says so. Debrief at the end: who found a discrepancy, and "
           "with which check? Frame the breakages as the format working as designed, not as their failure.")

# ===================================================================== 12
s = d.slide("Checkpoint before the break")
sub(s, "To be answered in the last cell of Lab 2.1")
cps = ["Extracting only the first page yielded 42 records and nothing appeared wrong. Name three checks that would have detected it without reading the annex text.",
       "The assistant returned a clean twelve-row table. Which of the five log lines can be completed automatically, and which two require a human reader?",
       "A colleague sends the extracted table as CSV without provenance columns. Name two things that can no longer be done with it."]
for i, q in enumerate(cps):
    y = 1.55 + i * 1.50
    card(s, 0.41, y, 12.5, 1.32, LILAC if i % 2 == 0 else GREY1, alpha=40 if i % 2 == 0 else 100)
    badge(s, i + 1, 0.75, y + 0.44, acc(i))
    rich(s, [q], 1.45, y + 0.22, 11.0, 0.95, size=14, anchor=MSO_ANCHOR.MIDDLE)
banner(s, "Five-minute break.", "Run the installation cell of Lab 2.2 before leaving your seat.",
       x=3.20, y=6.20, w=6.95, h=0.48, fill=NAVY2, size=12.5)
d.notes(s, "Expected: (1) count boreholes and see S-6 missing; max depth against the report; more than one "
           "page with a table. (2) source, tool and date, counts and units can be automated; totals and "
           "spot checks need a person. (3) go back to the original to check a doubtful value; know whether "
           "the extraction predates a revision of the annex.")

# ===================================================================== 13
s = d.section("BLOCK 2, NO TEXT AT ALL", "OCR and AI assistants",
              "The scanned page has no text layer. There are two ways in, and neither raises an error when it is wrong.",
              ["tesseract", "confidence", "the log", "ask for the source"])
d.notes(s, "Ten minutes, four slides.")

# ===================================================================== 14
s = d.slide("Route 2. OCR fails silently")
sub(s, "Actual Tesseract output on today's certificate, at 300 dpi, greyscale, Spanish language data")
code(s, """Probeta  Fabricacion  Rotura      Edad  Carga(kN)  Resistencia(MPa)
P-01     12/03/2025   19/03/2025  d     374,7      21,2
P-02     12/03/2025   19/03/2025  7     438,7      24,8
P-03     12/03/2025   19/03/2025  ñ     444,3      20.)
P-04     12/03/2025   19/03/2025  ra    363,9      20,6
P-05     12/03/2025   09/04/2025  28    601,6      34,0
...
Tipificacion del hormigon: HA-30/B/20/lla""", 0.41, 1.50, 7.30, 2.95, 10.5)
rows = [["In the document", "OCR returned", "What happened", "Range check?"],
        ["Age: 7", "d, ñ, ra", "an isolated digit without context becomes a letter", "yes: not a number"],
        ["Strength: 25,1", "20.)", "the decimal comma became a point and a digit was lost", "yes: NaN on conversion"],
        ["HA-30/B/20/IIa", "lla", "capital I read as lower-case l", "no: still text"],
        ["Load: 438,7", "438,7", "grouped digits with numeric context are read correctly", "not needed"]]
table(s, rows, 7.95, 1.50, 4.97, [1.30, 1.00, 1.72, 0.95], rowh=0.56, size=9.5, mono_cols=(1,), mono_size=9, bold_col=0)
card(s, 0.41, 4.62, 6.08, 1.55, GREY1, alpha=100)
txt(s, "Confidence is not correctness", 0.70, 4.75, 5.6, 0.32, HN, 14, TEAL_D, bold=True)
rich(s, ["139 words recognised, mean confidence 92.7, seven words below 80, three cells wrong. A high confidence means that the engine is sure, not that the value is right."],
     0.70, 5.10, 5.6, 1.0, size=12)
card(s, 6.83, 4.62, 6.09, 1.55, LILAC)
txt(s, "A pipeline, not a function", 7.12, 4.75, 5.6, 0.32, HN, 14, PURPLE, bold=True)
rich(s, ["Rasterise at 300 dpi, convert to greyscale, recognise with the Spanish model, post-process. Omitting the greyscale step turned this same page into the string ESMERADA A OO PECAR 00 PECES."],
     7.12, 5.10, 5.6, 1.0, size=12)
banner(s, "In an inspection archive, a misread load rating is a structural safety problem.",
       "Every digit that matters is checked, by eye or by rule.",
       x=0.41, y=6.32, w=12.5, h=0.50, fill=NAVY2, size=13)
d.notes(s, "The output and the three errors are literally what Tesseract returned on the lab certificate. "
           "The nonsense string is also literal: it is what came back before converting to greyscale while "
           "preparing this material. OCR is extension B of Lab 2.1; shown here as a demonstration to save lab time.")

# ===================================================================== 15
s = d.slide("Route 3. AI assistants fail convincingly")
sub(s, "Now standard practice for one-off extraction. Professional use is distinguished by the protocol, not by the tool")
card(s, 0.41, 1.50, 6.08, 4.45, GREY1, alpha=100)
txt(s, "Where they are useful", 0.70, 1.66, 5.6, 0.36, HN, 16, TEAL_D, bold=True)
rich(s, ["Layouts that defeat rules: spanning headers, footnote markers inside values, merged cells.",
         "Skewed or low-contrast scans, where OCR confidence collapses.",
         "Semi-structured text: extracting dates, codes and quantities from paragraphs.",
         "A first pass over hundreds of heterogeneous documents to locate the pages that matter."],
     0.70, 2.15, 5.6, 3.6, size=12.5, space_after=9)
card(s, 6.83, 1.50, 6.09, 4.45, LILAC)
txt(s, "What does not change", 7.12, 1.66, 5.6, 0.36, HN, 16, PURPLE, bold=True)
rich(s, ["They produce wrong values with the same fluency as right ones; the table appears complete and consistent precisely where it is wrong.",
         "Request the page and position of every value, then check a sample of cells by hand and state how many were checked.",
         "The same page may be extracted differently twice. Keep the raw output and the prompt.",
         "A client's annex is not sent to an external service without written permission."],
     7.12, 2.15, 5.6, 3.6, size=12.5, space_after=9)
banner(s, "Each route fails in its own way:", "rules visibly, OCR silently, assistants convincingly. The verification is the same for all three.",
       x=0.41, y=6.15, w=12.5, h=0.52, fill=NAVY2, size=13)
d.notes(s, "One slide, no sermon. Presenting assistants as forbidden makes half the class stop verifying "
           "because they use them anyway. Presenting them as a route with a protocol is what an office does. "
           "Confidentiality is what new graduates forget most.")

# ===================================================================== 16
s = d.slide("The verification log: five lines")
sub(s, "Required whenever data extracted by an assistant enters an analysis. The log is part of the deliverable")
log = [("Source", "document, page, and edition or date of the original"),
       ("Tool and date", "which assistant or library, its version, and when"),
       ("Totals", "recomputed and compared with the printed ones; the result"),
       ("Spot checks", "three cells chosen at random, compared with the page by eye; the result"),
       ("Counts and units", "rows, columns and units; any discrepancy noted")]
for i, (t, b) in enumerate(log):
    y = 1.52 + i * 0.88
    card(s, 0.41, y, 8.10, 0.78, LILAC if i % 2 == 0 else GREY1, alpha=40 if i % 2 == 0 else 100)
    badge(s, i + 1, 0.70, y + 0.17, acc(i))
    txt(s, t, 1.36, y + 0.20, 2.4, 0.36, HN, 15, NAVY, bold=True)
    rich(s, [b], 3.85, y + 0.22, 4.5, 0.45, size=12.5)
card(s, 8.80, 1.52, 4.12, 4.30, NAVY, alpha=100)
txt(s, "The decision rule", 9.08, 1.70, 3.6, 0.32, HN, 14, TEAL, bold=True)
rule = [("Rules", "recurring, auditable, batch work: five hundred weekly bulletins, a pipeline that runs unattended"),
        ("Assistant with the log", "a one-off document with a hostile layout: a table to be extracted exactly once"),
        ("Before either", "ask whether the source spreadsheet still exists")]
for i, (t, b) in enumerate(rule):
    y = 2.15 + i * 1.15
    txt(s, t, 9.08, y, 3.6, 0.30, HN, 13, WHITE, bold=True)
    txt(s, b, 9.08, y + 0.30, 3.6, 0.75, HNL, 11, "CFD8DC", spacing=1.1)
banner(s, "Exercise 6 of Lab 2.1 writes this log.", "Lines 1, 2 and 5 can be automated; lines 3 and 4 require a person.",
       x=0.41, y=6.05, w=12.5, h=0.52, fill=NAVY2, size=13)
d.notes(s, "Read the five lines slowly. Then the decision rule on the right, in that order: rules for "
           "recurring work, assistants with the log for one-off chaos, and before either, ask for the source.")

# ===================================================================== 17
s = d.section("BLOCK 3, THE RESERVOIR", "A web page claims, an image checks",
              "The basin authority publishes the water surface of the reservoir in a web bulletin.\nA satellite image measures the same surface by a completely independent route.",
              ["read_html", "control figure", "reflectance", "NDWI", "hectares"])
d.notes(s, "Twelve minutes, four slides, and one question: how much water is in the reservoir? The block has "
           "two halves. First the claim, read from a web table. Then the check, derived from an image. Both "
           "are read by rules, route 1 of the map, and both can fail silently.")

# ===================================================================== 17a
s = d.slide("The claim: a table on a web page")
sub(s, "pandas.read_html walks the page and returns a list with every table it finds")
code(s, """<table class="datos">
 <thead>
  <tr><th rowspan="2">Embalse</th>
      <th colspan="2">Reserva</th>
      <th rowspan="2">Superficie (ha)</th></tr>
  <tr><th>Capacidad (hm3)</th>
      <th>Llenado (%)</th></tr>
 </thead>
 <tbody>
  <tr><td>Presa de la Hoz<sup>[1]</sup></td>
      <td>96,4</td><td>63,5</td><td>307,1</td></tr>
  ...
  <tr class="total"><td>Total cuenca</td>
      <td>930,4</td><td></td><td></td></tr>
 </tbody>
</table>""", 0.41, 1.50, 6.05, 4.10, 10)
feats = [("rowspan and colspan", "a header of two levels", 'header=[0, 1]'),
         ("<sup>[1]</sup>", "a footnote marker attached to the name", "str.replace"),
         ('class="total"', "a summary row, set aside: it is the control figure", "recompute it"),
         ("930,4 and 96,4", "thousands point and decimal comma, as in session 1", 'thousands, decimal')]
for i, (tag, what, fix) in enumerate(feats):
    y = 1.50 + i * 0.86
    card(s, 6.83, y, 6.09, 0.76, LILAC if i == 2 else GREY1, alpha=40 if i == 2 else 100)
    badge(s, i + 1, 7.06, y + 0.16, acc(i))
    txt(s, tag, 7.66, y + 0.08, 2.7, 0.28, MONO, 10.5, PURPLE if i == 2 else NAVY, bold=True)
    txt(s, fix, 10.35, y + 0.09, 2.42, 0.28, MONO, 9, GREY_TXT, align=PP_ALIGN.RIGHT)
    rich(s, [what], 7.66, y + 0.40, 5.1, 0.34, size=11)
card(s, 6.83, 5.00, 6.09, 0.60, NAVY, alpha=100)
txt(s, "The bulletin claims:  Presa de la Hoz,  307.1 ha", 7.06, 5.00, 5.7, 0.60, HN, 13.5, WHITE, bold=True, anchor=MSO_ANCHOR.MIDDLE)
banner(s, "Validate before trusting:", "the page prints its own total, 930.4 hm3; recompute it from the extracted rows.",
       x=0.41, y=5.85, w=12.5, h=0.50, fill=NAVY2, size=12.5)
d.notes(s, "Show the HTML and the numbered points side by side: each feature of the page explains one "
           "argument of read_html. The page contains two tables, hence the list and the match argument. The "
           "totals row is both a trap, because it enters any sum as if it were a reservoir, and the best "
           "control figure available. The dark box states the number the rest of the block will check. If a "
           "table is built from div elements, read_html sees nothing: that is BeautifulSoup, next week.")

# ===================================================================== 17b
s = d.slide("The check: from pixels to hectares")
sub(s, "A satellite scene is the field model of session 1, one grid per band. Four steps turn it into a surface")
s.shapes.add_picture(os.path.join(FIG, "pipeline_pixels_to_hectares.png"), Inches(0.41), Inches(1.45), Inches(12.5), Inches(3.60))
steps = [("Read reflectance", "digital numbers converted with the offset in the metadata"),
         ("Compute NDWI", "(green - NIR) / (green + NIR): water positive, land negative"),
         ("Threshold and mask", "choose the cut-off, remove clouds and shadows"),
         ("Count and convert", "water pixels x 400 m2, divided by 10 000")]
for i, (t, b) in enumerate(steps):
    x = 0.41 + i * 3.16
    card(s, x, 5.18, 3.00, 0.98, LILAC if i == 0 else GREY1, alpha=40 if i == 0 else 100)
    badge(s, i + 1, x + 0.20, 5.36, acc(i), d=0.40)
    txt(s, t, x + 0.72, 5.26, 2.2, 0.30, HN, 12.5, NAVY, bold=True)
    rich(s, [b], x + 0.72, 5.56, 2.2, 0.58, size=10)
banner(s, "Every step is a rule, and step 1 can fail without any warning.", "The next two slides take the two decisions that matter.",
       x=0.41, y=6.35, w=12.5, h=0.46, fill=NAVY2, size=12)
d.notes(s, "The key slide of the block, and the one that was missing: the whole chain in one picture, "
           "before any detail. The scene is a stack of grids, exactly the raster of session 1; the only new "
           "thing is that the values are reflectance encoded as integers. Walk the four panels left to right "
           "and land on the number: 307.1 hectares. Only then open steps 1 and 3 in the next two slides. "
           "Lab 2.2 follows exactly this order.")

# ===================================================================== 18
s = d.slide("Step 1: reading the numbers correctly")
sub(s, "Sentinel-2 stores reflectance as integers; the conversion is written in the product metadata, not in the code")
facts = [("Open data", "Copernicus Data Space Ecosystem, free account. A monitoring resource for dams, coasts and sites at no cost."),
         ("Four bands today", "B02 blue, B03 green, B04 red, B08 near infrared. The SCL band classifies each pixel: water, vegetation, cloud, shadow."),
         ("Today's clip", "300 by 300 pixels at 20 m around one reservoir, on two dates: August 2023 and April 2025.")]
for i, (t, b) in enumerate(facts):
    x = 0.41 + i * 4.22
    card(s, x, 1.50, 4.05, 1.62, GREY1, alpha=100)
    badge(s, i + 1, x + 0.22, 1.64, acc(i), d=0.40)
    txt(s, t, x + 0.76, 1.68, 3.1, 0.32, HN, 13.5, NAVY, bold=True)
    rich(s, [b], x + 0.22, 2.12, 3.6, 0.95, size=11)
card(s, 0.41, 3.28, 12.5, 1.18, NAVY, alpha=100)
txt(s, "reflectance = ( DN + BOA_ADD_OFFSET ) / QUANTIFICATION_VALUE", 0.70, 3.40, 9.0, 0.40, MONO, 14.5, WHITE, bold=True)
txt(s, "Both values are read from the metadata file. Since processing baseline 04.00 (January 2022) the offset is minus 1000; dividing by 10 000 alone is no longer correct.",
    0.70, 3.86, 11.9, 0.55, HNL, 11.5, "CFD8DC", spacing=1.1)
s.shapes.add_picture(os.path.join(FIG, "desplazamiento_radiometrico.png"), Inches(0.41), Inches(4.62), Inches(6.30), Inches(1.97))
card(s, 6.95, 4.62, 5.97, 1.97, LILAC)
txt(s, "What happens if the offset is ignored", 7.20, 4.74, 5.5, 0.30, HN, 13, PURPLE, bold=True)
rich(s, ["Water reflects 0.118 in the near infrared instead of 0.018, as brightly as bare soil. With the literature threshold of 0.3, the detected surface falls from 305 hectares to none. No error is raised: the reservoir simply disappears."],
     7.20, 5.08, 5.5, 1.45, size=11.5)
d.notes(s, "Exercise 4 of Lab 2.2. This is the silent failure of the image route, the counterpart of the lost "
           "decimal comma in OCR. Honest nuance, worth saying: with a threshold derived from the histogram "
           "the sign of the index is preserved and the result would have been nearly right; the offset is "
           "critical for absolute values and fixed thresholds.")

# ===================================================================== 19
s = d.slide("Steps 2 and 3: index and threshold")
sub(s, "Water absorbs near-infrared light and land reflects it; a normalised difference turns that contrast into a number")
code(s, "ndwi = (green - nir) / (green + nir)   # -1 to 1", 0.41, 1.50, 6.05, 0.56, 11.5)
idx = [("NDWI", "(Green - NIR) / (Green + NIR)", "open water; McFeeters (1996). The index used today.", True),
       ("NDVI", "(NIR - Red) / (NIR + Red)", "vegetation; Rouse et al. (1974).", False),
       ("NDWI (Gao)", "(NIR - SWIR) / (NIR + SWIR)", "water in leaves; Gao (1996). A different index with the same name.", False)]
for i, (n, f, u, hot) in enumerate(idx):
    y = 2.20 + i * 0.92
    card(s, 0.41, y, 6.05, 0.82, LILAC if hot else GREY1, alpha=40 if hot else 100)
    txt(s, n, 0.64, y + 0.08, 1.8, 0.32, NOHEMI, 14, PURPLE if hot else NAVY, bold=True)
    txt(s, f, 2.45, y + 0.11, 3.9, 0.28, MONO, 9.5, NAVY, bold=True)
    rich(s, [u], 0.64, y + 0.44, 5.7, 0.34, size=10.5, color=GREY_TXT)
s.shapes.add_picture(os.path.join(FIG, "ndwi_histograma.png"), Inches(6.83), Inches(1.50), Inches(6.09), Inches(2.58))
opts = [("Zero", "convenient and arbitrary; cannot be defended in a report", "9AA3B2"),
        ("0.3, from the literature", "defensible with a citation, but foreign to this image", "9AA3B2"),
        ("Otsu (1979): minus 0.110", "derived from this histogram; reproducible", PURPLE)]
for i, (t, b, col) in enumerate(opts):
    y = 4.18 + i * 0.52
    pill(s, t, 6.83, y + 0.05, w=2.55, color=col, size=9.5, h=0.34)
    txt(s, b, 9.50, y + 0.08, 3.4, 0.34, HNL, 11, NAVY)
banner(s, "Mask clouds and shadows (SCL 3, 8, 9) before thresholding,", "otherwise they move the threshold.",
       x=0.41, y=5.95, w=12.5, h=0.52, fill=NAVY2, size=12.5)
d.notes(s, "Exercises 6 and 7 of Lab 2.2. Left: the index, and the warning that two different indices share "
           "the name NDWI. Right: the histogram is bimodal, a large peak for land and a small one for water, "
           "and Otsu finds the valley between them. A histogram that is not bimodal still yields a number, "
           "and that number means nothing, so the histogram must always be inspected first.")

# ===================================================================== 21
s = d.section("LAB 2.2", "The web table, then the reservoir",
              "Twenty-eight minutes; roles swap. Eight exercises and two extensions.")
lab2 = [("Locate the table", "read_html returns two; select with match"), ("Clean", "flatten the header, set the total aside, remove [1]"),
        ("Control figure", "recompute the total and compare with the printed one"), ("Reflectance", "read the metadata; apply the equation"),
        ("Composites", "guided: true and false colour"), ("Indices", "NDVI and NDWI; check the signs"),
        ("Threshold and surface", "Otsu, SCL mask, two dates, hectares"), ("The two sources", "image against bulletin; relative difference")]
for i, (t, b) in enumerate(lab2):
    x = 0.90 + (i % 4) * 3.10
    y = 4.85 + (i // 4) * 1.0
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.37), Inches(0.37))
    _fill(sh, TEAL if i < 3 else "9B7BFF"); _noline(sh)
    txt(s, str(i + 1), x, y, 0.37, 0.37, HN, 11, NAVY if i < 3 else WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, t, x + 0.50, y - 0.02, 2.55, 0.30, HN, 13, WHITE, bold=True)
    txt(s, b, x + 0.50, y + 0.28, 2.55, 0.45, HNL, 9.5, "9AA3B2")
txt(s, "Predict before exercise 4: does ignoring the offset make water appear darker or brighter in the near infrared? "
       "Finished when exercise 8 prints the relative difference and you can name three hypotheses for a discrepancy of 40 per cent.",
    0.90, 6.75, 11.8, 0.45, HNL, 10.5, "8E96AB", italic=True)
d.notes(s, "Exercises 1-3 are the HTML part, eight minutes. Exercise 5 is guided to save time. Exercise 8 "
           "closes the session: two independent routes to the same number. Extension A (both mistakes at "
           "once) is the one that impresses; mention it even if there is no time.")

# ===================================================================== 22
s = d.slide("Two routes, one number")
sub(s, "A web table and a satellite image, with nothing in common but the object they measure")
s.shapes.add_picture(os.path.join(FIG, "mascaras_agua.png"), Inches(0.41), Inches(1.50), Inches(6.60), Inches(3.23))
vals = [("Hydrological bulletin", "307.1 ha", "web table published by the basin authority, April 2025", False),
        ("Sentinel-2 image", "307.1 ha", "NDWI thresholded with Otsu, clouds masked, same date", False),
        ("Discrepancy", "below 1 %", "the two sources confirm each other", True)]
for i, (t, v, b, hot) in enumerate(vals):
    y = 1.50 + i * 1.10
    card(s, 7.30, y, 5.62, 1.0, LILAC if hot else GREY1, alpha=40 if hot else 100)
    txt(s, t, 7.55, y + 0.12, 3.2, 0.30, HN, 13, PURPLE if hot else TEAL_D, bold=True)
    txt(s, v, 10.60, y + 0.08, 2.1, 0.42, NOHEMI, 19, PURPLE if hot else NAVY, bold=True, align=PP_ALIGN.RIGHT)
    rich(s, [b], 7.55, y + 0.48, 5.1, 0.45, size=11, color=GREY_TXT)
card(s, 7.30, 4.85, 5.62, 1.65, NAVY, alpha=100)
txt(s, "Had they not agreed", 7.55, 4.97, 5.1, 0.30, HN, 13, TEAL, bold=True)
txt(s, "Three hypotheses, cheapest first: the dates differ; the bulletin measures the basin while the image includes neighbouring ponds; cloud shadow has been classified as water.",
    7.55, 5.30, 5.1, 1.1, HNL, 11.5, "CFD8DC", spacing=1.1)
rich(s, [[("The image adds what the bulletin cannot: a second date. August 2023, in drought, 134.8 ha; April 2025, full, 307.1 ha. A 56 per cent loss of water surface between the two.", True)]],
     0.41, 4.85, 6.6, 0.75, size=12)
rich(s, ["Agreement between independent sources is stronger evidence than either source alone. This is data fusion in the sense of the module's title, and the subject of sessions 13 and 14."],
     0.41, 5.70, 6.6, 0.85, size=11.5, color=GREY_TXT)
cite(s, "Figures computed on the Lab 2.2 data.", y=6.7)
d.notes(s, "Ask two pairs for their number before showing this slide. If one differs a lot, they almost "
           "certainly did not mask clouds or did not apply the offset; diagnosing it live is worth more than the slide.")

# ===================================================================== 23
s = d.slide("Back to the map: four routes")
sub(s, "Each one fails in its own way; the verification is the same for all")
rows = [["Route", "Fails", "When", "Use it for", "Verified by"],
        ["Rules", "visibly", "the layout breaks its assumptions", "recurring, auditable, batch work", "recount, ranges, plot"],
        ["OCR", "silently", "image quality confuses the recognition", "scanned pages, every digit checked", "confidence, ranges, eye"],
        ["AI assistants", "convincingly", "the model fills gaps plausibly", "one-off documents with hostile layouts", "the five-line log"],
        ["Ask for the source", "it cannot", "not applicable", "before any of the above", "the table is never transcribed"]]
fills = lambda i, j: (LILAC if i == 3 else (GREY1 if i % 2 else WHITE))
table(s, rows, 0.41, 1.50, 12.5, [2.2, 1.6, 3.3, 3.0, 2.4], rowh=0.72, size=12, bold_col=0, hot_col=1, row_fills=fills)
banner(s, "From last week's project folder, the file with an .xls extension that was really HTML now opens.",
       "The IFC model is next week's; the point cloud remains in the appendix.",
       x=0.41, y=5.30, w=12.5, h=0.52, fill=NAVY2, size=13)
d.notes(s, "Same table as slide 6, closed. Point at the last row: the route professionals forget.")

# ===================================================================== 24
s = d.slide("Synthesis")
sub(s, "Six statements to retain for next week")
syn = ["A PDF stores pieces of text at coordinates; the table is rebuilt, and may be rebuilt wrongly.",
       "An extraction error does not present itself as a failure but as a plausible result: 42 rows instead of 63.",
       "Validation is made against the document's own statements: counts, ranges, printed totals.",
       "Rules fail visibly, OCR silently, assistants convincingly; the protocol is the same for all three.",
       "Metadata state how the numbers are to be read. A single ignored offset can make a reservoir disappear.",
       "Two independent sources that agree are worth more than either alone. When they disagree, the work begins."]
for i, t in enumerate(syn):
    x = 0.41 + (i % 2) * 6.42
    y = 1.55 + (i // 2) * 1.62
    card(s, x, y, 6.08, 1.45, LILAC if i % 2 == 0 else GREY1, alpha=40 if i % 2 == 0 else 100)
    badge(s, i + 1, x + 0.28, y + 0.30, acc(i))
    txt(s, t, x + 0.92, y + 0.26, 5.0, 1.0, HN, 13.5, NAVY, bold=True, spacing=1.10)
d.notes(s, "Read them slowly.")

# ===================================================================== 25
s = d.slide("Homework")
sub(s, "Two minutes, done in the room: next Friday's session does not work without the key")
card(s, 0.41, 1.50, 7.60, 3.15, LILAC)
txt(s, "Request your AEMET OpenData API key", 0.72, 1.70, 7.0, 0.40, HN, 18, PURPLE, bold=True)
rich(s, ["At opendata.aemet.es, choose Obtención de API Key, enter your e-mail address, and the key arrives by mail. Keep that message.",
         "Session 3 begins by calling that API. The confirmation message sometimes takes a day to arrive."],
     0.72, 2.25, 7.0, 2.2, size=13.5, space_after=10)
card(s, 8.32, 1.50, 4.60, 3.15, GREY1, alpha=100)
txt(s, "Still open", 8.62, 1.70, 4.0, 0.36, HN, 16, TEAL_D, bold=True)
rich(s, ["The format card from session 1, due before session 4: half a page on a dataset you will actually use.",
         "Optional: bring a PDF from any engineering context that you would like to extract; one of them will be examined in class."],
     8.62, 2.15, 4.0, 2.4, size=12, space_after=9)
card(s, 0.41, 4.90, 12.5, 1.55, NAVY, alpha=100)
txt(s, "Session 3, Friday 2 October", 0.72, 5.05, 6, 0.32, HN, 15, TEAL, bold=True)
txt(s, "Data acquisition: live APIs (AEMET, datos.madrid.es), requests, JSON as it arrives, BeautifulSoup for the pages that read_html cannot see, and the rules that govern it: headers, rate limits, robots.txt and terms of use.",
    0.72, 5.42, 11.9, 0.95, HNL, 13, "CFD8DC", spacing=1.12)
d.notes(s, "Have them request the key in the room, now, with the phone. The mail can take a day.")

# ===================================================================== 26
s = d.section("THREE MINUTES BEFORE LEAVING", "Exit ticket",
              "Anonymous. Three short answers, read before Friday.")
for i, q in enumerate(["One thing you learned today.",
                       "One thing that is still unclear.",
                       "An assistant returns an impeccable forty-row table from a scanned annex. Write the first three lines of your verification log."]):
    y = 4.75 + i * 0.75
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.90), Inches(y), Inches(0.36), Inches(0.36))
    _fill(sh, TEAL if i < 2 else "9B7BFF"); _noline(sh)
    txt(s, str(i + 1), 0.90, y, 0.36, 0.36, HN, 11, NAVY if i < 2 else WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, q, 1.50, y + 0.01, 10.8, 0.40, HN if i == 2 else HNL, 13.5, WHITE, bold=(i == 2), spacing=1.05)
d.notes(s, "Question 3 has a right answer: source (document, page, edition), tool and date, and totals "
           "recomputed against the printed ones. Read all answers to 1 and 2 before Friday.")

# ===================================================================== 27
s = d.slide("References")
sub(s, "The first three are the recommended readings for the topic")
refs = [("Lau, Gonzalez and Nolan (2023)", "Learning Data Science, chapters 9 and 13. Open access at learningds.org", True),
        ("ESA", "Sentinel-2 MSI Level-2A Processing Overview; radiometric offset from baseline 04.00", True),
        ("McFeeters (1996)", "The use of the NDWI in the delineation of open water features. International Journal of Remote Sensing, 17(7)", True),
        ("Gao (1996)", "NDWI for remote sensing of vegetation liquid water from space. Remote Sensing of Environment, 58(3)", False),
        ("Rouse et al. (1974)", "Monitoring vegetation systems in the Great Plains with ERTS. NASA SP-351", False),
        ("Otsu (1979)", "A threshold selection method from gray-level histograms. IEEE Transactions on Systems, Man, and Cybernetics, 9(1)", False),
        ("Rule et al. (2019)", "Ten simple rules for writing and sharing computational analyses in Jupyter Notebooks. PLOS Computational Biology, 15(7)", False),
        ("Wickham (2014)", "Tidy Data. Journal of Statistical Software, 59(10)", False)]
for i, (a, b, rec) in enumerate(refs):
    y = 1.50 + i * 0.64
    if rec:
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.41), Inches(y), Inches(0.08), Inches(0.50))
        _fill(bar, PURPLE); _noline(bar)
    txt(s, a, 0.70, y + 0.04, 3.6, 0.34, HN, 12.5, NAVY if rec else GREY_TXT, bold=True)
    rich(s, [b], 4.45, y + 0.04, 8.45, 0.50, size=12, color=NAVY if rec else GREY_TXT)
txt(s, "Courses consulted in the design of the session: CMU 15-388, UC Berkeley Data 100, MIT 6.S079 and UIUC CEE 492.",
    0.41, 6.70, 12.5, 0.28, HNL, 10, GREY_TXT, italic=True)
d.notes(s, "The first three are the pre-reading for next time's satellite work and this session's PDF work.")

# ===================================================================== APPENDIX
s = d.section("APPENDIX", "Reference material",
              "Not projected. Part of the handout, and a reserve if time allows.")

s = d.slide("A.1. Which tool for which source")
sub(s, "A decision table for unstructured sources, to keep after the session")
rows = [["Source", "Start with", "First move", "Then validate with"],
        ["Native PDF, ruled table", "pdfplumber", "page.extract_tables()", "row count against the text, ranges"],
        ["Native PDF, unruled table", "camelot stream", "column positions given by hand", "the same, plus a visual check"],
        ["Native PDF, running text", "pdfplumber or PyMuPDF", "extract_text(), regular expressions", "spot-check ten matches"],
        ["Scanned PDF, clean, few pages", "pytesseract", "300 dpi, lang=spa, image_to_data", "confidence and ranges"],
        ["Scanned PDF, skewed or long", "assistant with the log, or manual", "budget it, document it", "sample 5 % of the cells"],
        ["HTML with a real table element", "pd.read_html", "match, header, decimal", "the page's own totals"],
        ["HTML built from div elements", "BeautifulSoup (session 3)", "inspect the page structure", "count against visible rows"],
        ["Satellite scene", "rasterio and numpy", "metadata, clip, mask clouds", "an independent source or gauge"],
        ["Drone or site photographs", "PIL, exifread", "EXIF: time, GPS, camera", "match to the site log"]]
table(s, rows, 0.41, 1.50, 12.5, [3.2, 3.0, 3.3, 3.0], rowh=0.50, size=11, mono_cols=(1, 2), mono_size=9.5,
      bold_col=0, hot_col=1)
d.notes(s, "Reference slide from the first version of the session. It goes into the one-page cheat sheet, "
           "together with that of session 1.")

s = d.slide("A.2. Cleaning a web table")
sub(s, "Seven problems present in almost every web table, and the pandas line for each")
rows = [["Symptom", "Fix"],
        ["Two or three header rows, MultiIndex columns", "header=[0, 1], then flatten the column names"],
        ["Footnote markers attached to text: Valmayor[3]", 'col.str.replace(r"\\[\\d+\\]", "", regex=True)'],
        ["Spanish number formatting: 1.104,0", 'thousands=".", decimal=","'],
        ["Units attached to numbers: 425,3 hm3", 'col.str.extract(r"([\\d.,]+)"), then to_numeric'],
        ["Total or footer rows mixed with the data", 'df[~df[col].str.contains("Total", na=False)]'],
        ["Merged cells repeated down the column", "usually desired; otherwise drop_duplicates on the key"],
        ["Numbers read as text", 'pd.to_numeric(col, errors="coerce"), then count the new NaN']]
table(s, rows, 0.41, 1.50, 12.5, [5.4, 7.1], rowh=0.56, size=12, mono_cols=(1,), mono_size=10, bold_col=0)
banner(s, "The same idea as with the PDF:", "the page usually prints its own total. Recompute it, then store the URL and the download date next to the data.",
       x=0.41, y=6.20, w=12.5, h=0.52, fill=NAVY2, size=12.5)
d.notes(s, "Reference slide from the first version of the session; complements the web-table slide of block 3.")

s = d.slide("A.3. Tools for native PDFs")
sub(s, "Begin with pdfplumber; turn to the others when it fails")
tools = [("pdfplumber", "Words and characters with bounding boxes; extract_tables() from drawn lines; page.crop(). Pure Python. The default.", "pip install pdfplumber", True),
         ("PyMuPDF (fitz)", "Fastest text extraction; pulls embedded images; renders pages for OCR. Less table logic.", "pip install pymupdf", False),
         ("camelot", "Two modes: lattice (ruled tables) and stream (whitespace-aligned). Accuracy score per table. Needs Ghostscript.", "pip install camelot-py", False),
         ("tabula-py", "Wrapper over the Java Tabula engine. Good on clean ruled tables; needs a JVM.", "pip install tabula-py", False)]
for i, (t, b, inst, hot) in enumerate(tools):
    x = 0.41 + (i % 2) * 6.42
    y = 1.50 + (i // 2) * 2.35
    card(s, x, y, 6.08, 2.15, LILAC if hot else GREY1, alpha=40 if hot else 100)
    txt(s, t, x + 0.28, y + 0.20, 3.5, 0.40, MONO, 16, PURPLE if hot else NAVY, bold=True)
    txt(s, inst, x + 0.28, y + 1.75, 5.5, 0.28, MONO, 9.5, GREY_TXT)
    rich(s, [b], x + 0.28, y + 0.72, 5.55, 1.0, size=12)
banner(s, "Rule of thumb:", "pdfplumber first. If a ruled table is split badly, camelot in lattice mode. If there are no ruling lines, camelot in stream mode with column positions given by hand.",
       x=0.41, y=6.20, w=12.5, h=0.52, fill=NAVY2, size=12.5)

s = d.slide("A.4. How pdfplumber finds a table")
sub(s, "Two strategies, depending on what the generating program drew")
card(s, 0.41, 1.50, 6.08, 4.30, GREY1, alpha=100)
txt(s, "With ruling lines (lattice)", 0.70, 1.66, 5.5, 0.36, HN, 16, TEAL_D, bold=True)
rich(s, ["Finds horizontal and vertical segments, intersects them, takes each closed cell as a table cell."], 0.70, 2.10, 5.5, 0.7, size=12.5)
for r in range(4):
    for c in range(4):
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.10 + c * 1.15), Inches(3.05 + r * 0.36), Inches(1.15), Inches(0.36))
        _fill(sh, MID if r == 0 else WHITE); _line(sh, "6B7683", 0.75)
txt(s, "robust; fails when vertical lines are missing", 0.70, 4.70, 5.5, 0.3, HNL, 11.5, GREY_TXT, italic=True)
txt(s, "page.extract_tables()", 0.70, 5.10, 5.5, 0.3, MONO, 10.5, PURPLE)
card(s, 6.83, 1.50, 6.09, 4.30, LILAC)
txt(s, "By alignment (stream)", 7.12, 1.66, 5.5, 0.36, HN, 16, PURPLE, bold=True)
rich(s, ["With no lines to follow, words are grouped by x coordinate and columns are inferred from vertical gaps of whitespace."], 7.12, 2.10, 5.5, 0.7, size=12.5)
for r in range(4):
    for c, (cx, w) in enumerate([(7.55, 1.0), (8.85, 0.95), (10.15, 0.85), (11.35, 0.9)]):
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx), Inches(3.10 + r * 0.36), Inches(w * (0.55 + 0.12 * ((r + c) % 3))), Inches(0.20))
        _fill(sh, "9AA3B2" if r == 0 else MID); _noline(sh)
txt(s, "fragile; one wide cell shifts the whole column", 7.12, 4.70, 5.5, 0.3, HNL, 11.5, GREY_TXT, italic=True)
txt(s, 'camelot.read_pdf(flavor="stream")', 7.12, 5.10, 5.5, 0.3, MONO, 10.5, PURPLE)
banner(s, "Today's annex is ruled, so pdfplumber resolves it.", "Laboratory certificates and tender documents usually are not.",
       x=0.41, y=6.05, w=12.5, h=0.50, fill=NAVY2, size=12.5)

s = d.slide("A.5. Documents you will extract from")
sub(s, "Throughout a career, each with its characteristic pathology")
docs = [("Geology and geotechnics annex", "borehole logs, SPT, lab tests", "native, table split across pages"),
        ("Concrete test certificates", "strength at 7 and 28 days, batch, date", "scanned, one per batch, hundreds per site"),
        ("Bridge inspection reports", "damage codes, element ratings, photos", "native forms with free text"),
        ("Tender documents", "deadlines, scoring criteria, price tables", "native, hundreds of pages"),
        ("Hydrological yearbooks and bulletins", "reservoir volumes, flows by station and day", "PDF and HTML, format changes across years"),
        ("Official gazettes", "expropriation lists, approvals, dates", "native, dense text, implicit structure")]
for i, (t, b, p) in enumerate(docs):
    x = 0.41 + (i % 3) * 4.22
    y = 1.50 + (i // 3) * 2.35
    card(s, x, y, 4.05, 2.15, LILAC if i == 0 else GREY1, alpha=40 if i == 0 else 100)
    badge(s, i + 1, x + 0.25, y + 0.22, acc(i))
    txt(s, t, x + 0.85, y + 0.22, 3.1, 0.65, HN, 13.5, NAVY, bold=True, spacing=1.05)
    rich(s, [b], x + 0.25, y + 1.00, 3.55, 0.55, size=11.5)
    txt(s, p, x + 0.25, y + 1.62, 3.55, 0.45, HNL, 10.5, PURPLE if i == 0 else GREY_TXT, italic=True, spacing=1.05)

s = d.slide("A.6. Sentinel-2 bands")
sub(s, "Which band answers which question")
rows = [["Band", "Name", "Resolution", "Used for"],
        ["B02, B03, B04", "blue, green, red", "10 m", "true colour; NDWI uses green"],
        ["B08", "near infrared", "10 m", "NDVI, NDWI, false colour"],
        ["B05-B07, B8A", "red edge", "20 m", "vegetation condition"],
        ["B11, B12", "short-wave infrared", "20 m", "built-up areas, soil moisture, burnt areas"],
        ["B01, B09, B10", "aerosol, water vapour, cirrus", "60 m", "atmospheric correction"],
        ["SCL", "scene classification", "20 m", "cloud, shadow, water, snow masks (L2A only)"]]
table(s, rows, 0.41, 1.50, 12.5, [2.4, 3.3, 1.6, 5.2], rowh=0.58, size=12, bold_col=0)
txt(s, "Level-2A products contain surface reflectance: a SAFE folder with one JPEG 2000 file per band, in 100 km tiles named like T30TVK. Alternatives: Landsat 8 and 9 (30 m, a thermal band, a series since the 1970s), PNOA orthophotos (25 to 50 cm), and drones.",
    0.41, 5.75, 12.5, 0.7, HNL, 12, GREY_TXT, spacing=1.1)

s = d.slide("A.7. Sources of documents and imagery")
sub(s, "Sources for the module and for the final project")
src = [("Copernicus Data Space", "Sentinel-1 and 2, levels 1C and 2A, the full catalogue with a free account", "SAFE, JP2"),
       ("CNIG download centre", "PNOA orthophotos, LiDAR, terrain models, base cartography", "TIF, LAZ"),
       ("Landsat, USGS EarthExplorer", "a series since the 1970s, with a thermal band", "TIF"),
       ("Basin authority bulletins", "reservoir storage by week, in PDF and HTML", "PDF, HTML"),
       ("Public information portals", "full projects in public consultation, annexes included", "PDF"),
       ("Official gazettes", "expropriations, approvals and deadlines, with a query API", "PDF, XML")]
for i, (t, b, f) in enumerate(src):
    x = 0.41 + (i % 3) * 4.22
    y = 1.50 + (i // 3) * 2.1
    card(s, x, y, 4.05, 1.9, LILAC if i % 4 == 0 else GREY1, alpha=40 if i % 4 == 0 else 100)
    txt(s, t, x + 0.25, y + 0.18, 3.55, 0.6, HN, 13.5, NAVY, bold=True, spacing=1.05)
    rich(s, [b], x + 0.25, y + 0.85, 3.55, 0.65, size=11, color=GREY_TXT)
    pill(s, f, x + 0.25, y + 1.48, w=1.7, color="9AA3B2", size=8.5)
banner(s, "Published does not mean redistributable.", "Projects in public consultation have a deadline and a purpose; Copernicus data are open but require attribution.",
       x=0.41, y=5.90, w=12.5, h=0.52, fill=NAVY2, size=12.5)

d.save(os.path.join(BASE, "Session2_Unstructured_data_FINAL.pptx"))
print("slides:", len(d.prs.slides))
