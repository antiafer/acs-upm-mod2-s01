"""Builds the module-calendar slide, with all twenty-four sessions listed.

    python scripts/build_calendar_slide.py [output.pptx]

Session names and dates come from Syllabus_Mod2_planifac.xlsx, shortened for the slide.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tpl import (Deck, txt, session_strip, timeline_sessions,  # noqa: E402
                 HNL, GREY_TXT)

OURS = {1, 2, 3, 19, 20}

BLOCKS = [
    {"kicker": "Block 1 · S1-S3", "title": "Structured and\nunstructured data",
     "date": "18 Sep – 2 Oct", "meta": "3 sessions · 6 h",
     "sessions": [
         (1, "Data formats and models", "18 Sep", True),
         (2, "Unstructured data: PDF, HTML", "25 Sep", True),
         (3, "APIs and web scraping", "2 Oct", True),
     ]},
    {"kicker": "Block 2 · S4-S12", "title": "Data quality\nand wrangling",
     "date": "21 Sep – 6 Nov", "meta": "9 sessions · 18 h",
     "sessions": [
         (4, "Descriptive statistics, DQ report", "21 Sep", False),
         (5, "Application to dataset", "28 Sep", False),
         (6, "Missing values and outliers", "5 Oct", False),
         (7, "Application to dataset", "9 Oct", False),
         (8, "Survey data: Likert scales", "16 Oct", False),
         (9, "Advanced pandas: merge and join", "23 Oct", False),
         (10, "Application to dataset", "26 Oct", False),
         (11, "Geospatial wrangling, choropleths", "30 Oct", False),
         (12, "Application to dataset", "6 Nov", False),
     ]},
    {"kicker": "Block 3 · S13-S14", "title": "Data integration",
     "date": "10 – 13 Nov", "meta": "2 sessions · 4 h",
     "sessions": [
         (13, "Structure, granularity, relations", "10 Nov", False),
         (14, "Referential integrity", "13 Nov", False),
     ]},
    {"kicker": "Block 4 · S15-S18", "title": "Feature\npreparation",
     "date": "16 – 27 Nov", "meta": "4 sessions · 8 h",
     "sessions": [
         (15, "Normalisation, scaling, encoding", "16 Nov", False),
         (16, "Feature selection", "20 Nov", False),
         (17, "PCA: scree plot, loadings, biplot", "23 Nov", False),
         (18, "Clustering as exploratory analysis", "27 Nov", False),
     ]},
    {"kicker": "Block 5 · S19-S20", "title": "Data\nvisualization",
     "date": "4 – 11 Dec", "meta": "2 sessions · 4 h",
     "sessions": [
         (19, "Visualization design principles", "4 Dec", True),
         (20, "Interactive visualization, Plotly", "11 Dec", True),
     ]},
    {"kicker": "Capstone · S21-S24", "title": "Mini-projects",
     "date": "Dec 2026 – Jan 2027", "meta": "4 sessions · 8 h",
     "sessions": [
         (21, "Group supervision", "", False),
         (22, "Independent work", "", False),
         (23, "Independent work", "", False),
         (24, "Oral presentations", "", False),
     ]},
]

NOTES = (
    "One minute, no more. Point at the strip: the five purple sessions are the ones I teach; today "
    "is the first. Then point at block 2, which is nine of the twenty-four: most of this module is "
    "data quality and wrangling, and that proportion is itself the message.\n\n"
    "Two caveats taken from the spreadsheet. Blocks 1 and 2 overlap: block 1 runs on Fridays from "
    "18 September while block 2 starts on 21 September, so the first fortnight has two sessions a "
    "week. And sessions 21 to 24 carry no date, so the December-January range is an assumption to "
    "be confirmed.\n\n"
    "The session names are shortened from the syllabus content column; the full wording is in "
    "Syllabus_Mod2_planifac.xlsx."
)


def build(path="Structure_of_the_module.pptx"):
    d = Deck()
    s = d.slide("Structure of the module")
    txt(s, "Twenty-four sessions, forty-eight contact hours, six blocks",
        0.41, 1.02, 12.0, 0.30, HNL, 14.5, GREY_TXT)
    session_strip(s, 24, highlight=OURS, y=1.38, h=0.30)
    txt(s, "In purple, the five sessions taught by Antía Fernández. Today is the first.",
        0.41, 1.73, 9.0, 0.22, HNL, 10.5, GREY_TXT, italic=True)
    timeline_sessions(s, BLOCKS, marker=0)
    d.notes(s, NOTES)
    return d.save(path)


if __name__ == "__main__":
    print(build(sys.argv[1] if len(sys.argv) > 1 else "Structure_of_the_module.pptx"))
