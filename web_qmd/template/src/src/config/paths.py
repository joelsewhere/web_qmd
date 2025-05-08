import sys
from pathlib import Path
from web_qmd.utils.roots import find_root

root = find_root()
sys.path.append(root.as_posix())

content = root / 'content'
config = root / 'config'
theme = config / 'global_theme.css'
files = root / 'files'
logo = Path(files.name)  / 'images' / 'logo.png'


content_groups = [x for x in content.iterdir() if x.is_dir()]





