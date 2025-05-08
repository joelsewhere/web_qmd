import sh
import shutil
import pandoc
from pathlib import Path
from bs4 import BeautifulSoup

log = lambda x: '\033[1m\033[38;5;214m' + x + '\033[0m'

init_string = f"""
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

"""

routes_string = """
from web_qmd.app import qmd_sub_app

app, rt = qmd_sub_app(__file__)
"""

def format_ojs(read_pandoc):
    """
    Iterate over every pandoc block and search for codeblocks
    that contain the string "{ojs}".

    When found convert to a RawBlock and place the contect of the block
    inside <script></script>
    """
    for block, path in pandoc.iter(read_pandoc, path=True):
        if isinstance(block, pandoc.types.CodeBlock):
            block_classes = block[0]
            for bc in block_classes:
                if isinstance(bc, list) and '{ojs}' in bc:
                    holder, index = path[-1]
                    holder[index] = pandoc.types.RawBlock(
                        pandoc.types.Format('html'),
                        '<script>' + block[-1] + '</script>'
                        )
                
def convert_fasthtml(json):
    meta, top_level_nodes = list(json)

    for idx, node in enumerate(top_level_nodes):
        for child in pandoc.iter(node):
            if isinstance(child, pandoc.types.CodeBlock):
                if child[0][1] and child[0][1][0] == 'html':
                    rawblock = pandoc.types.RawBlock(pandoc.types.Format('html'), child[1])
                    top_level_nodes[idx] = rawblock

    doc = pandoc.types.Pandoc(meta, top_level_nodes)

    return doc


def qmd_json(filepath, transform_ojs=True, extract_media=Path.cwd()):
    rendered_json = sh.quarto('render', filepath, to='json', output='-', **{"extract-media": extract_media})
    read_pandoc = pandoc.read(rendered_json, format='json')
    read_pandoc = convert_fasthtml(read_pandoc)
    if transform_ojs:
        format_ojs(read_pandoc)

    return read_pandoc

def scrub_pandas_styling(html):

    soup = BeautifulSoup(html, features="lxml")

    styles = soup.find_all('style')
    for style in styles:
        if '.dataframe' in style.text:
            style.decompose()

    tables = soup.find_all('table', {"class": 'dataframe'})
    for table in tables:
        trs = table.find_all('tr')
        for tr in trs:
            if 'style' in tr.attrs:
                del tr['style']

    return str(soup)

def project_files(directory, logger, replace=False, index=False):

    if not directory.is_dir():
        directory.mkdir(parents=True, exist_ok=True)

    if index:
        (directory / 'index.qmd').open('w').write('')

    layout = directory / 'layout.py'
    if (not layout.is_file()) or replace:

        logger.info(log(f'Writing template {layout.as_posix()}'))
        layout.open('w').write(init_string)

    routes = directory / 'routes.py'
    if (not routes.is_file()) or replace:

        logger.info(log(f'Writing template {routes.as_posix()}'))
        routes.open('w').write(routes_string)

def render(path, root, logger, init=False, replace=False, ensure_layout=False):
    path = Path(path).resolve()
    root = Path(root).resolve()

    logger.info(log(f'quarto render {path.as_posix()}'))
    print('\n\n', path.as_posix())
    json = qmd_json(path, extract_media=path.parent/'static')
    json_string = pandoc.write(json, format='json')
    json_string = json_string.replace(root.as_posix(), '')
    json_scrubbed = pandoc.read(json_string, format='json')
    html = pandoc.write(json_scrubbed, format='html')
    html_scrubbed = scrub_pandas_styling(html)
    html_path = (path.parent / 'index.html')
    html_path.open('w').write(html_scrubbed)

    logger.info(log(f'{html_path.as_posix()} regenerated'))

    if init or replace:
        project_files(path.parent, replace=replace)
            
    index_files = path.parent / 'index_files'
    if index_files.is_dir():
        shutil.rmtree(index_files.as_posix())



