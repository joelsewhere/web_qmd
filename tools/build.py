from qmd_convert import qmd_json
import pandoc
import shutil
import sys
from pathlib import Path
from argparse import ArgumentParser
from bs4 import BeautifulSoup


def scrub_pandas_styling(html):

    soup = BeautifulSoup(html)

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


cli = ArgumentParser()
cli.add_argument('-replace', action="store_true")
args = cli.parse_args()

root = Path(__file__).resolve().parents[2]
creations = root / 'creations'
ignore_directories = ['index_files', 'static']
directories = [x for x in creations.rglob('*') if (x.is_dir() and x.stem not in ignore_directories)]

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

def drop_pandas_styling(json):
    for block, path in pandoc.iter(json, path=True):

        if (
            isinstance(block, pandoc.types.RawBlock) 
            and '<style' in block[1]
            and '.dataframe' in block[1]
            ):

            holder, index = path[-1]
            holder[index] =  pandoc.types.RawBlock(
                        pandoc.types.Format('html'),
                        ''
                        )



for directory in directories:
    original_files = directory.iterdir()
    qmd_file = directory / 'index.qmd'
    if qmd_file.is_file():
        html = directory / 'index.html'
        json = qmd_json(qmd_file, extract_media=directory/'static')
        print(json)
        # drop_pandas_styling(json)
        # Add line fixing paths
        json_string = pandoc.write(json, format='json')
        json_string = json_string.replace(root.as_posix(), '')
        json_scrubbed = pandoc.read(json_string, format='json')
        html_ = pandoc.write(json_scrubbed, format='html')
        html_ = scrub_pandas_styling(html_)
        html.open('w').write(html_)
        layout = directory / 'layout.py'
        if (not layout.is_file()) or args.replace:
            layout.open('w').write(init_string)
        routes = directory / 'routes.py'
        if (not routes.is_file()) or args.replace:
            routes.open('w').write('')
        index_files = directory / 'index_files'
        if index_files.is_dir():
            shutil.rmtree(index_files.as_posix())

