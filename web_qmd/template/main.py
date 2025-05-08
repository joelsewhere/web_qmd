from web_qmd.app import qmd_app
from fasthtml.common import Link
from src.config.layout import paths, headers, footers
from web_qmd.utils.layout import load_html


app, rt, serve = qmd_app(
    project_root=paths.root,
    hdrs=(
        Link(rel='stylesheet', href=paths.theme.as_posix(), type='text/css'),
        ),
    qmd_directories=paths.content_groups,
    headers=headers,
    footers=footers,
)

@rt('/')
def get():

    return load_html('index.html', headers=headers, footers=footers)


serve()