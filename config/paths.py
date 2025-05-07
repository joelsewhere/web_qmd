import sys
from pathlib import Path

file_dir = 'files'

root = Path(__file__).resolve().parents[1]
sys.path.append(root.as_posix())

creations = root / 'creations'

creation_groups = [x for x in creations.iterdir() if x.is_dir()]

files = root / file_dir

logo = Path(file_dir)  / 'images' / 'logo.png'