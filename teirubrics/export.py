from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from .tei import find_element, extract_text


def export_data(data, key_name, sigla, output_path:Path, display_verse=True):
    templates = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(templates))
    rubric_template = env.get_template('rubric.html')

    rows = []
    for key in data:
        row = [key]
        for siglum in sigla:
            if siglum in data[key]:
                element = data[key][siglum]
                head = find_element(element, ".//head")
                orig = find_element(head, ".//orig")
                original_text = extract_text(orig)
                translation_element = find_element(head, ".//reg[@type='translation']")
                translation = extract_text(translation_element) if translation_element is not None else ""

                cell = rubric_template.render(
                    original_text=original_text,
                    translation=translation,
                    verse = element.attrib.get("corresp", "") if display_verse else "",
                )
            else:
                cell = ""
            row.append(cell)
        rows.append(row)

    table = env.get_template('table.html').render(
        rows=rows,
        headers=[key_name] + sigla,
    )
    print("Exporting to", output_path)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        f.write(table)    