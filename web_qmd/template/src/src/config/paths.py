import sys
from pathlib import Path
from web_qmd.utils.roots import find_root

root = find_root()
sys.path.append(root.as_posix())
src = root / 'src' / 'src'

content = root / 'content'
config = src / 'config'
theme_absolute = config / 'global_theme.css'
theme = '/' / theme_absolute.relative_to(root)
files = root / 'files'
logo = Path(files.name)  / 'images' / 'logo.png'


content_groups = [x for x in content.iterdir() if x.is_dir()]





