from pilot.qmd.app import qmd_app
from fasthtml.common import Link
from config.layout import paths, headers, footers


app, rt, serve = qmd_app(
    project_root=paths.root,
    hdrs=(
        Link(rel='stylesheet', href='/config/global_theme.css', type='text/css'),
        ),
    qmd_directories=paths.creation_groups,
    headers=headers,
    footers=footers,
)


serve()