# Module 2 — Data Fusion, Preparation and Visualization applied to Civil Engineering

Teaching material for Module 2 of the ACS-UPM Diploma in Engineering, Data Science and
Artificial Intelligence. ETSI Caminos, Canales y Puertos, Universidad Politécnica de Madrid.

- **Session 1 — From file to structure:** data models in civil engineering.
- **Session 2 — Extraction and validation:** getting data out of PDFs, web tables and satellite
  imagery, and checking it against an independent source.

## Contents

```
.
|-- Session1_Data_models.pptx          slide deck (48 slides: 34 projected + 14 appendix)
|-- template.pptx                      the ACS-UPM template the deck is built on
|-- calendario.pptx                    the course-structure slide this deck's slide 2 follows
|-- Syllabus_Mod2_planifac.xlsx        the module calendar slide 2 summarises
|-- tpl_media/                         logos and cover background extracted from the template
|-- notebooks/                         student versions, pushed to GitHub
|   |-- Lab_1_1_reading_files.ipynb
|   |-- Lab_1_2_object_and_field.ipynb
|   |-- Lab_2_1_extraction_and_validation.ipynb
|   '-- Lab_2_2_web_table_and_satellite.ipynb
|-- master/                            SOURCE notebooks, with the answers; never pushed
|   '-- one per lab, same file names as notebooks/
|-- solutions/                         instructor versions built from master/, never pushed
|   '-- one per lab, with the _SOLUTION suffix
|-- data/                              datasets for both sessions (generated)
|-- figuras/                           deck figures generated from the data
|-- scripts/
|   |-- make_data.py                   generates data/ and prints the expected assert values
|   |-- build_labs.py                  builds notebooks/ and solutions/ from master/
|   |-- make_figures.py                generates figuras/ from data/
|   |-- tpl.py                         component library that reproduces the template
|   |-- build_tpl.py                   builds the deck from those components
|   |-- build_calendar_slide.py        builds slide 2 on its own, as a one-slide file
|   '-- s02/                           the same tooling for session 2
|-- SOURCES.md                         provenance, licence and date of the session 1 data
|-- SOURCES_session2.md                the same for session 2
|-- DEPLOY.md                          how to publish the labs to Colab, with a diagram
|-- PUSH.md                            the four commands to push this folder to GitHub
|-- .gitignore                         keeps master/ and solutions/ out of the public repository
'-- notebooks/                         student notebooks, pushed
```

## Getting started

```bash
pip install pandas numpy matplotlib openpyxl pyarrow geopandas rasterio scipy laspy
python scripts/make_data.py --comprobar     # writes data/ and prints the expected values
python scripts/build_labs.py
python scripts/make_figures.py
jupyter lab notebooks/
```

In Google Colab, the first cell of each notebook clones the repository and defines `DATA`.
Data are preloaded: nothing is downloaded in class.

## How the notebooks are edited

Each lab has **one** source: its notebook in `master/`. You edit that one, in Jupyter or in Colab,
like any other notebook. Answers go inside the nbgrader marker pair:

```python
### BEGIN SOLUTION
result = frame.groupby(key).mean()      # an illustration, not a real answer
### END SOLUTION
```

`python scripts/build_labs.py` then writes two versions of every master notebook: the one in
`notebooks/`, where each block above becomes `# YOUR CODE HERE` and `raise NotImplementedError`
with the indentation preserved, and the one in `solutions/`, where only the marker lines are
removed. Outputs are stripped from both, so no execution result is ever published.

`master/` and `solutions/` are in `.gitignore`. **Keep it that way**: anything pushed is public,
including a script that happens to contain the answers.

Do not edit `notebooks/` or `solutions/` directly. They are overwritten on every rebuild.

## Verification before teaching

Both solution versions must run end to end without errors. Every `assert` depends on the concrete
values of the dataset, so **if the synthetic data are replaced by real downloads, the expected
values must be recomputed**:

```bash
python scripts/make_data.py --comprobar
cd notebooks && python - <<'EOF'
import nbformat
from nbclient import NotebookClient
for f in ["../solutions/Lab_1_1_reading_files_SOLUTION.ipynb",
          "../solutions/Lab_1_2_object_and_field_SOLUTION.ipynb"]:
    nb = nbformat.read(f, as_version=4)
    NotebookClient(nb, timeout=400, resources={"metadata": {"path": "."}}).execute()
    print("OK", f)
EOF
```

