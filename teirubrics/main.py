import re
from pathlib import Path
# import plotly.express as px
import plotly.graph_objects as go
import typer
from collections import defaultdict

from .export import export_data
from .tei import read_tei, find_elements, get_siglum, find_element, extract_text


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
def by_date(
    paths:list[Path], 
):
    tei_list = [read_tei(path) for path in paths]
    data = defaultdict(dict)
    sigla = [get_siglum(tei) for tei in tei_list]
    for tei in tei_list:
        siglum = get_siglum(tei)
        rubrics = find_elements(tei, ".//div[@type='rubric']")
        for rubric in rubrics:
            date_elements = find_elements(rubric, ".//date")
            for date_element in date_elements:
                date_id = date_element.attrib['when-custom']
                if date_id.startswith("#"):
                    date_id = date_id[:]
                data[date_id][siglum] = rubric

                if date_id not in data:
                    data[date_id] = {}
    
    calendar = tei.find('.//taxonomy[@xml:id="calendar"]', namespaces={'xml': 'http://www.w3.org/XML/1998/namespace'})
    date_definitions = find_elements(calendar, ".//category")
    date_dict = dict()
    for date_element in date_definitions:
        date_id = date_element.attrib['{http://www.w3.org/XML/1998/namespace}id']
        cat_description = find_element(date_element, ".//catDesc")
        date_name = extract_text(cat_description) or date_id
        date_dict[date_id] = date_name

    date_rank = { date_id:index for index, date_id in enumerate(date_dict) }
    
    def sort_by_date(item):
        date = item[0]
        return date_rank[date] if date in date_rank else -1

    data = dict(sorted(data.items(), key=sort_by_date))
    export_data(
        data=data,
        key_name="Date",
        sigla=sigla,
        output_path=Path("dates.html"),
    )    


@app.command()
def by_verse(
    paths:list[Path], 
    verse_list:Path=typer.Option(...),
):
    verse_list = Path(verse_list).read_text().strip().splitlines()
    data = defaultdict(dict)

    tei_list = [read_tei(path) for path in paths]
    sigla = [get_siglum(tei) for tei in tei_list]
    for tei in tei_list:
        siglum = get_siglum(tei)
        rubrics = find_elements(tei, ".//div[@type='rubric']")
        for rubric in rubrics:
            verse = rubric.attrib.get("corresp", "")
            data[verse][siglum] = rubric
    
    def sort_by_verse(item):
        verse = item[0]
        verse_str = re.sub(r"b$", "", verse)
        return verse_list.index(verse_str) if verse_str in verse_list else -1

    data = dict(sorted(data.items(), key=sort_by_verse))
    export_data(
        data=data,
        key_name="Verse",
        sigla=sigla,
        output_path=Path("output.html"),
    )