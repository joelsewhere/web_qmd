import sys 
import logging
from web_qmd.render import render
from uvicorn.supervisors import basereload
import sh

logger = logging.getLogger("uvicorn.error")

# ===============================================================================
# Edit file listener so changes to .qmd files generates a rerender
class BaseReload(basereload.BaseReload):

    def run(self) -> None:
        self.startup()
        sh.pip('install', '-r', (Path(self.config.root_path) / 'requirements.txt').as_posix())
        for changes in self:
            if changes:
                changes = list(changes)
                for change in changes:
                    if change.suffix == '.qmd':
                        sh.cd(self.config.root_path)
                        render(change, self.config.root_path, logger=logger)
                logger.warning(
                    "%s detected changes in %s. Reloading...",
                    self.reloader_name,
                    ", ".join(map(basereload._display_path, changes)),
                )

                self.restart()

        self.shutdown()

basereload.BaseReload = BaseReload

# ===============================================================================
# Monkey patch uvicorn

def uncache(exclude):
    """Remove package modules from cache except excluded ones.
    On next import they will be reloaded.

    Args:
        exclude (iter<str>): Sequence of module paths.

    Thank you! https://medium.com/@chipiga86/python-monkey-patching-like-a-boss-87d7ddb8098e
    """
    pkgs = []
    for mod in exclude:
        pkg = mod.split('.', 1)[0]
        pkgs.append(pkg)

    to_uncache = []
    for mod in sys.modules:
        if mod in exclude:
            continue

        if mod in pkgs:
            to_uncache.append(mod)
            continue

        for pkg in pkgs:
            if mod.startswith(pkg + '.'):
                to_uncache.append(mod)
                break

    for mod in to_uncache:
        del sys.modules[mod]


uncache(['uvicorn._subprocess', 'uvicorn.supervisors.basereload'])
# ===============================================================================
# QMD App


import os
import inspect
import uvicorn
from typing import List
from pathlib import Path
from fastcore.basics import listify
from fasthtml.common import fast_app, Body
from web_qmd.utils.modules import load_module
from web_qmd.utils import get_route_base
from web_qmd.components import CombinedComponent
from starlette.routing import Mount
from types import MethodType



def add_route(self, route):
    """
    Overwrite existing routes by inserting derived routes
    at the beginning of the routes list
    """
    route.methods = [m.upper() for m in listify(route.methods)]
    self.router.routes = [r for r in self.routes if not
                    (r.path==route.path and r.name == route.name and
                    ((route.methods is None) or (set(r.methods) == set(route.methods))))]
    self.router.routes.insert(0, route)

def mount(self, path: str, app, name: str | None = None) -> None:  # pragma: no cover
    """
    Overwrite existing routes by inserting derived routes
    at the beginning of the routes list
    """
    route = Mount(path, app=app, name=name)
    self.routes.insert(0, route)


def qmd_app(
        project_root: Path,
        pico=False,
        hdrs=(),
        qmd_directories:List[Path]=[],
        headers = [],
        footers = [],
        ):
    """
    Generates QMD App
    """

    app,rt = fast_app(
        pico=pico,
        hdrs=hdrs,
    )

    # LAST ADD
    app.add_route = MethodType(add_route, app)
    app.router.mount = MethodType(mount, app.router)

    import web_qmd
    setattr(web_qmd, 'app', app)

    app.root_path = project_root.as_posix()
    app.router.redirect_slashes = False 

    def create_endpoint(endpoint, group):

        
        @rt(endpoint, include_in_schema=False)
        def get(location:str=''):
            
            layout_path = group / location / 'layout.py'
            page_layout = load_module(layout_path).layout
            from web_qmd import app

            print(app.router.routes)

            class PageLayout(CombinedComponent):

                outer_tag_type = Body
                children = []

                if page_layout.headers:
                
                    children += headers

                children.append(page_layout)

                if page_layout.footers:

                    children += footers

            layout = PageLayout()

            return layout()


    for directory in qmd_directories:

        for route_file in directory.rglob('routes.py'):
            load_module(route_file)

        group_indicator = directory / '.qmd_page_group'
        if not group_indicator.is_file():
            group_indicator.open('w').write('')

        endpoint = f'/{directory.stem}/' + '{location:str}'  
        print('ENDPOINT', endpoint)
        create_endpoint(endpoint, directory)
        
        directory_path = f'/{directory.stem}'
        print('DIRECTORY:', directory_path)
        create_endpoint(directory_path, directory)
        print(app.router.routes)




# Copy of the fasthtml.core::serve
# The function in fasthtml doesn't 


    def serve(
            appname=None, # Name of the module
            app='app', # App instance to be served
            host='0.0.0.0', # If host is 0.0.0.0 will convert to localhost
            port=None, # If port is None it will default to 5001 or the PORT environment variable
            reload=True, # Default is to reload the app upon code changes
            reload_includes:list[str]|str|None=None, # Additional files to watch for changes
            reload_excludes:list[str]|str|None=None # Files to ignore for changes
            ): 
        "Run the app in an async server, with live reload set as the default."
        bk = inspect.currentframe().f_back
        glb = bk.f_globals
        code = bk.f_code
        if not appname:
            if glb.get('__name__')=='__main__': appname = Path(glb.get('__file__', '')).stem
            elif code.co_name=='main' and bk.f_back.f_globals.get('__name__')=='__main__': appname = inspect.getmodule(bk).__name__
        if appname:
            if not port: port=int(os.getenv("PORT", default=5001))
            uvicorn.run(
                f'{appname}:{app}',
                host=host,
                port=port,
                reload=reload,
                reload_includes=["*.qmd"],
                reload_excludes=reload_excludes,
                root_path=project_root.as_posix()
                )
    
            
    return app, rt, serve


def qmd_sub_app(file, **kwargs):
    """
    TODO: Rework this to use mounting starlett subapps/mounting
    """

    _sub_app, rt = fast_app(**kwargs)

    route_base = get_route_base(file)

    from web_qmd import app

    app.mount(path=route_base.as_posix(), app=_sub_app)

    return _sub_app, rt

# app.router: https://github.com/AnswerDotAI/fasthtml/blob/324ba3746b8892ccdc35f707c4c270aaba4d9e3b/fasthtml/core.py#L554C9-L554C44
# @router add endpoint: https://github.com/AnswerDotAI/fasthtml/blob/324ba3746b8892ccdc35f707c4c270aaba4d9e3b/fasthtml/core.py#L577
# router class: https://github.com/AnswerDotAI/fasthtml/blob/324ba3746b8892ccdc35f707c4c270aaba4d9e3b/fasthtml/core.py#L446