Lab 1.2 consumes `top10.parquet`, produced by exercise 6 of Lab 1.1. Run them in order.
When that file is missing, Lab 1.2 falls back to `data/top10_reference.parquet`, so it also
runs on its own. That reference is written by `master/make_top10_reference.py`, which
executes the Lab 1.1 solution notebook and keeps its output, so there is no second copy
of the pipeline to drift. **If you replace the synthetic data with real downloads, run it
again**, or Lab 1.2 will silently answer the question of the session with the old points.
It is the one `.parquet` exempted from `.gitignore`, because students need it.

## The deck and the template

The deck is generated, not hand-drawn. `scripts/tpl.py` opens `template.pptx`, keeps its master,
theme, fonts and logos, removes the example slides and exposes the template's own component
vocabulary: cover, titled slide, dark section divider, numbered circle, rounded card, code block,
pill, banner and table. `scripts/build_tpl.py` writes the 48 slides with those components.

Every measurement comes from the template: title at x=0.41 y=0.27 in Nohemi 28 pt bold #23263B,
footer at y=7.06 in Helvetica 9 pt #6B7683, logo at x=9.92 y=0.21 w=3.10 h=0.69, cards as rounded
rectangles with adj=4368 at 40 % alpha, numbered badges as 0.45 in circles in #964BFF or #42DEDC,
code blocks in #23263B with Courier New #E8EDF2.

```bash
python scripts/build_tpl.py            # rewrites Session1_Data_models.pptx
python scripts/build_calendar_slide.py # writes Structure_of_the_module.pptx, one slide
```

To restyle the whole deck, replace `template.pptx` and re-extract `tpl_media/`; the slides follow.

## Slide 2: the module calendar

Slide 2 summarises `Syllabus_Mod2_planifac.xlsx` following the layout of `calendario.pptx`: a strip
of twenty-four numbered sessions with the five taught by Antía Fernández in purple, and a horizontal
timeline of the six blocks with **every session listed by name and date**.

| Block | Sessions | Dates | Hours |
|---|---|---|---|
| 1. Structured and unstructured data | 1-3 | 18 Sep – 2 Oct 2026 | 6 |
| 2. Data quality and wrangling | 4-12 | 21 Sep – 6 Nov 2026 | 18 |
| 3. Data integration | 13-14 | 10 – 13 Nov 2026 | 4 |
| 4. Feature preparation | 15-18 | 16 – 27 Nov 2026 | 8 |
| 5. Data visualization | 19-20 | 4 – 11 Dec 2026 | 4 |
| Capstone mini-projects | 21-24 | Dec 2026 – Jan 2027 | 8 |

The session names on the slide are shortened from the spreadsheet's content column so that they fit
the columns; the full wording stays in the spreadsheet. They live in one editable list at the top of
`scripts/build_calendar_slide.py`, which also writes the slide as a standalone one-slide file.

**Note on the dates.** In the spreadsheet blocks 1 and 2 overlap: block 1 runs on Fridays from
18 September while block 2 starts on 21 September, so the first fortnight has two sessions a week.
Sessions 21 to 24 carry no date; the December-January range on the slide is an assumption and should
be confirmed before teaching. The spreadsheet also has a typo in the instructor of session 9
("Carlos Garía Gutiérrez").

## Publishing the labs

Start with `PUSH.md`: four commands. Then see `DEPLOY.md` and the diagram in `figuras/colab_setup.png`. In short: push the folder to a public
GitHub repository and hand out a `colab.research.google.com/github/...` link, or upload it to Drive
and have students add a shortcut to My Drive. The first cell of each notebook detects which of the
three situations it is in and sets `BASE`, `DATA` and `WORK` accordingly, so students never edit a
path. `scripts/prepare_repo.py` sets `REPO` in the master notebooks for you; set `DRIVE` there by hand
if you move the Drive folder.

## Language

Slides, notebooks and this README are in English, the language of the diploma. Column names in
the data files (`fecha`, `intensidad`, `vmed`…) are Spanish because the sources are Spanish public
portals, and are kept as they arrive; variables and new columns are in English.

## About the data

The files in `data/` are synthetic. They reproduce the structure, encoding and defects of the real
public data (`;` separator, decimal comma, `latin-1`, `dd/mm/yyyy` dates, sentinel values,
duplicates from retransmissions, shapefile field-name truncation, no-data area in the terrain
model, an `.xls` that is actually HTML, a `.dat` that is logger text) but the values correspond to
no real measurement and the municipalities are invented.

Before teaching, replace them with real downloads from datos.madrid.es and the CNIG download
centre, and recompute the asserts. Until then the material is self-contained and runs offline.

## Duration and structure

