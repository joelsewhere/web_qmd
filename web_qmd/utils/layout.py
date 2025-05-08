from fasthtml.common import *
from pathlib import Path
from web_qmd.components.combined_component import CombinedComponent

def load_html(path, headers=[], footers=[]):

    if isinstance(path, str):
        path = Path(path).resolve()


    class PageLayout(CombinedComponent):

        children = []

        if path.is_file():
            
            qmd_div = Div(NotStr(path.read_text()))
            children.append(qmd_div)

    PageLayout.children = headers + PageLayout.children + footers

    
    return PageLayout()()