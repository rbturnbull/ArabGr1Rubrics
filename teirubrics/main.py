from pathlib import Path
import typer

from .tei import read_tei, find_elements

app = typer.Typer()


@app.command()
def plot_veres(tei:Path, verse_list:Path):
    tei = read_tei(tei)
    rubrics = find_elements(tei, ".//div[@type='rubric']")
    verse_list = Path(verse_list).read_text().strip().splitlines()
    for rubric in rubrics:
        verse = rubric.attrib.get("corresp", "")
        if verse:
            if verse.endswith("b"):
                verse = verse[:-1]
            verse_index = verse_list.index(verse)
            print(verse, verse_index)