Two hours. One hundred and ten minutes including the break, ten of slack. The schedule counts the
opening and the close. Laptops open at minute seven.

| Block | Minutes | Mode | Slides |
|---|---|---|---|
| 0. Opening and Exercise 0 | 17 | mixed | 1-7 |
| 1. The map | 8 | lecture | 8-11 |
| 2. Tabular data | 12 | lecture | 12-18 |
| Lab 1.1 | 26 | pair practice | 19-20 |
| Break | 5 | | |
| 3. Spatial data | 12 | lecture | 21-27 |
| Lab 1.2 | 22 | pair practice | 28 |
| 4. Close and exit ticket | 8 | lecture | 29-34 |

The deck follows a pyramid: slide 9 states the thesis (three levels), slide 10 is the map of seven
data models with the session in which each is covered, and blocks 2 and 3 descend into today's
three rows with the same internal order (model, format, pitfalls, lab). Slide 30 returns to the map
with today's rows ticked.

**Only the first 34 slides are projected.** From 35 on there are fourteen appendix slides.

### Working rules (slide 5)

Predict before you run; pairs with roles that swap at the break; errors are debugged on the
projector; AI assistants allowed on condition of being able to explain every line.

### Lab breakdown

| Lab 1.1 (10 + 26 min) | Lab 1.2 (22 min) |
|---|---|
| 0. The project folder (opening) · 10 min | 1. Break the shapefile · 4 min |
| 1. The naive read · 4 min | 2. Areas in degrees and metres · 5 min |
| 2. The correct read · 7 min | 3. Geographic table and CRS mismatch · 5 min |
| 3. Granularity · 4 min | 4. Open the surface *(guided)* · 2 min |
| 4. Sentinel values · 4 min | 5. The question of the session · 5 min |
| 5. CSV vs Parquet *(on the projector)* · 3 min | 6. Zonal statistics *(if time allows)* |
| 6. The question of the session · 6 min | |
| A, B, C: Excel, hourly profile, provenance | A, B: GeoPackage, surface to table |

Exercise 0 runs at the start of the session, before the theory, with twelve files of the project
folder of which two lie about their extension. Exercise 5 of Lab 1.1 resolves the vote of slide 16
(2, 10 or 50 times smaller?) and shows the 30-row counterexample. Exercise 3 of Lab 1.2 builds the
points without a CRS on purpose so that the mismatch is seen before it is fixed.

### Exit ticket (slide 32)

Three minutes, anonymous: one thing learned, one thing unclear, one transfer question. Needs a form
in the repository or paper. Read before session 2.

## Reference values of the dataset

| Quantity | Value |
|---|---|
| Rows in the traffic CSV | 21,568, of which 40 duplicated; 21,528 unique |
| Sentinels (-1) in `vmed` | 2,339 |
| Mean speed bias from sentinels | 58.4 → 65.7 km/h |
| CSV vs Parquet, 21,568 rows | 0.97 MB → 0.13 MB, 7.4× smaller; ≈7× faster to read |
| CSV vs Parquet, 30 rows | 1,515 B → 4,611 B, Parquet 3× larger |
| Files in Exercise 0 | 12; two lie about their extension |
| Municipalities | 9, EPSG:25830 (shapefile) and EPSG:4326 (GeoJSON) |
| Terrain model | 800 × 800 cells, 25 m, no-data −32768 |

## Readings

Required before the session: Lau, Gonzalez and Nolan (2023), sections 8.2 and 8.3, open access at
learningds.org. Ten minutes.

Recommended: Rey, Arribas-Bel and Wolf (2023), chapters 3 and 5, at geographicdata.science;
Wickham, H. (2014), *Tidy Data*, Journal of Statistical Software 59(10).

## Licence

Teaching material. Generated data are synthetic and free to use. The deck cites its sources on
slide 34.

<!-- COLAB -->
## Open the labs in Colab

- [Lab_1_1_reading_files.ipynb](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_1_reading_files.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_1_reading_files.ipynb)
- [Lab_1_2_object_and_field.ipynb](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_2_object_and_field.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_1_2_object_and_field.ipynb)
- [Lab_2_1_extraction_and_validation.ipynb](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_2_1_extraction_and_validation.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_2_1_extraction_and_validation.ipynb)
- [Lab_2_2_web_table_and_satellite.ipynb](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_2_2_web_table_and_satellite.ipynb)  [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/antiafer/acs-upm-mod2-s01/blob/main/notebooks/Lab_2_2_web_table_and_satellite.ipynb)
<!-- /COLAB -->
