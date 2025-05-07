from pathlib import Path


def has_fastqmd(dir, page_group=False):
    if page_group:
        return (dir / '.qmd_page_group').is_file()
    return (dir / '.fastqmd').is_file()

def find_root(path=Path.cwd(), page_group=False):
    for parent in [path] + list(path.parents):
        if has_fastqmd(parent, page_group=page_group):
            return parent

def get_route_base(file):
    cwd = Path(file).resolve().parent
    root = find_root(cwd, page_group=True).parent
    return '/' / cwd.relative_to(root)