
from pathlib import Path
from fasthtml.common import Div, NotStr
from pilot.html.components.combined import CombinedComponent

cwd = Path(__file__).resolve().parent
html = cwd / 'index.html'


class PageLayout(CombinedComponent):

    headers = True
    footers = True
    children = [

        # Fasthtml elements go here

        ]

    if html.is_file():
        qmd_div = Div(NotStr(html.read_text()))
        children.append(qmd_div)

layout = PageLayout()

