import re
from pathlib import Path
# import plotly.express as px
import plotly.graph_objects as go
import typer
from collections import defaultdict

from .tei import read_tei, find_elements, get_siglum

app = typer.Typer()


@app.command()
def plot_verses(
    paths:list[Path], 
    verse_list:Path=typer.Option(...),
):
    tei_list = [read_tei(path) for path in paths]
    verse_list = Path(verse_list).read_text().strip().splitlines()
    data = []
    for tei_index, tei in enumerate(tei_list):
        rubrics = find_elements(tei, ".//div[@type='rubric']")
        for rubric in rubrics:
            verse = rubric.attrib.get("corresp", "")
            if verse:
                if verse.endswith("b"):
                    verse = verse[:-1]
                verse_index = verse_list.index(verse)
                data.append( (tei_index, verse_index) )
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[x[1] for x in data],
            y=[x[0] for x in data],
            mode='markers',
            marker=dict(size=10, color='blue'),
        )
    )
    fig.show()


@app.command()
def by_verse(
    paths:list[Path], 
    verse_list:Path=typer.Option(...),
):
    tei_list = [read_tei(path) for path in paths]
    verse_list = Path(verse_list).read_text().strip().splitlines()
    data = defaultdict(dict)
    for tei_index, tei in enumerate(tei_list):
        siglum = get_siglum(tei)
        rubrics = find_elements(tei, ".//div[@type='rubric']")
        for rubric in rubrics:
            verse = rubric.attrib.get("corresp", "")
            data[verse][siglum] = rubric
    
    def sort_verse(verse):
        verse_str = re.sub(r"b$", "", verse)
        return verse_list.index(verse_str) if verse_str in verse_list else -1

    verses = sorted(data.keys(), key=sort_verse)
    for verse in verses:
        print(verse, data[verse].keys())
