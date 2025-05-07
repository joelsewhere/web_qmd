
import importlib.util
from pathlib import Path
 
def load_module(path:Path):

    spec=importlib.util.spec_from_file_location(path.stem, path.as_posix())
    
    foo = importlib.util.module_from_spec(spec)
    
    spec.loader.exec_module(foo)

    return foo